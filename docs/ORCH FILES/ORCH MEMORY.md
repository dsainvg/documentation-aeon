# ORCH MEMORY

Owner: Durga Sai
Verification: Verified
Tags: orch

# Feature Deep-Dive: Global Memory (`.orch`)

Memory handling inside the Global Dispatcher (`.orch` file) establishes overarching state that is inherently **public** to the entire project.

The available variable types in ORCH are: `int`, `float`, `char`, `string`, `list`, `tuple`.

## How to Define Global Memory

Global memory is defined freely at the top level of the `.orch` file (they are not enclosed within any `Private` or functional block). You simply declare a type and a variable name.

```
Include ProcessingAgent

# Defining global memory
int totalRounds = 10
string currentMode = "competitive"
```

## How to Use Global Memory in `.orch` Files

Within the `.orch` file itself, these variables are primarily used to direct the Global `Route` block. They act as the state conditions determining which Agent gets to run next.

```
Route {
   # Using global variables natively without prefixes in the orchestrator
   totalRounds > 0 : ProcessingAgent
}
```

## How to Use Global Memory in `.aeon` Files

Because any variable defined in the `.orch` file is implicitly placed into the **Graph/Global Memory**, they are universally accessible to all `.aeon` agents connected to the graph.

Inside any agent’s `Task` blocks, you can securely access these variables by using the `Public` accessor prefix.

```
Task evaluate_mode {
    # Accessing 'currentMode' globally defined in the .orch file
    IF Public.currentMode == "competitive" {
        # Perform action
        Public.totalRounds = Public.totalRounds - 1
    }
}
```

Global memory variables act as the system-wide static glue binding agent logic. They track the overarching progress, whereas agent-specific logic states belong strictly nested within the agents themselves.