# Nodes and Edges Explained

## Nodes: The Processing Units

**Nodes** are the individual steps in your graph where actual work happens. Each node is a Python function that:
- Receives the current state
- Performs some processing
- Returns state updates

### Node Anatomy

```python
def my_node(state: MyState) -> dict:
    """
    Args:
        state: Current state (read-only access)
    
    Returns:
        dict: Updates to merge into state
    """
    # 1. Read from state
    input_data = state["input"]
    
    # 2. Process
    result = process_data(input_data)
    
    # 3. Return updates
    return {"output": result}
```

### Node Types

#### 1. Processing Nodes
Transform or analyze data:

```python
def analyze_sentiment(state):
    text = state["text"]
    sentiment = "positive" if "good" in text.lower() else "negative"
    return {"sentiment": sentiment}
```

#### 2. Decision Nodes
Determine routing (used with conditional edges):

```python
def should_continue(state):
    if state["iterations"] < state["max_iterations"]:
        return {"should_continue": True}
    return {"should_continue": False}
```

#### 3. Integration Nodes
Call external services:

```python
def call_api(state):
    query = state["query"]
    response = requests.get(f"https://api.example.com/search?q={query}")
    return {"api_results": response.json()}
```

#### 4. LLM Nodes
Interact with language models:

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()

def llm_node(state):
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}
```

### Adding Nodes to Graph

```python
workflow = StateGraph(MyState)

# Add nodes with unique names
workflow.add_node("process", process_node)
workflow.add_node("analyze", analyze_node)
workflow.add_node("finalize", finalize_node)
```

## Edges: The Connections

**Edges** define how execution flows from one node to another. They're the "roads" between nodes.

### Edge Types

#### 1. Normal Edges (Static)
Fixed connections that always follow the same path:

```python
# Always go from "search" to "analyze"
workflow.add_edge("search", "analyze")

# Always go from "analyze" to END
workflow.add_edge("analyze", END)
```

#### 2. Conditional Edges (Dynamic)
Route based on state - the most powerful feature:

```python
def route_decision(state) -> str:
    """Return the name of the next node."""
    if state["needs_more_info"]:
        return "gather_more"
    else:
        return "finalize"

workflow.add_conditional_edges(
    "decision_point",
    route_decision,
    {
        "gather_more": "search_node",
        "finalize": "final_node"
    }
)
```

#### 3. Entry and End Points

```python
# Set where the graph starts
workflow.set_entry_point("first_node")

# Set where a path ends
workflow.add_edge("last_node", END)
```

## Conditional Edges in Detail

Conditional edges are where LangGraph shines - they enable dynamic, intelligent routing.

### Basic Conditional Edge

```python
def router(state):
    """Simple router based on state."""
    if state["score"] > 0.8:
        return "high_confidence"
    elif state["score"] > 0.5:
        return "medium_confidence"
    else:
        return "low_confidence"

workflow.add_conditional_edges(
    "scorer",               # From this node
    router,                 # Use this function
    {
        "high_confidence": "approve",
        "medium_confidence": "review",
        "low_confidence": "reject"
    }
)
```

### Conditional Edge with END

```python
def should_continue(state):
    if state["done"]:
        return END
    return "continue"

workflow.add_conditional_edges(
    "checker",
    should_continue,
    {
        "continue": "processor",
        END: END
    }
)
```

### Multi-Path Routing

```python
def complex_router(state):
    error = state.get("error")
    attempts = state.get("attempts", 0)
    
    if error and attempts < 3:
        return "retry"
    elif error and attempts >= 3:
        return "fail"
    elif state.get("needs_validation"):
        return "validate"
    else:
        return "success"

workflow.add_conditional_edges(
    "process",
    complex_router,
    {
        "retry": "process",        # Loop back
        "fail": "handle_error",
        "validate": "validator",
        "success": END
    }
)
```

## Graph Patterns

### 1. Linear Flow (Pipeline)
```
A → B → C → D → END
```

```python
workflow.add_edge("A", "B")
workflow.add_edge("B", "C")
workflow.add_edge("C", "D")
workflow.add_edge("D", END)
workflow.set_entry_point("A")
```

### 2. Branching (Fan-out)
```
        ┌→ B1 →┐
    A →→│       ├→ D → END
        └→ B2 →┘
```

```python
def router(state):
    if state["path"] == 1:
        return "B1"
    return "B2"

