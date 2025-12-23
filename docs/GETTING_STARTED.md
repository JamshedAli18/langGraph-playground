# Getting Started with LangGraph

This guide will help you set up your environment and run your first LangGraph example.

## Installation

### 1. Python Setup

Make sure you have Python 3.9 or higher:

```bash
python --version
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install LangGraph

```bash
pip install langgraph
```

### 4. Install Optional Dependencies

For working with LLMs:
```bash
pip install langchain langchain-openai
```

For other integrations:
```bash
pip install langchain-anthropic  # For Claude
pip install langchain-google-genai  # For Gemini
```

## Running Your First Example

### 1. Navigate to Examples Directory

```bash
cd examples/basic
```

### 2. Run the Sequential Graph Example

```bash
python 01_sequential_graph.py
```

Expected output:
```
Starting graph execution...
Initial input: hello world
--------------------------------------------------
Step 1: hello world -> HELLO WORLD
Step 2: HELLO WORLD -> PROCESSED: HELLO WORLD
Step 3: PROCESSED: HELLO WORLD -> PROCESSED: HELLO WORLD [COMPLETE]
--------------------------------------------------
Final output: PROCESSED: HELLO WORLD [COMPLETE]
```

### 3. Try Other Examples

```bash
# Conditional routing
python 02_conditional_routing.py

# State accumulation
python 03_state_accumulation.py
```

## Understanding the Code

Let's break down the basic example:

### 1. Import Required Modules
```python
from typing import TypedDict
from langgraph.graph import StateGraph, END
```

### 2. Define Your State
```python
class SimpleState(TypedDict):
    input: str
    output: str
```

### 3. Create Node Functions
```python
def my_node(state: SimpleState) -> dict:
    result = process(state["input"])
    return {"output": result}
```

### 4. Build the Graph
```python
workflow = StateGraph(SimpleState)
workflow.add_node("my_node", my_node)
workflow.set_entry_point("my_node")
workflow.add_edge("my_node", END)
app = workflow.compile()
```

### 5. Run It
```python
result = app.invoke({"input": "test", "output": ""})
print(result["output"])
```

## Next Steps

### For Beginners
1. Read [Understanding Graphs](../docs/01-fundamentals/01-understanding-graphs.md)
2. Learn about [State Management](../docs/01-fundamentals/02-state-management.md)
3. Follow [Creating Your First Graph](../docs/01-fundamentals/03-first-graph.md)
4. Study [Nodes and Edges](../docs/01-fundamentals/04-nodes-and-edges.md)

### For Intermediate Users
- Explore conditional routing examples
- Learn about cycles and loops
- Understand checkpointing
- Master error handling

### For Advanced Users
- Build agent systems
- Integrate external tools
- Implement multi-agent architectures
- Work with streaming

## Common Issues

### Issue: "Module not found"
**Solution**: Make sure you've installed LangGraph:
```bash
pip install langgraph
```

### Issue: "Python version too old"
**Solution**: Upgrade to Python 3.9+:
```bash
python --version
```

### Issue: Examples don't run
**Solution**: Make sure you're in the correct directory:
```bash
cd /path/to/langGraph-playground/examples/basic
```

## Getting Help

- Check the [documentation](../docs/)
- Review the [examples](../examples/)
- Read the [official LangGraph docs](https://python.langchain.com/docs/langgraph)

## Tips for Success

1. **Start Simple**: Begin with basic sequential flows
2. **Test Incrementally**: Test each node independently
3. **Use Type Hints**: Leverage TypedDict for clarity
4. **Print State**: Add print statements to debug
5. **Read Examples**: Learn from working code

## Ready to Build?

Now that you're set up, explore the examples and documentation to build your own LangGraph applications!

Happy coding! 🚀
