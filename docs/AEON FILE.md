# AEON FILE

Owner: Durga Sai
Tags: aeon

An `.aeon` file defines the behavior of an agent.

Each agent:

- stores some data
- performs tasks
- shares results with other agents

---

### Basic Structure

Every agent file follows this structure:

```
Include Library

Private {
    // variables
}

Task <task_name> {
    // logic
}

Route {
    // execution flow
}
```

---

This section explains the structure of an agent using the **EmergencyAgent.aeon** file as an example

### 1. Include (Optional)

You can include Python libraries at the top:

```
Include time
Include datetime
```

These can be used inside tasks.

---

### 2. Variables (Private & Public)

All variables are defined inside the `Private` block.

```
Private {
    int count;
    string status = "idle";
    Public int result;
}
```

- `Private` → only this agent can use
- `Public` → shared with other agents

---

### 3. Tasks (Core Logic)

Tasks define what the agent does.

```
Task process {
    result = count * 2
}
```

You can also use conditions:

```
Task check {
    IF count > 10 {
        result = 1
    } ELSE {
        result = 0
    }
}
```

---

### 4. Using Python in Tasks

You can directly call Python functions:

```
Task report {
    log("Result:", result)
    time.sleep(1)
}
```

[Functions](LIB FILE/Functions.md) 

---

### 5. Route Block (Execution Flow)

The `Route` block controls which task runs.

```
Route {
    on_start : process
    count > 10 : check
    on_end : report
}
```

- `on_start` → runs first
- conditions → decide next tasks
- `on_end` → runs at the end

---

### 6. Complete Example

```
Include time

Private {
    int count = 5
    Public int result = 0
}

Task process {
    result = count * 2
}

Task report {
    log("Final result:", result)
    time.sleep(1)
}

Route {
    on_start : process
    on_end : report
}
```

---

### Understanding the Agent Structure

- Variables → what information the agent keeps track of
- Tasks → the actions the agent performs
- Route → decides when each action should run

Together, this helps the agent work step-by-step and interact smoothly with other agents in the system.

[AEON Memory](AEON FILE/AEON Memory.md)

[AEON Includes](AEON FILE/AEON Includes.md)

[TASKS](AEON FILE/TASKS.md)