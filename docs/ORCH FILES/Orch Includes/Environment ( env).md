---
title: Environment Variables
summary: Load `.env` values into graph memory and Python runtime access.
owner: Durga Sai
verification: Verified
tags:
  - orch
  - environment
---

# Environment Variables

## Sourcing Environment Variables

By declaring the reserved phrase `Include env` in your global orchestrator (`.orch`), the transpiler hooks directly to the backend to automatically load and parse a `.env` file from the runtime directory.

```orch
# Automatically load all variables from `.env` into global graph memory.
Include env
```

All key-value pairs established in the `.env` file are unpacked and bundled into the overarching **Graph Memory** layer as explicitly public variables.

## 1. Example `.env` File

```dotenv
API_KEY=YOUR_SECRET_KEY
DB_HOST=localhost
```

## 2. Accessing From Inside an Agent (`Task` block)

Because the environment pairs map entirely into the graph's public memory structure, any initialized agent can read those variables in their `Task` blocks by reaching into the global scope with the `Public` accessor.

```orch
Task check_connection {
    # Natively fetches the variable loaded from `.env` into graph memory.
    current_key = Public.API_KEY;
}
```

## 3. Accessing From Python (`Func` block)

Because the ORCH compilation engine utilizes standard `dotenv` libraries under the hood during the script's execution phase, `.env` variables are also injected into the operating system shell environment.

This means any pure Python script running within an agent's `Func` escape hatch can use standard Python `os` modules to fetch them natively, sidestepping standard graph memory:

```orch
Func check_native_env {
    import os
    # Fetch natively from the underlying OS environment.
    python_key = os.environ.get("API_KEY")
    return python_key;
}
```

## Next

- [ORCH Includes](../Orch Includes.md)
- [Global Memory](../ORCH MEMORY.md)
