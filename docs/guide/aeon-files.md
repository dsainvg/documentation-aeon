---
summary: Define one agent with imports, state, tasks, and a local Route block.
---

# AEON Files

An `.aeon` file defines a single agent. It describes:

- the data the agent stores
- the tasks the agent can perform
- the order in which those tasks run

Each agent is a self-contained unit with its own local logic.

## Basic structure

```text
Include <python_library>

Private {
    // variables
}

Task <task_name> {
    // logic
}

Route {
    // execution flow
}
```

## Include Python libraries

You can import Python libraries at the top of the file:

```text
Include time
Include datetime
```

These libraries can then be used inside tasks.

## Declare variables

State is stored inside the `Private` block.

```text
Private {
    int count;
    string status = "idle";
    Public int result;
}
```

- `Private` values are only visible inside the current agent.
- `Public` values can be shared with other agents.

!!! tip
    Keep only the values that truly need to be shared as `Public`. Most agent state should stay private.

## Write tasks

Tasks are the executable units of logic in the file.

```text
Task process {
    result = count * 2
}
```

Tasks can also contain conditionals:

```text
Task check {
    IF count > 10 {
        result = 1
    } ELSE {
        result = 0
    }
}
```

## Use Python inside tasks

When a Python library has been included, you can call it directly:

```text
Task report {
    log("Result:", result)
    time.sleep(1)
}
```

This is useful for timers, formatting, external helpers, or small utility behavior.

## Control local flow

Each agent has its own `Route` block that decides which task runs and when.

```text
Route {
    on_start : process
    count > 10 : check
    on_end : report
}
```

- `on_start` runs first.
- Conditions can trigger follow-up tasks.
- `on_end` runs at the end of the agent's flow.

## Complete example

```text
Include time

Private {
    int count = 5
    Public int result = 0
}

Task process {
    result = count * 2
}

Task report {
    log("Final result:", result)
    time.sleep(1)
}

Route {
    on_start : process
    on_end : report
}
```

## Best practices

- Give tasks names that describe intent, not implementation details.
- Keep the `Private` block easy to scan.
- Use the route block to show the task lifecycle clearly instead of hiding flow inside large tasks.
