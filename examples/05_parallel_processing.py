"""
Example 5: Parallel Processing

This example demonstrates parallel node execution in LangGraph.
Multiple nodes can process data simultaneously and their results are merged.
"""

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, END, START


# Define the state with annotation for list accumulation
class State(TypedDict):
    input_data: str
    results: Annotated[list, add]


# Define parallel processing nodes
def process_a(state: State) -> State:
    """Process data - Path A"""
    print("  Processing in Path A...")
    result = f"A-processed({state['input_data']})"
    return {
        "results": [result]
    }


def process_b(state: State) -> State:
    """Process data - Path B"""
    print("  Processing in Path B...")
    result = f"B-processed({state['input_data']})"
    return {
        "results": [result]
    }


def process_c(state: State) -> State:
    """Process data - Path C"""
    print("  Processing in Path C...")
    result = f"C-processed({state['input_data']})"
    return {
        "results": [result]
    }


def display_results(state: State) -> State:
    """Display final results from all parallel processes"""
    print("\n  All parallel processes completed!")
    print(f"  Collected {len(state['results'])} results")
    # Return empty dict to avoid modifying state further
    # All processing is already done, this node is just for display
    return {}


def create_graph():
    """Create and configure the graph"""
    # Create the graph
    workflow = StateGraph(State)
    
    # Add all nodes
    workflow.add_node("process_a", process_a)
    workflow.add_node("process_b", process_b)
    workflow.add_node("process_c", process_c)
    workflow.add_node("display", display_results)
    
    # Fan out from START to all three parallel nodes
    workflow.add_edge(START, "process_a")
    workflow.add_edge(START, "process_b")
    workflow.add_edge(START, "process_c")
    
    # All parallel nodes converge to display
    workflow.add_edge("process_a", "display")
    workflow.add_edge("process_b", "display")
    workflow.add_edge("process_c", "display")
    
    # End after display
    workflow.add_edge("display", END)
    
    # Compile the graph
    return workflow.compile()


def main():
    """Main function to run the example"""
    # Create the graph
    app = create_graph()
    
    print("\n=== Running Parallel Processing Example ===\n")
    
    # Initial state
    initial_state = {
        "input_data": "test_data",
        "results": []
    }
    
    print(f"Input data: {initial_state['input_data']}")
    print("\nProcessing in parallel paths...\n")
    
    # Run the graph
    result = app.invoke(initial_state)
    
    print(f"\n=== Final Result ===")
    print(f"Input: {result['input_data']}")
    print(f"Results collected from parallel execution:")
    for i, res in enumerate(result['results'], 1):
        print(f"  {i}. {res}")


if __name__ == "__main__":
    main()
