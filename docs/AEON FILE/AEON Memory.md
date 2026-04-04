# AEON Memory

Owner: Durga Sai

# Feature Deep-Dive: Agent Sandbox Memory (`.aeon`)

Within an Agent Definition (`.aeon` file), memory requires explicit scoping constraints. All variables for an agent must be declared tightly within its `Private { ... }` block to instruct the runtime how exposed the internal data is allowed to be.

The available variable types in ORCH are: `int`, `float`, `char`, `string`, `list`, `tuple`.

## Defining Memory Scopes

### 1. `Private` (Explicit Constraint)

Variables explicitly prefixed with `Private` remain strictly protected from the rest of the graph. No other agent can access them.

```
Private {
    Private int internal_counter = 0;
}
```

### 2. Not Specifying Anything (Implicit Private)

If you declare variables with normal types *without* utilizing the `Public` or `Private` prefix, **it defaults to Private automatically**. This is the standard shorthand for writing agent structures.

```
Private {
    # Implicitly private. Identical behavior to 'Private string key = "abc";'
    string key = "abc";
}
```

### 3. `Public` (Graph-Exposed)

By prefixing a declaration with the `Public` keyword, the system manages the variable structure inside the agent’s memory layout, but deliberately pushes an accessible alias pointing directly to the **Graph Level Memory**, broadcasting it natively to the rest of the application.

```
Private {
    # Any other agent in the system can read this variable natively!
    Public float satisfaction = 1.0;
}
```

## How to Use Your Own Memory

Inside your `Task` blocks, you manipulate these variables dynamically:
- **Using Private State:** You can call `Private.internal_counter` explicitly, or just `internal_counter` inherently since it defaults to the local agent tracking scope.
- **Using Public State:** You can call `Public.satisfaction`.

## How to Access Other Agents’ Variables

If another agent (e.g., `DataCollector.aeon`) declares a `Public list raw_data = [];`, it puts that data into the central graph-level memory under that specific agent’s namespace.

To read and use that variable inside *this* agent, you query it from the global pool using the `Public` accessor **followed by the target Agent’s name**.

**Inside Agent B’s Task block:**

```
Task analyze {
    # Fetches 'raw_data' exported publicly from the DataCollector agent specifically
    my_local_list = Public.DataCollector.raw_data;

    # If DataCollector was cloned as an array (e.g. Include DataCollector{3})
    # You must specify the index of the clone!
    my_clone_list = Public.DataCollector[1].raw_data;
}
```