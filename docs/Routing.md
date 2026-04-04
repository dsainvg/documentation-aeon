# Routing

Owner: Durga Sai
Verification: Verified
Tags: Design

# Feature Deep-Dive: Routing

The `Route` block represents the central authority of any ORCH project. In ORCH, agents and tasks **never** trigger each other directly. Instead, all transitions and control flows are centralized inside `Route` blocks.

`Route` blocks are evaluated top-down. The first condition that evaluates to `true` is chosen to execute next.

There are exactly two variations of the `Route` block: **Global Routing** and **Agent Routing**.

---

## 1. Global Routing (in `.orch`)

Located in the Global Dispatcher, this route block decides *which Agent* gets to run.

### Reserved Keywords

- `on_start`: (Optional) Triggered exactly once when the program officially begins.
- `on_end`: (Optional) Triggered when the graph concludes.

### Example

```
int errors = 0

Route {
    # The first condition to match will trigger the corresponding Agent
    errors > 5 : AlertAgent          # Triggers AlertAgent if critical error
    on_start : InitAgent             # Always kicks off here first
}
```

---

## 2. Routing to Specific Clones (`{i}`)

When dealing with an array of cloned agents initialized in your global orchestrator (e.g., `Include WorkerAgent{3}`), you can explicitly route to a specific instance of that agent class by using the zero-indexed `{i}` syntax.

```
# Correct targeted deterministic routing for clones
Route {
    condition_A : WorkerAgent{0}    # Triggers the first clone explicitly
    condition_B : WorkerAgent{1}    # Triggers the second clone explicitly
}
```

### Warning: Non-Deterministic Execution Order

A critical detail when designing routes is ensuring conditions are mutually exclusive if exact execution order matters.

If you map the **exact same trigger condition** to multiple different targets inside the exact same `Route` block (or if you map a condition to an unindexed class of initialized clones), the ORCH compiler does not guarantee which one will execute first. Order will be highly variable and non-deterministic on every run.

**Avoid duplicate triggers** unless the sequence of execution does not matter to your logic.

---

## 3. Agent Routing (in `.aeon`)

Located inside every Agent Definition, this route block decides *which internal Task* is executed when the global route gives control to the Agent.

### Example

```
Route {
    health < 30 : heal       # If low health, agent focuses on healing
    on_start : fight         # Otherwise, agent defaults to fighting
}
```