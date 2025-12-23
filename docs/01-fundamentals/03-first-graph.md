# Creating Your First Graph

Let's build a complete, working LangGraph application step by step!

## The Problem

We'll create a simple research assistant that:
1. Takes a user question
2. Searches for information (simulated)
3. Generates an answer
4. Formats the final response

## Step 1: Define the State

```python
from typing import TypedDict, Annotated, List
from operator import add

class ResearchState(TypedDict):
    """State for our research assistant."""
    question: str                           # User's input
    search_results: List[str]               # Found information
    answer: str                             # Generated answer
    steps: Annotated[List[str], add]       # Track our progress
```

## Step 2: Create Node Functions

Each node is a Python function that receives state and returns updates:

```python
def search_node(state: ResearchState) -> ResearchState:
    """Simulate searching for information."""
    question = state["question"]
    
    # In a real app, you'd call a search API here
    results = [
        f"Information about: {question}",
        f"Related fact 1 for {question}",
        f"Related fact 2 for {question}"
    ]
    
    return {
        "search_results": results,
        "steps": ["Searched for information"]
    }

def generate_answer_node(state: ResearchState) -> ResearchState:
    """Generate an answer from search results."""
    question = state["question"]
    results = state["search_results"]
    
    # In a real app, you'd use an LLM here
    answer = f"Based on the search results, here's what I found about '{question}': "
    answer += " ".join(results[:2])
    
    return {
        "answer": answer,
        "steps": ["Generated answer from results"]
    }

def format_response_node(state: ResearchState) -> ResearchState:
    """Format the final response."""
    answer = state["answer"]
    steps_taken = state["steps"]
    
    formatted = f"""
=== Research Assistant Response ===
Question: {state['question']}

Answer: {answer}

Process: {' → '.join(steps_taken)}
===================================
    """
    
    return {
        "answer": formatted,
        "steps": ["Formatted final response"]
    }
```

## Step 3: Build the Graph

```python
from langgraph.graph import StateGraph, END

# Create the graph
workflow = StateGraph(ResearchState)

# Add nodes
workflow.add_node("search", search_node)
workflow.add_node("generate", generate_answer_node)
workflow.add_node("format", format_response_node)

# Define the flow: search → generate → format → END
workflow.add_edge("search", "generate")
workflow.add_edge("generate", "format")
workflow.add_edge("format", END)

# Set the entry point
workflow.set_entry_point("search")

# Compile the graph
app = workflow.compile()
```

## Step 4: Run the Graph

```python
# Define initial state
initial_state = {
    "question": "What is LangGraph?",
    "search_results": [],
    "answer": "",
    "steps": []
}

# Execute the graph
result = app.invoke(initial_state)

# Print the result
print(result["answer"])
```

## Complete Example

Here's the full code in one place:

```python
from typing import TypedDict, Annotated, List
from operator import add
from langgraph.graph import StateGraph, END

# 1. Define State
class ResearchState(TypedDict):
    question: str
    search_results: List[str]
    answer: str
    steps: Annotated[List[str], add]

# 2. Define Nodes
def search_node(state: ResearchState) -> ResearchState:
    question = state["question"]
    results = [
        f"Information about: {question}",
        f"Related fact 1 for {question}",
        f"Related fact 2 for {question}"
    ]
    return {
        "search_results": results,
        "steps": ["Searched for information"]
    }

def generate_answer_node(state: ResearchState) -> ResearchState:
    question = state["question"]
    results = state["search_results"]
    answer = f"Based on the search results, here's what I found about '{question}': "
    answer += " ".join(results[:2])
    return {
        "answer": answer,
        "steps": ["Generated answer from results"]
    }

def format_response_node(state: ResearchState) -> ResearchState:
    answer = state["answer"]
    formatted = f"""
=== Research Assistant Response ===
Question: {state['question']}

Answer: {answer}

Process: {' → '.join(state['steps'])}
===================================
    """
    return {
        "answer": formatted,
        "steps": ["Formatted final response"]
    }

# 3. Build Graph
workflow = StateGraph(ResearchState)
workflow.add_node("search", search_node)
workflow.add_node("generate", generate_answer_node)
workflow.add_node("format", format_response_node)

workflow.add_edge("search", "generate")
workflow.add_edge("generate", "format")
workflow.add_edge("format", END)

workflow.set_entry_point("search")

# 4. Compile
app = workflow.compile()

# 5. Run
result = app.invoke({
    "question": "What is LangGraph?",
    "search_results": [],
    "answer": "",
    "steps": []
})

print(result["answer"])
```

## Understanding the Flow

1. **Entry**: Start at "search" node
2. **Search**: Gather information (simulated)
3. **Generate**: Create an answer from results
4. **Format**: Make the response user-friendly
5. **End**: Execution completes

## Running the Example

Save the code to a file (e.g., `first_graph.py`) and run:

```bash
python first_graph.py
```

## Expected Output

```
=== Research Assistant Response ===
Question: What is LangGraph?

Answer: Based on the search results, here's what I found about 'What is LangGraph?': Information about: What is LangGraph? Related fact 1 for What is LangGraph?

Process: Searched for information → Generated answer from results → Formatted final response
===================================
```

## Exercises

Try modifying the example:

1. **Add a validation node** that checks if the answer is long enough
2. **Add error handling** for empty search results
3. **Add a filtering node** that selects the most relevant search results
4. **Track execution time** in the state

### Exercise 1 Solution Preview:

```python
def validate_answer_node(state: ResearchState) -> ResearchState:
    answer = state["answer"]
    if len(answer) < 10:
        return {
            "answer": "Answer is too short, needs more information",
            "steps": ["Validated answer (failed)"]
        }
    return {"steps": ["Validated answer (passed)"]}

# Add to graph:
workflow.add_node("validate", validate_answer_node)
workflow.add_edge("generate", "validate")
workflow.add_edge("validate", "format")
```

## Common Issues and Solutions

### Issue: "Key not found in state"
**Solution**: Make sure all required state keys are initialized:
```python
initial_state = {
    "question": "test",
    "search_results": [],  # Don't forget to initialize!
    "answer": "",
    "steps": []
}
```

### Issue: "State not updating"
**Solution**: Ensure your nodes return dictionaries:
```python
def my_node(state):
    return {"key": "value"}  # Must return dict
```

### Issue: "Graph doesn't end"
**Solution**: Make sure you have an edge to END or a finish point:
```python
workflow.add_edge("last_node", END)
```

## Next Steps

Congratulations! You've built your first LangGraph application. Next, let's dive deeper into [Nodes and Edges](04-nodes-and-edges.md) to learn about more advanced connection patterns.
