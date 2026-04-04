---
summary: Learn how ORCH, AEON, and LIB files work together in one Aeon project.
---

# DSL Guide

Aeon projects are built from three file types that each do one job well:

| File type | Extension | Responsibility |
| --- | --- | --- |
| Orchestrator | `.orch` | Loads agents and decides how execution moves through the system |
| Agent | `.aeon` | Defines one agent's state, tasks, and local routing behavior |
| Library | `.lib` | Stores reusable helper functions that agents can call |

The design is easiest to understand if you think about it in layers:

1. A `.lib` file gives you reusable logic.
2. A `.aeon` file uses that logic to implement one agent.
3. A `.orch` file connects multiple agents into one workflow.

!!! tip
    Read the docs in that same order if you are new to the DSL. It builds the right mental model quickly.

## Project shape

A typical Aeon project might look like this:

```text
project/
|-- traffic.orch
|-- intersection.aeon
|-- emergency.aeon
`-- traffic.lib
```

Each file stays focused:

- The orchestrator chooses which agent runs.
- Each agent describes what it knows and what it can do.
- The shared library keeps repeated logic out of the agents.

## Small end-to-end example

```text
Include MonitorAgent {1}
Include ReportAgent {1}

int stage = 0

Route {
    on_start : MonitorAgent {1}
    stage == 1 : ReportAgent {1}
    on_end : ReportAgent {1}
}
```

This example shows the full control loop:

- Agents are loaded at the top.
- Global state is declared once.
- The `Route` block decides what runs at startup, during execution, and when the flow ends.

## What to read next

- Move to [ORCH Files](orch-files.md) to understand the global routing language.
- Move to [AEON Files](aeon-files.md) to define an agent's internal behavior.
- Move to [LIB Files](lib-files.md) to write reusable helper functions.
