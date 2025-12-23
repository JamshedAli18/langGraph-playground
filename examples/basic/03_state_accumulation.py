"""
Basic Example: State Accumulation

This example demonstrates how to accumulate data across multiple
nodes using state reducers.

Concepts covered:
- State reducers (operator.add)
- Accumulating lists
- Tracking progress across nodes
- Using Annotated types
"""

from typing import TypedDict, Annotated, List
from operator import add
from langgraph.graph import StateGraph, END


# Define state with accumulator
class AccumulatorState(TypedDict):
    """State that accumulates results from multiple nodes."""
    input: str
    results: Annotated[List[str], add]  # This will accumulate!
    counter: int


# Node functions
def node_a(state: AccumulatorState) -> dict:
    """First processing node."""
    text = state["input"]
    result = f"Node A processed: {text.upper()}"
    print(f"Node A: {result}")
    
    return {
        "results": [result],  # Appended to list, not replaced
        "counter": state["counter"] + 1
    }


def node_b(state: AccumulatorState) -> dict:
    """Second processing node."""
    text = state["input"]
    result = f"Node B processed: {text.lower()}"
    print(f"Node B: {result}")
    
    return {
        "results": [result],
        "counter": state["counter"] + 1
    }


def node_c(state: AccumulatorState) -> dict:
    """Third processing node."""
    text = state["input"]
    result = f"Node C processed: {len(text)} characters"
    print(f"Node C: {result}")
    
    return {
        "results": [result],
        "counter": state["counter"] + 1
    }


def summarize_node(state: AccumulatorState) -> dict:
    """Summarize all accumulated results."""
    results = state["results"]
    summary = f"Processed {state['counter']} times with {len(results)} results"
    print(f"\nSummary: {summary}")
    
    return {
        "results": [summary]
    }


# Build graph
def create_graph():
    """Create the accumulator graph."""
    workflow = StateGraph(AccumulatorState)
    
    # Add nodes
    workflow.add_node("a", node_a)
    workflow.add_node("b", node_b)
    workflow.add_node("c", node_c)
    workflow.add_node("summarize", summarize_node)
    
    # Sequential flow
    workflow.add_edge("a", "b")
    workflow.add_edge("b", "c")
    workflow.add_edge("c", "summarize")
    workflow.add_edge("summarize", END)
    
    # Set entry point
    workflow.set_entry_point("a")
    
    return workflow.compile()


# Run
def main():
    """Execute the accumulator example."""
    app = create_graph()
    
    print("Starting accumulator example...")
    print("=" * 60)
    
    result = app.invoke({
        "input": "Hello World",
        "results": [],
        "counter": 0
    })
    
    print("\n" + "=" * 60)
    print("Final accumulated results:")
    for i, item in enumerate(result["results"], 1):
        print(f"{i}. {item}")
    
    print(f"\nTotal operations: {result['counter']}")


if __name__ == "__main__":
    main()
