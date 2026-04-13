---
title: Library Files
summary: Define reusable Python-backed functions that `.aeon` agents can import.
owner: Durga Sai
tags:
  - library
  - functions
---

# Library Files

A `.lib` file defines reusable functions that can be used inside agent files.

It helps you:

- avoid repeating logic.
- write complex operations in Python.
- reuse functions across multiple agents.

## Example (`math.lib`)

```orch
Func add {
    result = a + b
    return result;
}

Func multiply {
    result = a * b
    return result;
}
```

## Explanation

- `Func` -> defines a function.
- The block body -> contains Python code.
- `return` -> specifies the output of the function.

## Using Library Functions in Agents

First, include the library in your agent file:

```orch
Include math
```

Then call the function inside a task:

```orch
Task compute {
    result = add(a, b)
}
```

## Key Points

- `.lib` files only contain functions.
- Functions use Python syntax.
- Functions must end with `return <variable>;`.
- Functions can be reused across multiple agents.

## Next

- [Functions](LIB%20FILE/Functions.md)
- [AEON Includes](AEON%20FILE/AEON%20Includes.md)
