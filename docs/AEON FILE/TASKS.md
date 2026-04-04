# TASKS

Owner: Durga Sai
Verification: Verified
Tags: aeon

# Feature Deep-Dive: Tasks

A `Task` block is where an agent mutates state. Think of `Task`s as the distinct “actions” an agent knows how to perform. However, **Tasks are entirely passive**—they don’t choose when to run. Only the agent’s `Route` block decides which Task fires.

## The Mathematics Sub-Language

To ensure security and keep state manipulation clean, Tasks do not run arbitrary Python. They run inside ORCH’s constrained expression-based sub-language.

Operations supported in a Task body:
- **Variable Assignments:** E.g., `score = score + 1;`
- **Conditional Branches:** `IF { ... } ELSE { ... }`
- **Logic Statements:** `AND`, `OR`
- **Mathematical Operators:** `<`, `>`, `<=`, `>=`, `==`, `!=`, `+`, `-`, `/`, `*`

## Example

```
Task evaluate_data {
    # Basic math and assignment
    confidence = confidence * 0.95;

    # Conditional checks
    IF error_rate > 5.0 {
        # Inter-agent public mutation
        Public.status = "failure";
    } ELSE {
        # Invoking an internal Func block or library
        Public.status = format_success_msg(confidence);
    }
}
```

## Characteristics

- **Strict Logic Constraint:** By restricting exactly what a Task can do, ORCH keeps state mutations clearly defined without getting bogged down in boilerplate API calls or complex logic nested at the wrong layer.
- **Delegation:** When a Task finds something too complex to calculate mathematically, it pushes that calculation to a `Func` block using `CALL`.