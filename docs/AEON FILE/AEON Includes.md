---
title: AEON Includes
summary: Import `.lib` files, Python libraries, and Python scripts into `.aeon` files.
owner: Durga Sai
verification: Verified
tags:
  - aeon
  - includes
---

# AEON Includes

Inside the Agent Definition context (`.aeon` files), the `Include` keyword serves a fundamentally different purpose compared to the global orchestrator.

In an `.aeon` file, `Include` is used to import reusable modules, shared functions, or native Python libraries directly into the agent's internal logic.

## Resolution Order

When you use `Include my_module` inside an `.aeon` file, the transpiler follows a specific fallback order to resolve the import:

1. **Local `.lib` Files:** First, it checks whether a file named `my_module.lib` exists within your project directory.
2. **Built-in Libraries:** Second, it checks ORCH's default native library system. There are currently no built-in libraries available.
3. **Python Libraries and Scripts:** Finally, if both checks fail, it assumes `my_module` is either an installed Python package or an external `.py` script and uses the Python runtime to import it.

!!! warning
    You cannot use relative import paths for Python scripts yet, such as `Include ../utils`. Provide the absolute module name instead.

## Usage Examples

Below are clean examples demonstrating how the compiler resolves different scenarios based on the fallback order. Unlike the orchestrator, you **cannot** instantiate arrays of objects with `{N}` here.

### 1. Including a Local `.lib` File

If you have a file named `math_logic.lib` in your project folder, this pulls its shared functional logic into the agent.

```orch
Include math_logic
```

### 2. Including Native Python Libraries

If no local `.lib` file or ORCH built-in module matches, the system delegates to Python's execution space. This is how you bring Python ecosystem libraries into your agent's `Func` scopes.

```orch
# Automatically resolved as standard Python libraries.
Include math
Include json
```

### 3. Including External Python Scripts

Identical to a library, you can import your own local `.py` scripts, for example `utils.py`. Relative paths such as `../utils` are strictly forbidden.

```orch
# Resolves the external `utils.py` script located in your project root.
Include utils
```

By supporting agent-level includes across all three fallback contexts, agents can share complex algorithmic logic without rewriting functional blocks.

## Next

- [Agent Memory](AEON%20Memory.md)
- [Tasks](TASKS.md)
- [Library Functions](../LIB%20FILE/Functions.md)
