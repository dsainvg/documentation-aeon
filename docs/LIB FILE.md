# LIB FILE

Owner: Durga Sai

A `.lib` file is used to define reusable functions that can be used inside agent files.

It helps you:

- avoid repeating logic
- write complex operations in Python
- reuse functions across multiple agents

---

### Example (math.lib)

```
Func add {
    result = a + b
    return result;
}

Func multiply {
    result = a * b
    return result;
}
```

---

### Explanation

- `Func` → defines a function
- Inside the block → you can write Python code
- `return` → specifies the output of the function

---

### Using Library Functions in Agents

First, include the library in your agent file:

```
Include math
```

Then call the function inside a task:

```
Task compute {
    result = add(a, b)
}
```

---

### Key Points

- `.lib` files only contain functions
- Functions use Python syntax
- Must end with `return <variable>;`
- Can be reused across multiple agents

---

[Functions](LIB FILE/Functions.md)