---
title: ORCH Files
summary: Define the global dispatcher, graph memory, includes, and route rules for an ORCH project.
owner: Durga Sai
verification: Verified
tags:
  - orch
  - dispatcher
---

# ORCH Files

An `.orch` file defines a workflow using the DSL. It describes which agents are included, which graph-level variables exist, and how execution moves between agents.

You can think of it as the script that controls how different steps are executed.

## ORCH File Structure

An ORCH file follows a fixed structure:

### 1. Include Section

We first include all required files.

- Agent files are included using `Include AgentName`.
- Multiple instances can be created using `{n}`.

```orch
Include IntersectionAgent {4}
Include ReportAgent
```

This is where we load all agents that will be used in the system.

### 2. Global Variables

After including agents, we define global variables.

- These variables control the execution flow.
- Example variables: `trafficStage`, `responseMode`.

```orch
int trafficStage = 0
int responseMode = 0
```

They are mainly used inside the `Route` block for decision making.

### 3. Route Block

The `Route` block defines the execution logic.

- It decides which agent runs based on conditions.
- Each rule follows `condition : Agent {instance}`.
- Conditions are checked from top to bottom.

#### on_start and on_end

- `on_start : Agent` -> runs once at the beginning of execution.
- `on_end : Agent` -> runs once at the end of execution.

They are special rules inside the `Route` block used to:

- initialize the system with `on_start`.
- perform final tasks like reporting or cleanup with `on_end`.

This is the core part of the ORCH file where the entire system flow is controlled.

```orch
Route {
    on_start : SetupAgent
    trafficStage == 0 : IntersectionAgent {1}
    trafficStage == 1 : ZoneAgent {1}
    trafficStage == 1 : ZoneAgent {2}
    trafficStage == 2 AND responseMode == 2 : EmergencyAgent {1}
    on_end : LogAgent
}
```

## In This Section

- [Includes](ORCH FILES/Orch Includes.md)
- [Environment Variables](ORCH FILES/Orch Includes/Environment ( env).md)
- [Global Memory](ORCH FILES/ORCH MEMORY.md)
