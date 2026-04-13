---
title: Functions
summary: Use `Func` blocks as Python escape hatches for reusable and complex behavior.
owner: Durga Sai
verification: Verified
tags:
  - library
  - functions
  - aeon
---

# Functions

While ORCH uses a custom syntax sub-language for mathematical assignments inside `Task` blocks, multi-agent systems routinely need to call APIs, run machine learning inference, interact with databases, or parse complex text.

The `Func` block is the escape hatch: **the body of a `Func` block is unrestricted Python**.

## Defining a Func

A `Func` lets you write standard Python exactly where you need computational payload without cluttering the declarative nature of the agent's routing structure.

The only rule is that a `Func` must conclude by returning a variable to pass back to the DSL environment.

`Func` declarations are named forms (`Func my_function { ... }`). Anonymous `Func { ... }` forms are not supported.

### Syntax Example

```orch
Func validate_database {
    # Pure Python is accepted here natively.
    import sqlite3
    import pandas as pd

    # You can access agent memory natively by reading the mapped objects.
    threshold = Private.error_threshold

    try:
        conn = sqlite3.connect('local.db')
        data = pd.read_sql("SELECT * FROM metrics", conn)
        conn.close()

        if len(data) > threshold:
            result_code = 1
        else:
            result_code = 0
    except Exception as e:
        result_code = -1

    # The block must export a returned variable to hand back to the task.
    return result_code
}
```

## How to Use a Func

Invoke a `Func` from within a `Task` block by calling it directly.

```orch
Task handle_db {
    # Call the Python escape hatch logic.
    db_status = validate_database()

    IF db_status == 1 {
        alert_flag = true
    }
}
```

`Func` blocks can live in `.aeon` files or reusable `.lib` files. In either case, end the block with `return <value>`.

## Numeric Literals

Numeric literals in ORCH expressions (including those used to configure tasks that call `Func` blocks) support underscores for readability. The parser automatically normalizes underscores during tokenization:

```orch
int max_users = 1_000_000
int threshold = 5_000
```

These are equivalent to `1000000` and `5000` respectively. Underscore normalization is handled consistently across all numeric parsing paths.

## Func Body Parsing

`Func` blocks accept unrestricted Python. The parser extracts the Python body using brace-count matching and properly handles braces within Python strings and comments. Python syntax errors inside the body will be caught by the Python runtime, not the DSL parser.

## Why It Works This Way

By isolating Python inside `Func` blocks and isolating mathematics or state mutation inside `Task` blocks, the system encourages developers to separate execution-heavy logic from standard agent orchestration logic. It combines the readability of a DSL with the wider Python ecosystem.

## Next

- [Tasks](../AEON%20FILE/TASKS.md)
- [Routing](../Routing.md)
