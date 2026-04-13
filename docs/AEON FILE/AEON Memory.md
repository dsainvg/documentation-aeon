---
title: AEON Memory
summary: Declare private agent memory and public graph-exposed agent state.
owner: Durga Sai
tags:
  - aeon
  - memory
---

# AEON Memory

Within an Agent Definition (`.aeon` file), memory requires explicit scoping constraints. All variables for an agent must be declared tightly within its `Private { ... }` block to instruct the runtime how exposed the internal data is allowed to be.

The available variable types in ORCH are `int`, `float`, `char`, `string`, `list`, and `tuple`.

## Defining Memory Scopes

### 1. `Private` (Explicit Constraint)

Variables explicitly prefixed with `Private` remain strictly protected from the rest of the graph. No other agent can access them.

```orch
Private {
    Private int internal_counter = 0
}
```

### 2. Not Specifying Anything (Implicit Private)

If you declare variables with normal types without using the `Public` or `Private` prefix, they default to `Private`. This is the standard shorthand for writing agent structures.

```orch
Private {
    # Implicitly private. Same behavior as `Private string key = "abc"`.
    string key = "abc"
}
```

### 3. `Public` (Graph-Exposed)

By prefixing a declaration with the `Public` keyword, the system manages the variable structure inside the agent's memory layout and pushes an accessible alias pointing directly to the **Graph Level Memory**, broadcasting it to the rest of the application.

```orch
Private {
    # Any other agent in the system can read this variable.
    Public float satisfaction = 1.0
}
```

## How to Use Your Own Memory

Inside your `Task` blocks, you manipulate these variables dynamically:

- **Using Private State:** You can call `Private.internal_counter` explicitly, or just `internal_counter` because it defaults to the local agent tracking scope.
- **Using Public State:** You can call `Public.satisfaction`.

## How to Access Other Agents' Variables

If another agent, such as `DataCollector.aeon`, declares `Public list raw_data = []`, it puts that data into central graph-level memory under that specific agent's namespace.

To read and use that variable inside this agent, query it from the global pool using the `Public` accessor followed by the target agent's name.

Inside Agent B's `Task` block:

```orch
Task analyze {
    # Fetches `raw_data` exported publicly from the DataCollector agent.
    my_local_list = Public.DataCollector.raw_data

    # If DataCollector was cloned as an array, e.g. Include DataCollector{3},
    # specify the index of the clone.
    my_clone_list = Public.DataCollector[1].raw_data
}
```

## Next

- [Tasks](TASKS.md)
- [Routing](../Routing.md)
