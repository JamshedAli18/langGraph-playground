# State Management in LangGraph

## What is State?

**State** is the data structure that flows through your graph, getting updated at each node. It's the "memory" of your graph - containing all the information needed for processing.

## State as a TypedDict

LangGraph uses Python's `TypedDict` to define state schemas, providing type safety and clear documentation.

```python
from typing import TypedDict

class MyState(TypedDict):
    input: str
    output: str
    steps_taken: int
    history: list[str]
```

## State Updates

When a node returns a dictionary, LangGraph **merges** it with the current state:

```python
# Current state: {"input": "hello", "steps": 0}

def my_node(state: MyState):
    return {"steps": state["steps"] + 1, "output": "processed"}

# New state: {"input": "hello", "steps": 1, "output": "processed"}
```

### Key Points:
- Only returned keys are updated
- Unreturned keys remain unchanged
- Updates are merged, not replaced

## State Reducers

For more complex state updates (like appending to lists), use **reducers**:

```python
from typing import Annotated
from operator import add

class AgentState(TypedDict):
    messages: Annotated[list[str], add]  # Messages will be appended, not replaced
    counter: int

# Node 1 returns: {"messages": ["first"]}
# Node 2 returns: {"messages": ["second"]}
# Final state: {"messages": ["first", "second"]}
```

### Common Reducers:
- `operator.add`: Append to lists, add numbers
- Custom functions: Define your own merging logic

```python
def merge_unique(left: list, right: list) -> list:
    return list(set(left + right))

class State(TypedDict):
    tags: Annotated[list[str], merge_unique]
```

## State Access Patterns

### Reading State
Access state fields like a dictionary:

```python
def process_node(state: MyState):
    user_input = state["input"]
    current_count = state.get("count", 0)  # With default
    return {"output": f"Processed: {user_input}"}
```

### Updating State
Return a dictionary with the fields to update:

```python
def update_node(state: MyState):
    new_count = state["count"] + 1
    return {
        "count": new_count,
        "last_update": "2024-01-01"
    }
```

### Partial Updates
Only update what you need:

```python
def increment_only(state: MyState):
    return {"count": state["count"] + 1}
    # Other fields remain unchanged
```

## State Best Practices

### 1. Keep State Minimal
Only include data that needs to flow through the graph:

```python
# Good: Only essential data
class State(TypedDict):
    query: str
    result: str

# Avoid: Temporary or computed values
class State(TypedDict):
    query: str
    result: str
    temp_processing_var: str  # Should be local to node
```

### 2. Use Clear Field Names

```python
# Good: Descriptive names
class State(TypedDict):
    user_query: str
    search_results: list[str]
    final_answer: str

# Avoid: Cryptic abbreviations
class State(TypedDict):
    q: str
    res: list[str]
    ans: str
```

### 3. Document Your State

```python
class AgentState(TypedDict):
    """State for the research agent workflow.
    
    Fields:
        query: The user's original question
        documents: Retrieved relevant documents
        answer: Final synthesized answer
        iteration_count: Number of search iterations performed
    """
    query: str
    documents: list[str]
    answer: str
    iteration_count: int
```

### 4. Use Type Hints

```python
from typing import Optional, List

class State(TypedDict):
    required_field: str
    optional_field: Optional[str]
    list_field: List[str]
```

## State Patterns

### Accumulator Pattern
Building up results over multiple steps:

```python
class State(TypedDict):
    results: Annotated[list[str], add]

def step1(state): return {"results": ["step1"]}
def step2(state): return {"results": ["step2"]}
def step3(state): return {"results": ["step3"]}
# Final: ["step1", "step2", "step3"]
```

### Counter Pattern
Tracking iterations or attempts:

```python
class State(TypedDict):
    attempts: int
    max_attempts: int

def try_action(state):
    if state["attempts"] >= state["max_attempts"]:
        return {"error": "Max attempts reached"}
    return {"attempts": state["attempts"] + 1}
```

### Message History Pattern
Common in chat applications:

```python
from typing import Annotated
from operator import add

class ChatState(TypedDict):
    messages: Annotated[list[dict], add]

def add_user_message(state):
    return {"messages": [{"role": "user", "content": "Hello"}]}

def add_assistant_message(state):
    return {"messages": [{"role": "assistant", "content": "Hi there!"}]}
```

### Context Accumulation Pattern
Gathering information across multiple nodes:

```python
class State(TypedDict):
    context: dict

def gather_info_1(state):
    return {"context": {**state["context"], "source_1": "data"}}

def gather_info_2(state):
    return {"context": {**state["context"], "source_2": "more data"}}
```

## State Immutability

**Important**: State should be treated as immutable in nodes. Don't modify state directly:

```python
# Bad: Modifying state directly
def bad_node(state):
    state["count"] += 1  # Don't do this!
    return state

# Good: Return new values
def good_node(state):
    return {"count": state["count"] + 1}
```

## Common State Errors

### 1. Forgetting to Return Updates
```python
# Wrong: No return statement
def broken_node(state):
    new_value = state["value"] + 1
    # Missing return!

# Correct: Return the update
def fixed_node(state):
    return {"value": state["value"] + 1}
```

### 2. Returning Full State Instead of Updates
```python
# Inefficient: Returning entire state
def inefficient_node(state):
    state["value"] += 1
    return state  # Returns everything

# Better: Return only updates
def efficient_node(state):
    return {"value": state["value"] + 1}
```

### 3. Incorrect Reducer Usage
```python
# Wrong: Replacing list instead of appending
class State(TypedDict):
    items: list[str]  # No reducer

def node(state):
    return {"items": ["new"]}  # Replaces entire list!

# Correct: Use add reducer
class State(TypedDict):
    items: Annotated[list[str], add]

def node(state):
    return {"items": ["new"]}  # Appends to list
```

## Next Steps

Now that you understand state management, let's [create your first graph](03-first-graph.md) and see everything in action!
