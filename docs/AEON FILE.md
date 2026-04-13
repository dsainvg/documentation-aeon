---
title: AEON Files
summary: Define an agent's memory, tasks, Python functions, and internal route rules.
owner: Durga Sai
tags:
  - aeon
  - agents
---

# AEON Files

An `.aeon` file defines the behavior of an agent.

Each agent:

- stores some data.
- performs tasks.
- shares results with other agents.

## Basic Structure

Every agent file follows this structure:

```orch
Include Library

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

This section explains the structure of an agent using the **EmergencyAgent.aeon** file as an example.

### 1. Include (Optional)

You can include Python libraries at the top:

```orch
Include time
Include datetime
```

These can be used inside tasks.

### 2. Variables (Private & Public)

All variables are defined inside the `Private` block.

```orch
Private {
    int count
    string status = "idle"
    Public int result
}
```

- `Private` -> only this agent can use.
- `Public` -> shared with other agents.

### 3. Tasks (Core Logic)

Tasks define what the agent does.

```orch
Task process {
    result = count * 2
}
```

You can also use conditions:

```orch
Task check {
    IF count > 10 {
        result = 1
    } ELSE {
        result = 0
    }
}
```

### 4. Calling Python Logic from Tasks

Tasks remain DSL-focused. Put Python logic inside a `Func` block and call it from a task:

```orch
Func format_report {
    message = f"Result: {Private.result}"
    return message
}

Task report {
    report_message = format_report()
}
```

See [Library Functions](LIB%20FILE/Functions.md) for reusable Python-backed functions.

### 5. Route Block (Execution Flow)

The `Route` block controls which task runs.

```orch
Route {
    on_start : process
    count > 10 : check
    on_end : report
}
```

- `on_start` -> runs first.
- conditions -> decide next tasks.
- `on_end` -> runs at the end.

### 6. Complete Example

```orch
Include time

Private {
    int count = 5
    Public int result = 0
}

Func build_message {
    message = f"Final result: {Private.result}"
    return message
}

Task process {
    result = count * 2
}

Task report {
    message = build_message()
    print(message)
}

Route {
    on_start : process
    on_end : report
}
```

## Understanding the Agent Structure

- Variables -> what information the agent keeps track of.
- Tasks -> the actions the agent performs.
- Route -> decides when each action should run.

Together, this helps the agent work step by step and interact smoothly with other agents in the system.

## In This Section

- [Includes](AEON%20FILE/AEON%20Includes.md)
- [Agent Memory](AEON%20FILE/AEON%20Memory.md)
- [Tasks](AEON%20FILE/TASKS.md)
