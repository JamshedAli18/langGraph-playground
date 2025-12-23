"""
Intermediate Example: Loop with Exit Condition

This example shows how to create a cycle (loop) in your graph
that continues until a condition is met.

Concepts covered:
- Cycles/loops in graphs
- Exit conditions
- Iterative processing
- Counter-based termination
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END


# Define state
class LoopState(TypedDict):
    """State for looping example."""
    counter: int
    max_iterations: int
    results: list[str]


# Node functions
def process_node(state: LoopState) -> dict:
    """Process data - this runs in a loop."""
    counter = state["counter"]
    result = f"Iteration {counter}: Processing..."
    print(f"  {result}")
    
    return {
        "counter": counter + 1,
        "results": state["results"] + [result]
    }


def check_node(state: LoopState) -> dict:
    """Check if we should continue looping."""
    counter = state["counter"]
    max_iter = state["max_iterations"]
    
    if counter < max_iter:
        print(f"Check: {counter}/{max_iter} - Continuing...")
    else:
        print(f"Check: {counter}/{max_iter} - Done!")
    
    return {}


# Router function
def should_continue(state: LoopState) -> str:
    """
    Decide whether to continue the loop or end.
    
    Returns:
        "continue" to loop back to process
        "end" to finish
    """
    if state["counter"] < state["max_iterations"]:
        return "continue"
    return "end"


# Build graph
def create_graph():
    """Create a graph with a loop."""
    workflow = StateGraph(LoopState)
    
    # Add nodes
    workflow.add_node("process", process_node)
    workflow.add_node("check", check_node)
    
    # Set entry point
    workflow.set_entry_point("process")
    
    # Create the loop
    workflow.add_edge("process", "check")
    
    # Conditional edge: either loop back or end
    workflow.add_conditional_edges(
        "check",
        should_continue,
        {
            "continue": "process",  # Loop back!
            "end": END
        }
    )
    
    return workflow.compile()


# Run
def main():
    """Run the loop example."""
    app = create_graph()
    
    print("Starting loop example (max 5 iterations)...")
    print("=" * 60)
    
    result = app.invoke({
        "counter": 0,
        "max_iterations": 5,
        "results": []
    })
    
    print("\n" + "=" * 60)
    print(f"Loop completed after {result['counter']} iterations")
    print("\nAll results:")
    for item in result["results"]:
        print(f"  - {item}")


if __name__ == "__main__":
    main()
