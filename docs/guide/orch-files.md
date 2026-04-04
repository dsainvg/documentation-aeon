---
summary: Wire agents together, declare global state, and drive execution with one Route block.
---

# ORCH Files

An `.orch` file is the entry point for an Aeon workflow. It tells the runtime:

- which agents exist
- which global values matter
- which agent should run when a condition becomes true

If `.aeon` files describe behavior, the `.orch` file describes coordination.

## Structure

Most orchestrator files follow this order:

```text
Include AgentName {count}

int globalValue = 0

Route {
    condition : AgentName {instance}
}
```

## Include agents

Use `Include` to load the agents that participate in the workflow.

```text
Include IntersectionAgent {4}
Include ZoneAgent {3}
Include CongestionAgent {1}
Include EmergencyAgent {1}
Include ReportAgent {1}
```

The number in braces represents how many instances of that agent you want available.

!!! note
    Use multiple instances when the same agent type needs to handle work in parallel or in separate regions of the workflow.

## Declare global variables

Global variables are shared coordination state for the orchestrator.

```text
int trafficStage = 0
int responseMode = 0
```

These values are commonly used inside the `Route` block to decide what happens next.

## Route execution

The `Route` block is the core of the file. Each rule follows this shape:

```text
condition : AgentName {instance}
```

Conditions are evaluated from top to bottom.

```text
Route {
    trafficStage == 0 : IntersectionAgent {1}
    trafficStage == 0 : IntersectionAgent {2}
    trafficStage == 0 : IntersectionAgent {3}
    trafficStage == 0 : IntersectionAgent {4}

    trafficStage == 1 : ZoneAgent {1}
    trafficStage == 1 : ZoneAgent {2}
    trafficStage == 1 : ZoneAgent {3}

    trafficStage == 2 AND responseMode == 2 : EmergencyAgent {1}
    trafficStage == 2 AND responseMode == 1 : CongestionAgent {1}

    trafficStage == 3 OR trafficStage == 2 AND responseMode == 0 : ReportAgent {1}
}
```

### Route rules to remember

- `AND` combines conditions that must all be true.
- `OR` allows multiple paths to activate the same agent.
- Ordering matters when several rules can match at the same time.

## Lifecycle hooks

The route block also supports two special hooks:

```text
Route {
    on_start : SetupAgent {1}
    stage == 1 : WorkerAgent {1}
    on_end : ReportAgent {1}
}
```

- `on_start` runs once when execution begins.
- `on_end` runs once when the workflow is finishing.

These hooks are useful for setup, reporting, cleanup, and final summaries.

## Full example

```text
Include IntersectionAgent {4}
Include EmergencyAgent {1}
Include ReportAgent {1}

int trafficStage = 0
int responseMode = 0

Route {
    on_start : IntersectionAgent {1}

    trafficStage == 0 : IntersectionAgent {2}
    trafficStage == 0 : IntersectionAgent {3}
    trafficStage == 0 : IntersectionAgent {4}

    trafficStage == 2 AND responseMode == 2 : EmergencyAgent {1}

    on_end : ReportAgent {1}
}
```

## Best practices

- Keep global variables small and meaningful.
- Group related route rules together so the flow reads like a story.
- Use `on_start` and `on_end` for lifecycle concerns instead of mixing them into normal condition rules.
