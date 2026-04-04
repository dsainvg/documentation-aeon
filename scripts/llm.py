from __future__ import annotations

from pathlib import Path


def iter_markdown_files(root: Path) -> list[Path]:
    files = [p for p in root.rglob("*.md") if p.is_file()]
    return sorted(files, key=lambda p: str(p.relative_to(root)).lower())


def build_llm_text(root: Path, files: list[Path]) -> str:
    chunks: list[str] = []
    for file_path in files:
        rel = file_path.relative_to(root).as_posix()
        content = file_path.read_text(encoding="utf-8", errors="replace")
        chunks.append(f"===== {rel} =====\n")
        chunks.append(content)
        chunks.append("\n\n")
    return "".join(chunks)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    # root_output_path = root / "llm.txt"
    docs_output_path = root / "docs" / "llm.txt"

    md_files = iter_markdown_files(root)
    output_text = build_llm_text(root, md_files)
    # root_output_path.write_text(output_text, encoding="utf-8")
    docs_output_path.write_text(output_text, encoding="utf-8")

    print(
        "Created llm.txt from "
        f"{len(md_files)} markdown files at "
        # f"{root_output_path} and {docs_output_path}."
    )


if __name__ == "__main__":
    main()