# AEON Includes

Owner: Durga Sai
Verification: Verified
Tags: aeon

# Feature Deep-Dive: Agent Includes (`.aeon`)

Inside the Agent Definition context (`.aeon` files), the `Include` keyword serves a fundamentally different purpose compared to the global orchestrator.

In an `.aeon` file, `Include` is used to import reusable modules, shared functions, or native Python libraries directly into the agent’s internal logic.

## Resolution Order

When you use `Include my_module` inside an `.aeon` file, the transpiler follows a specific fallback order to resolve the import:

1. **Local `.lib` Files**: First, it checks if a file named `my_module.lib` exists within your project directory.
2. **Inbuilt Libraries**: Second, it checks against ORCH’s default native library system (Note: There are currently no inbuilt libraries available).
3. **Python Libraries & Scripts**: Finally, if both checks fail, it assumes `my_module` is either an installed Python package or an external `.py` script and uses the Python runtime to import it.

***Important Constraint:** You cannot use relative imports pathing for Python scripts yet (e.g., `Include ../utils`), you can only provide the absolute module name.*

## Usage Examples

Below are clean examples demonstrating how the compiler resolves different scenarios based on the fallback order. Unlike the orchestrator, you **cannot** instantiate arrays of objects `{N}` here.

### 1. Including a Local `.lib` File

If you have a file named `math_logic.lib` in your folder, this pulls its shared functional logic cleanly into the agent.

```
Include math_logic
```

### 2. Including Native Python Libraries

If no local `.lib` file or ORCH inbuilt module matches, the system naturally delegates to Python’s execution space. This is how you quickly bring powerful ecosystem libraries into your agent’s `Func` scopes.

```
# Automatically resolved as standard Python libraries!
Include math
Include json
```

### 3. Including External Python Scripts

Identical to a library, you can seamlessly import your own local `.py` scripts (for example, `utils.py`). Just remember, relative paths (e.g., `../utils`) are strictly forbidden.

```
# Resolves the external 'utils.py' script located in your root environment
Include utils
```

By supporting library includes at the agent level natively across all three fallback contexts, agents are empowered to freely share complex algorithmic logic securely without redundantly rewriting functional blocks.