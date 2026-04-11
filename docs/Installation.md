---
title: Installation and Downloads
summary: Install Python runtime support and download the ORCH executable or LLM reference text.
owner: Durga Sai
verification: Verified
tags:
  - installation
  - downloads
---

# Installation and Downloads

Install the Python runtime package first, then download the compiler executable if you need the bundled Windows build.

## Requirements

- Python 3.10 or newer.
- `pip`, Python's package installer.

Check that both are available:

```bash
python --version
python -m pip --version
```

## Install `orch-lib`

Install the ORCH Python runtime package with `pip`:

```bash
python -m pip install orch-lib
```

## Downloads

Use these files when you need the bundled executable or a plain-text reference copy for LLM context.

<p class="download-actions">
  <a class="btn btn-primary" href="../downloads/orch.exe" download>Download orch.exe</a>
  <a class="btn btn-primary" href="../downloads/linux_main.exe" download>Download linux_main.exe</a>
  <a class="btn btn-secondary" href="../downloads/llm.txt" download>Download llm.txt</a>
</p>

Direct links:

- [orch.exe](downloads/orch.exe)
- [linux_main.exe](downloads/linux_main.exe)
- [llm.txt](downloads/llm.txt)

## Next

- [Usage and Structure](Usage and Structure.md)
- [ORCH Files](ORCH FILES.md)
