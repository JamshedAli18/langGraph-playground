# Fundamentals of LangGraph

Welcome to the fundamentals section! This is where your LangGraph journey begins.

## What You'll Learn

1. **Graphs, Nodes, and Edges** - The building blocks of LangGraph
2. **State Management** - How data flows through your graph
3. **Basic Graph Construction** - Creating your first graph
4. **Execution Flow** - Understanding how graphs run

## Contents

- [Understanding Graphs](01-understanding-graphs.md)
- [Working with State](02-state-management.md)
- [Creating Your First Graph](03-first-graph.md)
- [Nodes and Edges Explained](04-nodes-and-edges.md)

## Prerequisites

Before diving in, make sure you have:
- Python 3.9+ installed
- Basic understanding of Python functions
- Familiarity with the concept of state machines (helpful but not required)

## Installation

```bash
pip install langgraph langchain langchain-openai
```

## Your First Graph - Quick Example

Here's a taste of what you'll be able to build:

```python
from langgraph.graph import StateGraph
from typing import TypedDict

# Define your state
class State(TypedDict):
    message: str
    count: int

# Create nodes (processing steps)
def process_message(state: State) -> State:
    return {"message": state["message"].upper(), "count": state["count"] + 1}

def finalize(state: State) -> State:
    return {"message": f"Processed: {state['message']}", "count": state["count"] + 1}

# Build the graph
workflow = StateGraph(State)
workflow.add_node("process", process_message)
workflow.add_node("finalize", finalize)
workflow.add_edge("process", "finalize")
workflow.set_entry_point("process")
workflow.set_finish_point("finalize")

# Compile and run
app = workflow.compile()
result = app.invoke({"message": "hello", "count": 0})
print(result)  # {'message': 'Processed: HELLO', 'count': 2}
```

## Next Steps

Start with [Understanding Graphs](01-understanding-graphs.md) to build a solid foundation!
