---
title: Clones Library
summary: Mechanical multi-agent operations for querying and aggregating cloned agent states
owner: Durga Sai
verification: Verified
tags:
  - orch
  - clones
  - agents
---

# Clones Library

## Overview

When you instantiate multiple identical agents using `Include AgentClass {N}`, the ORCH engine creates N independent clones with isolated memory scopes. The `clones` library provides a unified, declarative interface to query and aggregate state across these parallel agent instances without requiring manual Python loops.

By declaring the reserved phrase `Include clones` in your global orchestrator (`.orch`), you gain access to mechanical operations for counting, summing, searching, and routing across cloned agent arrays.

```orch
Include clones
Include WorkerAgent {5}
```

## API Reference

### Aggregation Functions

#### `clones.count(AgentClass, "variable", target_value)` → `int`

Returns the integer count of how many clones match a specific state.

```orch
Task evaluate_fleet {
    # Count how many workers have status "idle"
    idle_count = clones.count(WorkerAgent, "status", "idle")

    IF idle_count > 0 {
        Public.workers_available = 1
    }
}
```

**Parameters:**
- `AgentClass`: The class name of the cloned agents (e.g., `WorkerAgent`)
- `"variable"`: The agent memory variable to inspect (must be a string literal)
- `target_value`: The value to match (can be a number, string, or boolean)

**Returns:** Integer count of matching clones

---

#### `clones.sum(AgentClass, "variable")` → `number`

Sums a numerical variable across all clones.

```orch
Task calculate_totals {
    # Sum the processed_items variable across all workers
    total_items = clones.sum(WorkerAgent, "processed_items")

    Public.cumulative_output = total_items
}
```

**Parameters:**
- `AgentClass`: The class name of the cloned agents
- `"variable"`: The numerical agent memory variable to sum

**Returns:** Numeric sum of all clone values

---

#### `clones.max_index(AgentClass, "variable")` → `int`

Returns the `{i}` index (1-based) of the clone with the highest value.

```orch
Task find_top_performer {
    # Find which worker processed the most items
    top_worker = clones.max_index(WorkerAgent, "processed_items")

    IF top_worker != -1 {
        Public.promote_target = top_worker
    }
}
```

**Parameters:**
- `AgentClass`: The class name of the cloned agents
- `"variable"`: The numerical variable to compare

**Returns:** Index of the max clone, or -1 if no clones exist

---

#### `clones.min_index(AgentClass, "variable")` → `int`

Returns the `{i}` index (1-based) of the clone with the lowest value.

```orch
Task find_underperformer {
    # Find which worker has processed the fewest items
    slowest_worker = clones.min_index(WorkerAgent, "processed_items")
}
```

**Parameters:**
- `AgentClass`: The class name of the cloned agents
- `"variable"`: The numerical variable to compare

**Returns:** Index of the min clone, or -1 if no clones exist

---

### Selection Functions

#### `clones.find_first(AgentClass, "variable", target_value)` → `int`
#### `find_all(AgentClass, "variable", target_value)` → `list of int`

Returns a list of all clone indices matching a condition. Useful for batch processing or comprehensive tracking.

```orch
Task process_all_idle {
    # Get all idle workers as a list of indices
    idle_list = clones.find_all(WorkerAgent, "status", "idle")

    # Batch operation on all matching workers
    Public.idle_workers = idle_list
}
```

**Parameters:**
- `AgentClass`: The class name of the cloned agents
- `"variable"`: The agent memory variable to inspect
- `target_value`: The value to match

**Returns:** List of all matching clone indices (empty list if none found)

---

Returns the index `{i}` (1-based) of the first clone matching a condition. Useful for routing to the first available worker.

```orch
Task assign_work {
    # Find the first worker with status "idle"
    free_agent_id = clones.find_first(WorkerAgent, "status", "idle")

    IF free_agent_id != -1 {
        Public.next_assignment_target = free_agent_id
    } ELSE {
        Public.system_overloaded = 1
    }
}
```

**Parameters:**
- `AgentClass`: The class name of the cloned agents
- `"variable"`: The agent memory variable to inspect
- `target_value`: The value to match

**Returns:** Index of the first matching clone, or -1 if none are found

---

### Introspection Functions

#### `my_index(agent_id)` → `int`

Extracts the numeric index from an agent's identity string. Useful when an agent needs to know its own instance number during execution.

```orch
Task identify_self {
    # Within an agent, pass its own agent identifier
    my_id = clones.my_index(Public.agent_id)

    IF my_id == 0 {
        # This is the leader (first clone); perform leader-only logic
        Public.is_leader = 1
    }
}
```

**Parameters:**
- `agent_id`: The agent's identifier string (typically provided by the runtime)

**Returns:** Numeric index of the agent, or -1 if the format is invalid

---

#### `clones.size(AgentClass)` → `int`

Returns the total number of clones initialized for a given agent class.

```orch
Task check_fleet_size {
    # Query the total number of worker instances
    total_workers = clones.size(WorkerAgent)

    Public.fleet_capacity = total_workers
}
```

**Parameters:**
- `AgentClass`: The class name of the cloned agents

**Returns:** Total number of initialized clones

---

## Complete Example

```orch

Returns the index of the first clone matching a condition. Useful for routing to the first available worker.

int total_work = 0
Task assign_work {
    # Find the first worker with status "idle"
    free_agent_id = clones.find_first(WorkerAgent, "status", "idle")

    IF free_agent_id != -1 {
        Public.next_assignment_target = free_agent_id
    } ELSE {
        Public.system_overloaded = 1
    }

Task InitLeader {
    leader_id = 0
    Public.leader_elected = leader_id
}

Task AssignWork {
    # Count how many workers are available
**Returns:** Index of the first matching clone, or -1 if none are found

    # Sum all completed work
    total_work = clones.sum(WorkerAgent, "work_completed")
#### `find_all(AgentClass, "variable", target_value)` → `list of int`

Returns a list of all clone indices matching a condition. Useful for batch processing or comprehensive tracking.
    # Find the first idle worker
    next_worker = clones.find_first(WorkerAgent, "status", "idle")
Task process_all_idle {
    # Get all idle workers as a list of indices
    idle_list = clones.find_all(WorkerAgent, "status", "idle")

    # Batch operation on all matching workers
    Public.idle_workers = idle_list
Task Finalize {
    final_count = clones.size(WorkerAgent)
    total_output = clones.sum(WorkerAgent, "work_completed")
}
```

## Design Principles

**Returns:** List of all matching clone indices (empty list if none found)

- **No Custom Logic:** All operations are deterministic aggregations and searches, not domain-specific calculations.
- **No LLM Wrappers:** The library does not include AI/ML functionality; that belongs in `Func` blocks.
- **0-based Indexing:** Clone indices start at 0 (index 0 is the first clone).
- **Declarative DSL:** Query operations remain inside `Task` blocks, keeping your agent routing logic clean and readable.
- **Memory Safe:** Accessing clones through this API is memory-safe and respects isolation boundaries between agent instances.

## Next

- [Environment Variables](Environment%20(%20env).md)
- [ORCH Includes](../Orch%20Includes.md)
- [Global Memory](../ORCH%20MEMORY.md)
