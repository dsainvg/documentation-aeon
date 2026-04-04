#!/usr/bin/env python3
"""Import a nested Notion-style export while preserving the original tree."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse
from uuid import uuid4
from zipfile import ZipFile


NOTION_ID_SUFFIX = re.compile(r"\s+[0-9a-f]{32}(?=\.[^.]+$|$)", re.IGNORECASE)
MARKDOWN_LINK_RE = re.compile(r"(!?\[[^\]]*]\()([^)]+)(\))")
DEFAULT_MOJIBAKE = {
    "\u00e2\u20ac\u2122": "'",
    "\u00e2\u20ac\u201c": '"',
    "\u00e2\u20ac\u009d": '"',
    "\u00e2\u20ac\u201d": "-",
    "\u00e2\u2020\u2019": "->",
}


class NavDir:
    def __init__(self, name: str) -> None:
        self.name = name
        self.files: list[Path] = []
        self.children: dict[str, "NavDir"] = {}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Unpack a nested Notion-style export ZIP, keep the original file and "
            "folder names, remove the trailing Notion IDs, rename the top page to "
            "index.md, and rewrite internal markdown links."
        )
    )
    parser.add_argument("archive", type=Path, help="Path to the outer export ZIP.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs-imported"),
        help="Directory to write the cleaned export into. Defaults to docs-imported.",
    )
    parser.add_argument(
        "--root-page",
        help="Optional top page title, for example 'DSL USER GUIDE'.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the planned output tree without writing files.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow writing into a non-empty output directory.",
    )
    parser.add_argument(
        "--mkdocs-config",
        type=Path,
        default=Path("mkdocs-imported.yml"),
        help="Path to the generated MkDocs config file. Defaults to mkdocs-imported.yml.",
    )
    parser.add_argument(
        "--mkdocs-template",
        type=Path,
        default=Path("mkdocs-template.yml"),
        help="Existing MkDocs config to copy non-nav settings from. Defaults to mkdocs-template.yml.",
    )
    return parser.parse_args()


def clean_name(name: str) -> str:
    return NOTION_ID_SUFFIX.sub("", name).strip()


def unwrap_nested_export(archive: Path, temp_root: Path) -> Path:
    current_archive = archive
    for depth in range(8):
        layer_dir = temp_root / f"layer_{depth}"
        layer_dir.mkdir(parents=True, exist_ok=True)
        with ZipFile(current_archive) as zip_file:
            zip_file.extractall(layer_dir)

        files = [path for path in layer_dir.rglob("*") if path.is_file()]
        markdown_files = [path for path in files if path.suffix.lower() == ".md"]
        nested_archives = [path for path in files if path.suffix.lower() == ".zip"]

        if markdown_files:
            return layer_dir

        if len(nested_archives) == 1:
            current_archive = nested_archives[0]
            continue

        raise RuntimeError(
            "Could not locate markdown files inside the export archive. "
            "If there are multiple nested ZIP files, extract the correct one first."
        )

    raise RuntimeError("Exceeded the maximum supported nested ZIP depth.")


def find_root_markdown(extracted_root: Path, expected_title: str | None) -> Path:
    markdown_files = [path for path in extracted_root.rglob("*.md")]
    if not markdown_files:
        raise RuntimeError("No markdown files were found after extraction.")

    if expected_title:
        matches = [path for path in markdown_files if clean_name(path.stem).casefold() == expected_title.casefold()]
        if not matches:
            raise RuntimeError(f"Could not find a root page named {expected_title!r}.")
        if len(matches) > 1:
            raise RuntimeError(f"Found multiple pages named {expected_title!r}.")
        return matches[0]

    shallowest_depth = min(len(path.relative_to(extracted_root).parts) for path in markdown_files)
    candidates = [path for path in markdown_files if len(path.relative_to(extracted_root).parts) == shallowest_depth]
    if len(candidates) == 1:
        return candidates[0]

    names = ", ".join(clean_name(path.stem) for path in sorted(candidates))
    raise RuntimeError(
        "Could not infer the root page automatically. "
        f"Top-level candidates: {names}. Use --root-page to choose one."
    )


def child_folder_for(page_md: Path) -> Path | None:
    candidate = page_md.parent / clean_name(page_md.stem)
    return candidate if candidate.is_dir() else None


def ensure_output_dir(output_dir: Path, force: bool) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    if any(output_dir.iterdir()) and not force:
        raise RuntimeError(
            f"Output directory {output_dir} is not empty. Use --force or choose another --output directory."
        )


def build_clean_tree(root_md: Path) -> dict[Path, Path]:
    mapping: dict[Path, Path] = {}
    used_targets: set[Path] = set()

    def allocate(relative_path: Path) -> Path:
        candidate = relative_path
        index = 2
        while candidate in used_targets:
            stem = candidate.stem
            suffix = candidate.suffix
            candidate = candidate.with_name(f"{stem}-{index}{suffix}")
            index += 1
        used_targets.add(candidate)
        return candidate

    root_dir = root_md.parent
    root_children_dir = child_folder_for(root_md)
    if root_children_dir is None:
        raise RuntimeError(f"Could not find the folder for root page {root_md.name!r}.")

    mapping[root_md.resolve()] = Path("index.md")
    used_targets.add(Path("index.md"))

    for item in sorted(root_children_dir.rglob("*"), key=lambda path: (len(path.parts), str(path).casefold())):
        relative = item.relative_to(root_children_dir)
        cleaned_parts = [clean_name(part) for part in relative.parts]
        cleaned_relative = Path(*cleaned_parts)
        target = allocate(cleaned_relative)
        mapping[item.resolve()] = target

    for sibling in sorted(root_dir.iterdir(), key=lambda path: path.name.casefold()):
        if sibling.resolve() == root_md.resolve():
            continue
        if sibling.resolve() == root_children_dir.resolve():
            continue
        target = allocate(Path(clean_name(sibling.name)))
        mapping[sibling.resolve()] = target

    return mapping


def fix_mojibake(text: str) -> str:
    for bad, good in DEFAULT_MOJIBAKE.items():
        text = text.replace(bad, good)
    return text


def rewrite_markdown_links(text: str, source_md: Path, target_md: Path, target_lookup: dict[Path, Path]) -> str:
    source_dir = source_md.parent.resolve()
    target_dir = target_md.parent

    def replace(match: re.Match[str]) -> str:
        raw_target = match.group(2).strip()
        if not raw_target or raw_target.startswith("#"):
            return match.group(0)

        parsed = urlparse(raw_target)
        if parsed.scheme or raw_target.startswith(("/", "\\")):
            return match.group(0)

        decoded_path = unquote(parsed.path)
        resolved = (source_dir / decoded_path).resolve()
        mapped = target_lookup.get(resolved)
        if mapped is None:
            return match.group(0)

        relative_target = os.path.relpath(mapped, target_dir)
        relative_target = Path(relative_target).as_posix()
        if parsed.fragment:
            relative_target = f"{relative_target}#{parsed.fragment}"
        return f"{match.group(1)}{relative_target}{match.group(3)}"

    return MARKDOWN_LINK_RE.sub(replace, text)


def label_from_markdown(path: Path) -> str:
    if path.name == "index.md" and path.parent == Path("."):
        return "Home"
    return path.stem


def build_nav_tree(markdown_paths: list[Path]) -> NavDir:
    root = NavDir("")
    for markdown_path in markdown_paths:
        current = root
        for part in markdown_path.parts[:-1]:
            current = current.children.setdefault(part, NavDir(part))
        current.files.append(markdown_path)
    return root


def render_nav_items(node: NavDir, base: Path = Path(".")) -> list[tuple[str, str | list]]:
    items: list[tuple[str, str | list]] = []
    files_by_name = {path.name: path for path in node.files}

    if base == Path(".") and "index.md" in files_by_name:
        items.append(("Home", "index.md"))

    consumed_files = {"index.md"} if base == Path(".") and "index.md" in files_by_name else set()

    for dir_name in sorted(node.children):
        child = node.children[dir_name]
        matching_file = files_by_name.get(f"{dir_name}.md")
        child_items: list[tuple[str, str | list]] = []
        if matching_file is not None:
            child_items.append(("Overview", matching_file.as_posix()))
            consumed_files.add(matching_file.name)
        child_items.extend(render_nav_items(child, base / dir_name))
        items.append((dir_name, child_items))

    remaining_files = [path for path in node.files if path.name not in consumed_files]
    for file_path in sorted(remaining_files, key=lambda path: path.name.casefold()):
        items.append((label_from_markdown(file_path), file_path.as_posix()))

    return items


def nav_items_to_yaml_lines(items: list[tuple[str, str | list]], indent: int = 0) -> list[str]:
    lines: list[str] = []
    prefix = " " * indent
    for label, value in items:
        if isinstance(value, list):
            lines.append(f"{prefix}- {label}:")
            lines.extend(nav_items_to_yaml_lines(value, indent + 4))
        else:
            lines.append(f"{prefix}- {label}: {value}")
    return lines


def strip_top_level_keys(text: str, keys: set[str]) -> str:
    lines = text.splitlines()
    kept: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):", line)
        if match and match.group(1) in keys:
            index += 1
            while index < len(lines):
                next_line = lines[index]
                if next_line and not next_line[0].isspace():
                    break
                index += 1
            continue
        kept.append(line)
        index += 1
    return "\n".join(kept).strip()


def build_mkdocs_config_text(output_dir: Path, config_path: Path, template_path: Path, nav_items: list[tuple[str, str | list]]) -> str:
    nav_lines = nav_items_to_yaml_lines(nav_items, indent=2)

    if template_path.is_file():
        base_text = template_path.read_text(encoding="utf-8")
        base_text = strip_top_level_keys(base_text, {"nav"})
    else:
        base_text = "site_name: Imported Docs\nuse_directory_urls: true"

    sections = [base_text, "nav:\n" + "\n".join(nav_lines)]
    return "\n\n".join(section for section in sections if section.strip()) + "\n"


def print_plan(path_map: dict[Path, Path], output_dir: Path, mkdocs_config: Path, nav_items: list[tuple[str, str | list]]) -> None:
    print(f"Archive will be imported into: {output_dir}")
    print("")
    for source_path, relative_target in sorted(path_map.items(), key=lambda item: item[1].as_posix().casefold()):
        print(f"{source_path} -> {output_dir / relative_target}")
    print("")
    print(f"MkDocs config will be written to: {mkdocs_config}")
    print("nav:")
    for line in nav_items_to_yaml_lines(nav_items, indent=2):
        print(line)


def write_output(path_map: dict[Path, Path], output_dir: Path) -> None:
    for source_path, relative_target in sorted(path_map.items(), key=lambda item: item[1].as_posix().casefold()):
        destination = output_dir / relative_target

        if source_path.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
            continue

        destination.parent.mkdir(parents=True, exist_ok=True)
        if source_path.suffix.lower() == ".md":
            content = source_path.read_text(encoding="utf-8")
            content = fix_mojibake(content)
            content = rewrite_markdown_links(content, source_path, relative_target, path_map)
            destination.write_text(content, encoding="utf-8")
        else:
            shutil.copy2(source_path, destination)


def write_mkdocs_config(config_text: str, config_path: Path) -> None:
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(config_text, encoding="utf-8")


def main() -> int:
    args = parse_args()
    temp_root: Path | None = None

    try:
        archive = args.archive.resolve()
        if not archive.is_file():
            raise RuntimeError(f"Archive not found: {archive}")

        output_dir = args.output.resolve()
        mkdocs_config = args.mkdocs_config.resolve()
        mkdocs_template = args.mkdocs_template.resolve()
        if not args.dry_run:
            ensure_output_dir(output_dir, args.force)

        temp_root = (Path.cwd() / f".notion-import-{uuid4().hex[:8]}").resolve()
        temp_root.mkdir(parents=True, exist_ok=False)

        extracted_root = unwrap_nested_export(archive, temp_root)
        root_md = find_root_markdown(extracted_root, args.root_page)
        path_map = build_clean_tree(root_md)
        markdown_paths = sorted(
            [relative_path for relative_path in path_map.values() if relative_path.suffix.lower() == ".md"],
            key=lambda path: path.as_posix().casefold(),
        )
        nav_items = render_nav_items(build_nav_tree(markdown_paths))
        config_text = build_mkdocs_config_text(output_dir, mkdocs_config, mkdocs_template, nav_items)

        if args.dry_run:
            print_plan(path_map, output_dir, mkdocs_config, nav_items)
            return 0

        write_output(path_map, output_dir)
        write_mkdocs_config(config_text, mkdocs_config)

    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 1
    finally:
        if temp_root is not None:
            shutil.rmtree(temp_root, ignore_errors=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
