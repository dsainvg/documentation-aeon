---
title: ORCH Includes
summary: Include agents, clone agent instances, load environment variables, and use mechanical operations on cloned agents from `.orch` files.
owner: Durga Sai
verification: Verified
tags:
  - orch
  - includes
---

# ORCH Includes

In the Global Dispatcher context (`.orch` files), the `Include` keyword is structurally responsible for **instantiating agents into the execution graph**.

You use `Include` in an `.orch` file to bind `.aeon` agent definitions to the project runtime. If an agent is not explicitly included via an `Include` statement, it will not be created or executed, even if its definition file exists in the directory.

## Basic Includes

To pull a single instance of an agent into the runtime graph, use the keyword followed by the agent name.

```orch
# Include a single instance of an agent.
# Assumes `DataCollector.aeon` exists in the folder.
Include DataCollector
```

Once included, `DataCollector` can be targeted by the global `Route` block.

## Instantiating Parallel Agent Clones

A powerful feature of the ORCH engine is its ability to instantly clone agent configurations to create multiple parallel processors. You can spin up `N` identical agents that share the same `.aeon` instructions but maintain their own completely isolated memory scopes.

You do this by adding bracketed instantiation sizes, such as `{N}`.

```orch
# Automatically create five separate instances of ProcessingAgent.
Include ProcessingAgent {5}
```

Behind the scenes, `orch-lib` handles provisioning five parallel instances and registering them dynamically.

## Clones Library

When you create parallel cloned agents using `Include AgentClass {N}`, the `clones` library provides mechanical operations to query and aggregate their states without manual Python loops.

```orch
Include clones
Include WorkerAgent {5}

Task count_workers {
    idle_workers = clones.count(WorkerAgent, "status", "idle")
    total_processed = clones.sum(WorkerAgent, "items_done")
}
```

The library offers strict, deterministic functions for aggregation, selection, and introspection across cloned agent arrays.

## Environment Variables (`.env`)

The ORCH compiler contains a natively integrated pipeline to load environmental secrets safely into the running graph.

```orch
# Automatically load all variables from `.env` into global graph memory.
Include env
```

## Next

- [Clones Library](Orch Includes/Clones ( clones).md)
- [Environment Variables](Orch Includes/Environment ( env).md)
- [Global Memory](ORCH%20MEMORY.md)
