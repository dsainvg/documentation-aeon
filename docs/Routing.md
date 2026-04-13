---
title: Routing
summary: Control graph-level agent execution and agent-level task execution with `Route` blocks.
owner: Durga Sai
verification: Verified
tags:
  - routing
  - design
---

# Routing

The `Route` block represents the central authority of any ORCH project. In ORCH, agents and tasks **never** trigger each other directly. Instead, all transitions and control flows are centralized inside `Route` blocks.

`Route` blocks are evaluated top-down each pass. Any rule whose condition evaluates to `true` can run in that pass.

There are exactly two variations of the `Route` block: **Global Routing** and **Agent Routing**.

## 1. Global Routing (in `.orch`)

Located in the Global Dispatcher, this route block decides which agent gets to run.

### Reserved Keywords

- `on_start`: Optional. Triggered exactly once when the program officially begins.
- `on_end`: Optional. Triggered when the graph concludes.

### Example

```orch
int errors = 0

Route {
    # Rules are evaluated top-down each pass.
    errors > 5 : AlertAgent
    on_start : InitAgent
}
```

## 2. Routing to Specific Clones (`{i}`)

When dealing with an array of cloned agents initialized in your global orchestrator, such as `Include WorkerAgent{3}`, you can explicitly route to a specific instance of that agent class by using the `{i}` syntax.

Clone indices are **1-based** in route targets (`{1}`, `{2}`, ...).

```orch
# Correct targeted deterministic routing for clones.
Route {
    condition_A : WorkerAgent{1}
    condition_B : WorkerAgent{2}
}
```

### Warning: Non-Deterministic Execution Order

A critical detail when designing routes is ensuring conditions are mutually exclusive if exact execution order matters.

If you map the exact same trigger condition to multiple different targets inside the same `Route` block, or if you map a condition to an unindexed class of initialized clones, the ORCH compiler does not guarantee which one will execute first. Order will be variable and non-deterministic on every run.

Avoid duplicate triggers unless the sequence of execution does not matter to your logic.

## 3. Agent Routing (in `.aeon`)

Located inside every Agent Definition, this route block decides which internal task is executed when the global route gives control to the agent.

### Example

```orch
Route {
    health < 30 : heal
    on_start : fight
}
```

## Related

- [ORCH Files](ORCH%20FILES.md)
- [AEON Files](AEON%20FILE.md)
- [Tasks](AEON%20FILE/TASKS.md)