workflow.add_conditional_edges("A", router, {"B1": "B1", "B2": "B2"})
workflow.add_edge("B1", "D")
workflow.add_edge("B2", "D")
workflow.add_edge("D", END)
```

### 3. Cycles (Loops)
```
A → B → C
    ↑   ↓
    └───┘
```

```python
def should_loop(state):
    if state["iterations"] < 5:
        return "B"  # Loop back
    return "END"

workflow.add_edge("A", "B")
workflow.add_edge("B", "C")
workflow.add_conditional_edges("C", should_loop, {"B": "B", "END": END})
```

### 4. Agent Loop Pattern
```
    ┌→ tools →┐
    │         ↓
agent ←───── call
    ↓
   END
```

```python
def agent_decision(state):
    if state["needs_tool"]:
        return "use_tool"
    return "finish"

workflow.add_conditional_edges(
    "agent",
    agent_decision,
    {
        "use_tool": "tools",
        "finish": END
    }
)
workflow.add_edge("tools", "agent")  # Loop back
```

## Best Practices

### Node Best Practices

1. **Single Responsibility**: Each node should do one thing well
```python
# Good: Focused node
def extract_keywords(state):
    return {"keywords": extract(state["text"])}

# Avoid: Doing too much
def do_everything(state):
    keywords = extract(state["text"])
    sentiment = analyze(state["text"])
    summary = summarize(state["text"])
    return {"keywords": keywords, "sentiment": sentiment, "summary": summary}
```

2. **Error Handling**: Nodes should handle their own errors
```python
def safe_api_call(state):
    try:
        result = call_api(state["query"])
        return {"result": result, "error": None}
    except Exception as e:
        return {"result": None, "error": str(e)}
```

3. **Idempotency**: Nodes should be safe to retry
```python
def idempotent_node(state):
    # Check if work already done
    if state.get("processed"):
        return {}
    
    # Do work
    result = process()
    return {"processed": True, "result": result}
```

### Edge Best Practices

1. **Clear Routing Logic**: Make routing decisions obvious
```python
# Good: Clear decision
def clear_router(state):
    if state["confidence"] > 0.9:
        return "accept"
    return "reject"

# Avoid: Complex logic in router
def confusing_router(state):
    return "accept" if (state["confidence"] > 0.9 and 
                        state["validated"] and 
                        not state["flagged"] and
                        len(state["history"]) > 5) else "reject"
```

2. **Handle All Cases**: Ensure router covers all possibilities
```python
def robust_router(state):
    status = state.get("status", "unknown")
    
    # Explicit handling of all cases
    if status == "success":
        return "process_success"
    elif status == "error":
        return "handle_error"
    else:
        return "handle_unknown"  # Don't forget edge cases!
```

3. **Avoid Deep Nesting**: Keep graph structure flat when possible
```python
# Good: Flat structure
A → router → B1 → END
           → B2 → END

# Avoid: Deep nesting
A → B → router1 → C1 → router2 → D1 → END
                                → D2 → END
              → C2 → END
```

## Debugging Tips

### Visualize Your Graph
```python
# Get a visual representation
print(app.get_graph().draw_ascii())
```

### Add Logging to Nodes
```python
def debug_node(state):
    print(f"Node executing with state: {state}")
    result = process(state)
    print(f"Node returning: {result}")
    return result
```

### Test Nodes Independently
```python
# Test a single node
test_state = {"input": "test"}
result = my_node(test_state)
assert result["output"] == expected_output
```

## Common Mistakes

1. **Forgetting to return from nodes**
```python
# Wrong
def broken_node(state):
    result = process(state)
    # Missing return!

# Correct
def working_node(state):
    result = process(state)
    return {"result": result}
```

2. **Invalid routing**
```python
# Wrong: Router returns non-existent node name
def bad_router(state):
    return "non_existent_node"

# Correct: Router returns valid node names
def good_router(state):
    return "valid_node_name"
```

3. **Circular dependencies without exit**
```python
# Wrong: Infinite loop
workflow.add_edge("A", "B")
workflow.add_edge("B", "A")

# Correct: Conditional exit
workflow.add_edge("A", "B")
workflow.add_conditional_edges("B", should_continue, {
    "continue": "A",
    "stop": END
})
```

## Next Steps

You now have a solid understanding of the fundamentals! Ready to level up? Move on to [Intermediate Concepts](../02-intermediate/) to learn about:
- Advanced conditional routing
- Implementing cycles and loops
- Persistence with checkpointing
- Error handling strategies
