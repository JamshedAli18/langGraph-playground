"""
Example 2: Conditional Branching

This example demonstrates conditional routing in LangGraph.
The graph decides which path to take based on the state.
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END


# Define the state
class State(TypedDict):
    number: int
    path: str
    result: str


# Define nodes
def check_number(state: State) -> State:
    """Entry node that checks the number"""
    print(f"Checking number: {state['number']}")
    return state


def even_path(state: State) -> State:
    """Process even numbers"""
    print(f"Processing even number: {state['number']}")
    return {
        "number": state["number"],
        "path": "even",
        "result": f"{state['number']} is even"
    }


def odd_path(state: State) -> State:
    """Process odd numbers"""
    print(f"Processing odd number: {state['number']}")
    return {
        "number": state["number"],
        "path": "odd",
        "result": f"{state['number']} is odd"
    }


def finalize(state: State) -> State:
    """Finalize the result"""
    print(f"Finalizing: {state['result']}")
    return state


# Conditional routing function
def route_number(state: State) -> Literal["even_path", "odd_path"]:
    """Route based on whether the number is even or odd"""
    if state["number"] % 2 == 0:
        return "even_path"
    else:
        return "odd_path"


def create_graph():
    """Create and configure the graph"""
    # Create the graph
    workflow = StateGraph(State)
    
    # Add nodes
    workflow.add_node("check_number", check_number)
    workflow.add_node("even_path", even_path)
    workflow.add_node("odd_path", odd_path)
    workflow.add_node("finalize", finalize)
    
    # Add edges
    workflow.set_entry_point("check_number")
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "check_number",
        route_number,
        {
            "even_path": "even_path",
            "odd_path": "odd_path"
        }
    )
    
    # Both paths lead to finalize
    workflow.add_edge("even_path", "finalize")
    workflow.add_edge("odd_path", "finalize")
    workflow.add_edge("finalize", END)
    
    # Compile the graph
    return workflow.compile()


def main():
    """Main function to run the example"""
    # Create the graph
    app = create_graph()
    
    print("\n=== Running Conditional Branching Example ===\n")
    
    # Test with different numbers
    test_numbers = [4, 7, 10, 15]
    
    for num in test_numbers:
        print(f"\n--- Testing with number: {num} ---")
        initial_state = {
            "number": num,
            "path": "",
            "result": ""
        }
        
        result = app.invoke(initial_state)
        print(f"Result: {result['result']}")
        print(f"Path taken: {result['path']}")


if __name__ == "__main__":
    main()
