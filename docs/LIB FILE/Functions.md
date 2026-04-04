# Functions

Owner: Durga Sai
Verification: Verified
Tags: aeon

# Funcs

While ORCH utilizes a custom syntactical sub-language for mathematical assignments inside `Task` blocks, Multi-Agent systems routinely require calling APIs, performing heavy machine learning inference, interacting with databases, or parsing complex text.

The `Func` block is the ultimate escape hatch: **The body of a Func block is unrestricted Python.**

## Defining a Func

A `Func` lets you write standard Python precisely where you need computational payload without cluttering the declarative nature of the agent’s routing structure.

The only rule is that a `Func` must conclude by returning a variable to pass back to the DSL environment.

### Syntax Example

```
Func validate_database {
    # Pure python is accepted here natively
    import sqlite3
    import pandas as pd

    # You can access agent memory natively by reading the mapped objects
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

    # The block must export a returned variable to hand back to the task
    return result_code;
}
```

## How to use a Func

You invoke a `Func` from within a `Task` block utilizing the `CALL` operator.

```
Task handle_db {
    # Calling the Python escape hatch logic
    db_status = validate_database();

    IF db_status == 1 {
        alert_flag = true;
    }
}
```

## Why it works this way

By isolating Python inside `Func` blocks and isolating Mathematics/State inside `Task` blocks, the system inherently forces developers to separate execution heavy-lifting from standard agent orchestration logic. It combines the readability of a DSL with the limitless ecosystem of the Python language.