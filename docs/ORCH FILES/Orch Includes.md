# Orch Includes

Owner: Durga Sai
Verification: Verified
Tags: orch

# Feature Deep-Dive: Orchfile Includes (`.orch`)

In the Global Dispatcher context (`.orch` files), the `Include` keyword is structurally responsible for **instantiating agents into the execution graph**.

You use `Include` in an `.orch` file to bind `.aeon` agent definitions to the project runtime. If an agent is not explicitly included via an `Include` statement, it will not be created or executed, even if its definition file exists in the directory.

## Basic Includes

To pull a single instance of an agent into the runtime graph, use the keyword followed by the agent name.

```
# Include a single instance of an agent
# Assuming 'DataCollector.aeon' exists in the folder
Include DataCollector
```

Once included, the `DataCollector` can be targeted by the Global `Route` block.

## Instantiating Parallel Agent Clones

A uniquely powerful feature of the ORCH engine is its ability to instantly clone agent configurations to create multiple parallel processors.
You can spin up `N` identical agents that share the same `.aeon` instructions but maintain their own completely isolated memory scopes.

You do this by adding bracketed instantiation sizes `{N}`.

```
# Automatically create 5 separate instances of ProcessingAgent
Include ProcessingAgent{5}
```

*Behind the scenes, `orch-lib` handles provisioning 5 parallel instances and registering them dynamically.*

# Environment Variables (`.env`)

The ORCH compiler contains a natively integrated pipeline specifically to load environmental secrets safely directly into the running graph.

```python
# Automatically load all variables from `.env` directly into Global Graph Memory
Include env
```

[Environment (.env)](Orch Includes/Environment ( env).md)