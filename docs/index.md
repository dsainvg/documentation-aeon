---
title: ORCH Agent Graph Orchestration Language
summary: Start here for the ORCH and AEON DSL documentation.
owner: Durga Sai
tags:
  - overview
  - orch
---

# ORCH Agent Graph Orchestration Language

ORCH is a domain-specific language for building and orchestrating systems made up of multiple intelligent agents. You write agents, give them tasks and memory, and use a central `Route` block to control which agent runs when.

Programs in ORCH are structured as a **graph of agents**. Each agent is an independent unit with its own private state and task logic. A single orchestrator file ties them all together, defining which agents exist and how execution flows between them.

## Features of the ORCH System

ORCH is not just another agent-chaining framework; it is a purpose-built Domain-Specific Language integrated closely with a Python execution engine (`orch-lib`). The combination of this domain-specific grammar and robust routing runtime yields several standout features:

### 1. Centrally Controlled Execution Automation

Unlike implicit state-machine or message-bus setups where agents call each other, ORCH centralizes the orchestrator flow.

- At the **Graph** level, the `Route` block decides which node or agent operates.
- At the **Agent** level, the `Route` block restricts agent scope to simple execution of tasks.
- **Result:** You can view a project and immediately trace its state evolution and path without reading deeply into execution details.

### 2. Distributed Compilation

The ORCH execution flow introduces a compiler pipeline composed of two layers:

- **Fast OCaml Build:** A statically typed `main.exe` executable guarantees the stability and structural soundness of the written DSL. It parses AST structures at high speed.
- **Generative Automation:** Instead of running the DSL line by line via interpreter, the architecture transpiles the tree into native Python bindings through `converter.py`, resulting in highly integrated and performant executable code.

### 3. Sandboxed Python Escapes (`Func` blocks)

You are not constrained to an obscure declarative language's limits. The `Func` block directly surfaces **unrestricted, native Python**.

If your agent needs to perform an API call or run a machine learning model, the logic lives securely inside a `Func {}`.

### 4. Simplified Memory Scoping

You do not need to deal with event queues to get memory working between agents.

- Need graph-wide visibility? Prefix with `Public`.
- Need isolated safety? Prefix with `Private`.

`orch-lib` translates this behind the scenes directly into structured contexts for every single agent and task.

### 5. Parallel/Multi-Agent Cloning Support

Through the simple array syntax `Include AgentB{5}`, ORCH will silently duplicate, register, and provision five totally disjoint instances of `AgentB`, handling all the memory initialization.

### 6. Built-in Math and Expression Evaluation Sub-language

ORCH's `Task` body behaves like basic Python expression assignments with complete support for conditional checks (`IF / ELSE`), logic bindings (`AND`, `OR`), and math operations (`+`, `-`, `/`, `*`), without needing the verbosity of a full language.

## Documentation Map

Read the guides in this order when you are learning the DSL:

1. [Installation](Installation.md)
2. [Downloads](Installation/Downloads.md)
3. [Usage and Structure](Usage and Structure.md)
4. [ORCH Files](ORCH FILES.md)
5. [AEON Files](AEON FILE.md)
6. [Library Files](LIB FILE.md)
7. [Routing](Routing.md)

