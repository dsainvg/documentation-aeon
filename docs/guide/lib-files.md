---
summary: Keep reusable functions in one place and call them from AEON agents.
---

# LIB Files

A `.lib` file stores reusable helper functions. It is the right place for logic that:

- would otherwise be duplicated across agents
- is easier to express as a reusable function
- should stay separate from agent-specific behavior

## Basic structure

A library file contains function definitions:

```text
Func functionName {
    # Python-style logic
    return result;
}
```

Each function should do one focused job and return a value clearly.

## Example

```text
Func add {
    result = a + b
    return result;
}

Func multiply {
    result = a * b
    return result;
}
```

## How functions are used

First, include the library in an agent:

```text
Include math
```

Then call the function inside a task:

```text
Task compute {
    result = add(a, b)
}
```

## Good patterns for `.lib` files

- Put shared calculations in libraries.
- Keep side effects small and predictable.
- Return a value explicitly so the calling task is easy to understand.

!!! note
    Libraries should support your agents, not replace them. Workflow logic still belongs in `.orch` and `.aeon` files.

## Best practices

- Keep names descriptive, such as `calculatePriority` or `formatReport`.
- Group related helper functions in the same file.
- Avoid duplicating the same helper across multiple libraries.
