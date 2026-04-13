---
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

Generated from `docs/releases/latest`. Filenames can change between versions, so this page maps the current release files by fuzzy matching platform and distribution tokens in the release filenames.

## Recommended Downloads

| Use | Download | Release file |
| --- | --- | --- |
| Windows executable | [Windows x86_64 (v2.0.0)](../releases/latest/main-v2.0.0-windows11-server2022-x86_64.exe) | `main-v2.0.0-windows11-server2022-x86_64.exe` |
| macOS Sequoia executable | [macOS Sequoia ARM64 (v2.0.0)](../releases/latest/main-v2.0.0-macos-sequoia-apple-silicon-arm64) | `main-v2.0.0-macos-sequoia-apple-silicon-arm64` |
| macOS Sonoma executable | [macOS Sonoma ARM64 (v2.0.0)](../releases/latest/main-v2.0.0-macos-sonoma-apple-silicon-arm64) | `main-v2.0.0-macos-sonoma-apple-silicon-arm64` |
| Ubuntu 24 / Noble executable | [Ubuntu 24 / Noble x86_64 (v2.0.0)](../releases/latest/main-v2.0.0-linux-ubuntu24-noble-x86_64) | `main-v2.0.0-linux-ubuntu24-noble-x86_64` |
| Ubuntu 22 / Jammy executable | [Ubuntu 22 / Jammy x86_64 (v2.0.0)](../releases/latest/main-v2.0.0-linux-ubuntu22-jammy-x86_64) | `main-v2.0.0-linux-ubuntu22-jammy-x86_64` |
| Debian 12 / Bookworm executable | [Debian 12 / Bookworm x86_64 (v2.0.0)](../releases/latest/main-v2.0.0-linux-debian12-bookworm-x86_64) | `main-v2.0.0-linux-debian12-bookworm-x86_64` |
| Fedora executable | [Fedora x86_64 (v2.0.0)](../releases/latest/main-v2.0.0-linux-fedora41-x86_64) | `main-v2.0.0-linux-fedora41-x86_64` |
| Arch Linux executable | [Arch Linux x86_64 (v2.0.0)](../releases/latest/main-v2.0.0-linux-arch-rolling-x86_64) | `main-v2.0.0-linux-arch-rolling-x86_64` |
| Verify downloaded release files | [Checksums](../releases/latest/SHA256SUMS.txt) | `SHA256SUMS.txt` |
| Read release notes | [Release notes](../releases/latest/README.md) | `README.md` |

## Release Directory

- [Open the `latest` release notes](../releases/latest/README.md)
- [Open `llm.txt`](../llm.txt)

## Runtime Setup

Before running a release executable, install the Python runtime package:

```bash
python -m pip install orch-lib
```

## Verify Download Integrity

After downloading a binary, verify it with `SHA256SUMS.txt`.

```bash
# Linux/macOS
sha256sum -c SHA256SUMS.txt

# Windows PowerShell
Get-FileHash .\main-v2.0.0-windows11-server2022-x86_64.exe -Algorithm SHA256
```

