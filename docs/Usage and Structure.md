---
title: Usage and Structure
summary: How to run the compiler and organize an ORCH project directory.
owner: Durga Sai
verification: Verified
tags:
  - usage
  - structure
---

# Usage and Structure

The ORCH DSL provides a distributed compilation pipeline. The front-end compiler, `main.exe` (written in OCaml), parses your ORCH project, generates a JSON representation (AST), and then invokes a Python script (`converter.py`) to transpile the project into a runnable Python application leveraging `orch-lib`.

## Installation

Before running the compiler, install the Python runtime package:

```bash
python -m pip install orch-lib
```

Need the compiler executable or `llm.txt`? See [Downloads](Installation/Downloads.md).

## Usage

You can run the compiler using the following syntax:

```bash
./main.exe [--dryrun] [--verbose] [--no-delete] <project_directory>
```

Platform examples:

```bash
# Linux/macOS
./main.exe --verbose example

# Windows PowerShell
.\main.exe --verbose example
```

### Options

- `<project_directory>`: **Required.** Specifies the path to the directory containing your project.
- `--dryrun`: **Optional.** Generates the Python file without executing it.
- `--verbose`: **Optional.** Enables verbose logging.
- `--no-delete`: **Optional.** Prevents automatic cleanup of the generated `.json` and `.py` files.

### Internal Workflow

1. **Parsing:** `main.exe` reads the project in `<project_directory>`.
2. **JSON Generation:** Constructs an AST and outputs it as JSON.
3. **Transpilation:** Converts the JSON file to a Python execution file (`<project_name>.py`).
4. **Execution:** Automatically runs the Python file unless `--dryrun` is set.
5. **Cleanup:** Deletes intermediate generated `.json` and `.py` files.

## Developer Workflow (Compiler Repo)

For contributors working on the compiler/runtime codebase, use this canonical command flow:

```bash
dune build
dune runtest
pytest
dune clean
```

### Running Tests Locally

**OCaml Tests** are automatically configured and run as part of the development workflow:

- `dune build`: Compiles all OCaml code and runs type checking.
- `dune runtest`: Runs the OCaml test suite against compiled code.

The OCaml test suite includes comprehensive tests for the lexer, parser, AST, scope checking, and code generation modules. No additional configuration is needed; tests are discoverable and executable via `dune`.

**Python Tests** are run separately:  

```bash
pytest
```

This runs the Python runtime test suite for transpilation correctness, runtime behavior, and integration scenarios.

Template/codegen scaffolding should be treated as setup/build artifacts and not regenerated on every run.

## Project Structure

Your project should exist within a single directory. The ORCH DSL is designed to cleanly separate global orchestration logic from agent-specific task logic.

### Directory Components

Your directory can contain the following:

- **The Global Dispatcher (`.orch` files):** The main entry point for the entire project.
- **Agent Definitions (`.aeon` files):** The individual files or blocks implementing your specific agents.
- **`*.lib`:** Optional sub-library files containing shared functions.
- **`*.py`:** Optional external Python scripts for direct absolute imports. Relative imports are not accepted.

### The Global Dispatcher (`.orch` files)

The orchestrator handles overall global routing logic and configures which agents exist. Core blocks that can be there:

- **Includes:** Defines the agents to be pulled in.
- **Global Variables:** Top-level state accessible across the entire structure.
- **Global Route:** Central authority deciding which agent runs next.

### The Agent Definition (`.aeon` files)

An agent defines its own memory, executable actions, internal routing logic, and Python bindings. Component blocks that can be there:

- **`Private`:** Defines the agent memory and internal state variables, including private and public scope.
- **`Task`:** Defines executable actions intended to mutate state.
- **`Func`:** Defines custom inline native Python extensions for complex capability.
- **`Route`:** Defines the internal, agent-specific routing rules dictating which task executes.

### The Library Definition (`.lib` files)

A library file is a list of functions that can be imported by `.aeon` files.

## Next

- [Installation](Installation.md)
- [Downloads](Installation/Downloads.md)
- [ORCH Files](ORCH%20FILES.md)
- [AEON Files](AEON%20FILE.md)
- [Library Files](LIB%20FILE.md)

