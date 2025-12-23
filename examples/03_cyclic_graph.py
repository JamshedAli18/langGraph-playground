"""
Example 3: Cyclic Graph with State

This example demonstrates a graph with cycles and state management.
The graph loops until a certain condition is met.
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END


# Define the state
class State(TypedDict):
    counter: int
    max_iterations: int
    messages: list


# Define nodes
def increment_counter(state: State) -> State:
    """Increment the counter"""
    new_counter = state["counter"] + 1
    message = f"Iteration {new_counter}"
    print(f"  {message}")
    
    return {
        "counter": new_counter,
        "max_iterations": state["max_iterations"],
        "messages": state["messages"] + [message]
    }


def process_data(state: State) -> State:
    """Process some data"""
    message = f"Processing data at iteration {state['counter']}"
    print(f"  {message}")
    
    return {
        "counter": state["counter"],
        "max_iterations": state["max_iterations"],
        "messages": state["messages"] + [message]
    }


# Conditional routing function
def should_continue(state: State) -> Literal["continue", "end"]:
    """Decide whether to continue looping or end"""
    if state["counter"] < state["max_iterations"]:
        return "continue"
    else:
        return "end"


def create_graph():
    """Create and configure the graph"""
    # Create the graph
    workflow = StateGraph(State)
    
    # Add nodes
    workflow.add_node("increment", increment_counter)
    workflow.add_node("process", process_data)
    
    # Set entry point
    workflow.set_entry_point("increment")
    
    # Add edge from increment to process
    workflow.add_edge("increment", "process")
    
    # Add conditional edge from process (creates the cycle)
    workflow.add_conditional_edges(
        "process",
        should_continue,
        {
            "continue": "increment",  # Loop back
            "end": END
        }
    )
    
    # Compile the graph
    return workflow.compile()


def main():
    """Main function to run the example"""
    # Create the graph
    app = create_graph()
    
    print("\n=== Running Cyclic Graph Example ===\n")
    
    # Initial state
    initial_state = {
        "counter": 0,
        "max_iterations": 5,
        "messages": []
    }
    
    print("Starting loop (max 5 iterations):\n")
    
    # Run the graph
    result = app.invoke(initial_state)
    
    print(f"\n=== Final Result ===")
    print(f"Total iterations: {result['counter']}")
    print(f"Messages collected: {len(result['messages'])}")
    print("\nAll messages:")
    for msg in result["messages"]:
        print(f"  - {msg}")


if __name__ == "__main__":
    main()
