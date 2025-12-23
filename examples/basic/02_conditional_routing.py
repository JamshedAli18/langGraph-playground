"""
Basic Example: Conditional Routing

This example shows how to use conditional edges to make
decisions about which path to take based on state.

Concepts covered:
- Conditional edges
- Router functions
- Multiple execution paths
- Decision-making in graphs
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END


# Define state
class RoutingState(TypedDict):
    """State with a value that determines routing."""
    value: int
    path_taken: str
    result: str


# Node functions
def input_node(state: RoutingState) -> dict:
    """Process input and prepare for routing."""
    value = state["value"]
    print(f"Input node: Received value {value}")
    return {}


def high_value_node(state: RoutingState) -> dict:
    """Handle high values (>= 50)."""
    print("Taking HIGH value path")
    result = f"High value processing: {state['value']} * 2 = {state['value'] * 2}"
    return {
        "path_taken": "high",
        "result": result
    }


def medium_value_node(state: RoutingState) -> dict:
    """Handle medium values (20-49)."""
    print("Taking MEDIUM value path")
    result = f"Medium value processing: {state['value']} + 10 = {state['value'] + 10}"
    return {
        "path_taken": "medium",
        "result": result
    }


def low_value_node(state: RoutingState) -> dict:
    """Handle low values (< 20)."""
    print("Taking LOW value path")
    result = f"Low value processing: {state['value']} remains {state['value']}"
    return {
        "path_taken": "low",
        "result": result
    }


def output_node(state: RoutingState) -> dict:
    """Final output node."""
    print(f"Output node: Completed via {state['path_taken']} path")
    return {}


# Router function
def route_by_value(state: RoutingState) -> Literal["high", "medium", "low"]:
    """
    Route based on the value.
    
    Returns the name of the next node to execute.
    """
    value = state["value"]
    
    if value >= 50:
        return "high"
    elif value >= 20:
        return "medium"
    else:
        return "low"


# Build graph
def create_graph():
    """Create the routing graph."""
    workflow = StateGraph(RoutingState)
    
    # Add nodes
    workflow.add_node("input", input_node)
    workflow.add_node("high", high_value_node)
    workflow.add_node("medium", medium_value_node)
    workflow.add_node("low", low_value_node)
    workflow.add_node("output", output_node)
    
    # Set entry point
    workflow.set_entry_point("input")
    
    # Add conditional edge from input
    workflow.add_conditional_edges(
        "input",
        route_by_value,
        {
            "high": "high",
            "medium": "medium",
            "low": "low"
        }
    )
    
    # All paths converge to output
    workflow.add_edge("high", "output")
    workflow.add_edge("medium", "output")
    workflow.add_edge("low", "output")
    
    # End
    workflow.add_edge("output", END)
    
    return workflow.compile()


# Run examples
def main():
    """Test the graph with different values."""
    app = create_graph()
    
    test_values = [75, 35, 10]
    
    for value in test_values:
        print("\n" + "=" * 60)
        print(f"Testing with value: {value}")
        print("=" * 60)
        
        result = app.invoke({
            "value": value,
            "path_taken": "",
            "result": ""
        })
        
        print(f"\nResult: {result['result']}")
        print(f"Path taken: {result['path_taken']}")


if __name__ == "__main__":
    main()
