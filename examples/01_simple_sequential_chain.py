"""
Example 1: Simple Sequential Chain

This example demonstrates a basic LangGraph with sequential nodes.
Each node performs a simple transformation on the state.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END


# Define the state
class State(TypedDict):
    message: str
    count: int


# Define nodes
def node_1(state: State) -> State:
    """First node that modifies the message"""
    print(f"Node 1: Processing '{state['message']}'")
    return {
        "message": state["message"] + " -> Node1",
        "count": state["count"] + 1
    }


def node_2(state: State) -> State:
    """Second node that modifies the message"""
    print(f"Node 2: Processing '{state['message']}'")
    return {
        "message": state["message"] + " -> Node2",
        "count": state["count"] + 1
    }


def node_3(state: State) -> State:
    """Third node that modifies the message"""
    print(f"Node 3: Processing '{state['message']}'")
    return {
        "message": state["message"] + " -> Node3",
        "count": state["count"] + 1
    }


def create_graph():
    """Create and configure the graph"""
    # Create the graph
    workflow = StateGraph(State)
    
    # Add nodes
    workflow.add_node("node_1", node_1)
    workflow.add_node("node_2", node_2)
    workflow.add_node("node_3", node_3)
    
    # Add edges (sequential flow)
    workflow.set_entry_point("node_1")
    workflow.add_edge("node_1", "node_2")
    workflow.add_edge("node_2", "node_3")
    workflow.add_edge("node_3", END)
    
    # Compile the graph
    return workflow.compile()


def main():
    """Main function to run the example"""
    # Create the graph
    app = create_graph()
    
    # Initial state
    initial_state = {
        "message": "Start",
        "count": 0
    }
    
    print("\n=== Running Simple Sequential Chain ===\n")
    
    # Run the graph
    result = app.invoke(initial_state)
    
    print(f"\n=== Final Result ===")
    print(f"Message: {result['message']}")
    print(f"Node count: {result['count']}")


if __name__ == "__main__":
    main()
