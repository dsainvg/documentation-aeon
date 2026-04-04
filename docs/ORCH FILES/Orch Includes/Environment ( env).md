# Environment (.env)

Owner: Durga Sai
Verification: Verified
Tags: orch

## Sourcing Environment Variables

By declaring the specific reserved phrase `Include env` in your global orchestrator (`.orch`), the transpiler hooks directly to the backend to automatically load and parse a `.env` file from the runtime directory.

```
# Automatically load all variables from `.env` directly into Global Graph Memory
Include env
```

All key-value pairs established in the `.env` file are seamlessly unpacked and bundled into the overarching **Graph Memory** layer as explicitly public variables.

## 1. Example `.env` File

```
API_KEY=YOUR_SECRET_KEY
DB_HOST=localhost
```

## 2. Accessing From Inside an Agent (`Task` block)

Because the environment pairs map entirely into the graph’s public memory structure, any initialized agent can freely read those variables in their `Task` blocks by specifically reaching into the global scope using the `Public` accessor.

```
Task check_connection {
    # Natively fetches the variable loaded from the .env into Graph Memory
    current_key = Public.API_KEY;
}
```

## 3. Accessing From Python (`Func` block)

Because the ORCH compilation engine utilizes standard `dotenv` libraries under the hood during the script’s execution phase, `.env` variables are completely simultaneously injected straight into the operating system shell environment.

This means any pure Python script running within an agent’s `Func` escape hatch can use standard Python `os` modules to fetch them natively, completely sidestepping standard Graph Memory:

```
Func check_native_env {
    import os
    # Fetch natively from the underlying OS environment
    python_key = os.environ.get("API_KEY")
    return python_key;
}
```