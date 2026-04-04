# Usage and Structure

Owner: Durga Sai
Verification: Verified
Tags: Usage

# ORCH DSL: Usage and Project Structure

The ORCH DSL provides a distributed compilation pipeline. The front-end compiler, `main.exe` (written in OCaml), parses your ORCH project, generates a JSON representation (AST), and then invokes a Python script (`converter.py`) to transpile the project into a runnable Python application leveraging `orch-lib`.

## Usage

You can run the compiler using the following syntax:

```bash
./main.exe [--dryrun] [--verbose] [--no-delete] <project_directory>
```

### Options

- `<project_directory>` : **(Required)** Specifies the path to the directory containing your project.
- `-dryrun` : **(Optional)** Generates the Python file without executing it.
- `-verbose` : **(Optional)** Enables verbose logging.
- `-no-delete` : **(Optional)** Prevents automatic cleanup of the generated `.json` and `.py` files.

### Internal Workflow

1. **Parsing:** `main.exe` reads the project in `<project_directory>`.
2. **JSON Generation:** Constructs an AST and outputs it as JSON.
3. **Transpilation:** Converts the JSON file to a Python execution file (`<project_name>.py`).
4. **Execution:** Automatically runs the Python file.
5. **Cleanup:** Deletes intermediate generated `.json` and `.py` files.

---

## Project Structure

Your project should exist within a single directory. The ORCH DSL is designed to cleanly separate global orchestration logic from agent-specific task logic.

### Directory Components

Your directory can contain the following:
- **The Global Dispatcher (`.orch` files):** The main entry point for the entire project.
- **Agent Definitions (`.aeon` files):** The individual files or blocks implementing your specific agents.
- **`*.lib`:** (Optional) Sub-library files containing shared functions.
- **`*.py`:** (Optional) External Python scripts for direct absolute imports. Note: relative imports are NOT accepted.

### The Global Dispatcher (`.orch` files)

The orchestrator handles overall global routing logic and configures which agents exist. Core blocks that can be there:
- **Includes:** Defines the agents to be pulled in.
- **Global Variables:** Top-level state accessible across the entire structure.
- **Global Route:** Central authority deciding which agent runs next.

### The Agent Definition (`.aeon` files)

An agent defines its own memory, executable actions, internal routing logic, and python bindings. Component blocks that can be there:
- **`Private`:** Defines the agent memory and internal state variables (both private scope and public scope).
- **`Task`:** Defines executable actions intended to mutate state.
- **`Func`:** Defines custom inline native Python extensions for complex capability.
- **`Route`:** Defines the internal, agent-specific routing rules dictating which task executes.

### The Library Definition (`.lib` files)

A Library file is just a list of functions in a file that needed to be imported in `.aeon` files