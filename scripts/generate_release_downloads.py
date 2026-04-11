from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
RELEASES_DIR = DOCS_DIR / "releases"
PREFERRED_RELEASE_DIR = "latest"
OUTPUT_PATH = DOCS_DIR / "Installation" / "Downloads.md"


@dataclass(frozen=True)
class ReleaseAsset:
    path: Path
    label: str
    use: str
    rank: int


def normalized(path: Path) -> str:
    return path.name.lower().replace("_", "-")


def extract_version(name: str) -> str:
    match = re.search(r"v\d+(?:\.\d+)+", name, re.IGNORECASE)
    return match.group(0) if match else "current"


def contains_any(name: str, words: tuple[str, ...]) -> bool:
    return any(word in name for word in words)


def classify_asset(path: Path) -> tuple[str, str, int] | None:
    name = normalized(path)
    if path.is_dir():
        return None

    if name == "sha256sums.txt":
        return ("Checksums", "Verify downloaded release files", 90)
    if name == "readme.md":
        return ("Release notes", "Read release notes", 91)

    version = extract_version(name)
    arch = "ARM64" if contains_any(name, ("arm64", "apple-silicon")) else "x86_64"

    if contains_any(name, ("windows", "win")) or path.suffix.lower() == ".exe":
        return (f"Windows {arch} ({version})", "Windows executable", 10)

    if contains_any(name, ("macos", "darwin", "sonoma", "sequoia")):
        if "sequoia" in name:
            return (f"macOS Sequoia {arch} ({version})", "macOS Sequoia executable", 20)
        if "sonoma" in name:
            return (f"macOS Sonoma {arch} ({version})", "macOS Sonoma executable", 21)
        return (f"macOS {arch} ({version})", "macOS executable", 22)

    if "linux" in name:
        linux_targets = (
            (("ubuntu24", "noble"), "Ubuntu 24 / Noble"),
            (("ubuntu22", "jammy"), "Ubuntu 22 / Jammy"),
            (("debian", "bookworm"), "Debian 12 / Bookworm"),
            (("fedora",), "Fedora"),
            (("arch", "rolling"), "Arch Linux"),
        )
        for offset, (needles, label) in enumerate(linux_targets):
            if contains_any(name, needles):
                return (f"{label} {arch} ({version})", f"{label} executable", 30 + offset)
        return (f"Linux {arch} ({version})", "Linux executable", 39)

    return (f"{path.name} ({version})", "Release file", 80)


def find_release_dir() -> Path:
    preferred = RELEASES_DIR / PREFERRED_RELEASE_DIR
    if preferred.exists():
        return preferred

    candidates = sorted(
        (path for path in RELEASES_DIR.iterdir() if path.is_dir()),
        key=lambda path: path.name.lower(),
        reverse=True,
    )
    if candidates:
        return candidates[0]

    raise FileNotFoundError(f"No release directory found in {RELEASES_DIR}")


def collect_assets(release_dir: Path) -> list[ReleaseAsset]:
    assets: list[ReleaseAsset] = []
    for path in sorted(release_dir.iterdir(), key=lambda item: item.name.lower()):
        classified = classify_asset(path)
        if classified is None:
            continue
        label, use, rank = classified
        assets.append(ReleaseAsset(path=path, label=label, use=use, rank=rank))
    return sorted(assets, key=lambda asset: (asset.rank, asset.label.lower()))


def link_for(path: Path) -> str:
    return os.path.relpath(path, OUTPUT_PATH.parent).replace("\\", "/")


def build_markdown(release_dir: Path, assets: list[ReleaseAsset]) -> str:
    rows = "\n".join(
        f"| {asset.use} | [{asset.label}]({link_for(asset.path)}) | `{asset.path.name}` |"
        for asset in assets
    )

    return f"""---
title: Downloads
summary: Download ORCH release files from the static site releases directory.
owner: Durga Sai
verification: Generated
tags:
  - installation
  - downloads
  - releases
---

# Downloads

Generated from `docs/releases/{release_dir.name}`. Filenames can change between versions, so this page maps the current release files by fuzzy matching platform and distribution tokens in the release filenames.

## Recommended Downloads

| Use | Download | Release file |
| --- | --- | --- |
{rows}

## Release Directory

- [Open the `{release_dir.name}` release notes]({link_for(release_dir / "README.md")})
- [Open `llm.txt`](../llm.txt)

## Runtime Setup

Before running a release executable, install the Python runtime package:

```bash
python -m pip install orch-lib
```

"""


def main() -> None:
    release_dir = find_release_dir()
    assets = collect_assets(release_dir)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(build_markdown(release_dir, assets), encoding="utf-8")

    print(f"Generated {OUTPUT_PATH} from {len(assets)} files in {release_dir}.")


if __name__ == "__main__":
    main()



