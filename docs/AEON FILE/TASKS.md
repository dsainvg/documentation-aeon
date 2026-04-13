---
title: Tasks
summary: Use `Task` blocks to mutate agent state with ORCH's constrained expression language.
owner: Durga Sai
verification: Verified
tags:
  - aeon
  - tasks
---

# Tasks

A `Task` block is where an agent mutates state. Think of tasks as the distinct actions an agent knows how to perform. However, **tasks are entirely passive**: they do not choose when to run. Only the agent's `Route` block decides which task fires.

## The Mathematics Sub-Language

To keep state manipulation secure and readable, tasks do not run arbitrary Python. They run inside ORCH's constrained expression-based sub-language.

Operations supported in a task body:

- **Variable Assignments:** For example, `score = score + 1`.
- **Conditional Branches:** `IF { ... } ELSE { ... }`.
- **Logic Statements:** `AND`, `OR`.
- **Mathematical Operators:** `<`, `>`, `<=`, `>=`, `==`, `!=`, `+`, `-`, `/`, `*`.

## Example

```orch
Task evaluate_data {
    # Basic math and assignment.
    confidence = confidence * 0.95

    # Conditional checks.
    IF error_rate > 5.0 {
        # Inter-agent public mutation.
        Public.status = "failure"
    } ELSE {
        # Invoking an internal Func block or library.
        Public.status = format_success_msg(confidence)
    }
}
```

## Characteristics

- **Strict Logic Constraint:** By restricting exactly what a task can do, ORCH keeps state mutations clearly defined without getting bogged down in boilerplate API calls or complex logic nested at the wrong layer.
- **Delegation:** When a task finds something too complex to calculate mathematically, it pushes that calculation to a `Func` block using a direct function call.

## Next

- [Library Functions](../LIB%20FILE/Functions.md)
- [Routing](../Routing.md)
