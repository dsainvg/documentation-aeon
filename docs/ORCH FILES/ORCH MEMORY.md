---
title: Global Memory
summary: Define and access graph-wide memory from `.orch` and `.aeon` files.
owner: Durga Sai
verification: Verified
tags:
  - orch
  - memory
---

# Global Memory

Memory handling inside the Global Dispatcher (`.orch` file) establishes overarching state that is inherently **public** to the entire project.

The available variable types in ORCH are `int`, `float`, `char`, `string`, `list`, and `tuple`.

## How to Define Global Memory

Global memory is defined freely at the top level of the `.orch` file. Variables are not enclosed within any `Private` or functional block. You simply declare a type and a variable name.

```orch
Include ProcessingAgent

# Defining global memory.
int totalRounds = 10
string currentMode = "competitive"
```

## How to Use Global Memory in `.orch` Files

Within the `.orch` file itself, these variables are primarily used to direct the global `Route` block. They act as the state conditions determining which agent gets to run next.

```orch
Route {
   # Use global variables natively without prefixes in the orchestrator.
   totalRounds > 0 : ProcessingAgent
}
```

## How to Use Global Memory in `.aeon` Files

Because any variable defined in the `.orch` file is implicitly placed into **Graph/Global Memory**, it is universally accessible to all `.aeon` agents connected to the graph.

Inside any agent's `Task` blocks, you can securely access these variables by using the `Public` accessor prefix.

```orch
Task evaluate_mode {
    # Access `currentMode` from the `.orch` file's global memory.
    IF Public.currentMode == "competitive" {
        Public.totalRounds = Public.totalRounds - 1
    }
}
```

Global memory variables act as the system-wide glue binding agent logic. They track the overarching progress, whereas agent-specific logic states belong strictly nested within the agents themselves.

## Next

- [AEON Files](../AEON%20FILE.md)
- [Routing](../Routing.md)
