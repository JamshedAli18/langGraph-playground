"""
Basic Example: Simple Sequential Graph

This example demonstrates the most basic LangGraph pattern:
a sequential flow through multiple processing steps.

Concepts covered:
- State definition with TypedDict
- Creating node functions
- Building a linear graph
- Running the graph
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END


# Step 1: Define the state schema
class SimpleState(TypedDict):
    """State that flows through our graph."""
    input: str
    step1_output: str
    step2_output: str
    final_output: str


# Step 2: Define node functions
def step1(state: SimpleState) -> dict:
    """First processing step: Convert to uppercase."""
    text = state["input"]
    result = text.upper()
    print(f"Step 1: {text} -> {result}")
    return {"step1_output": result}


def step2(state: SimpleState) -> dict:
    """Second processing step: Add prefix."""
    text = state["step1_output"]
    result = f"PROCESSED: {text}"
    print(f"Step 2: {text} -> {result}")
    return {"step2_output": result}


def step3(state: SimpleState) -> dict:
    """Final processing step: Add suffix."""
    text = state["step2_output"]
    result = f"{text} [COMPLETE]"
    print(f"Step 3: {text} -> {result}")
    return {"final_output": result}


# Step 3: Build the graph
def create_graph():
    """Create and compile the graph."""
    workflow = StateGraph(SimpleState)
    
    # Add nodes
    workflow.add_node("step1", step1)
    workflow.add_node("step2", step2)
    workflow.add_node("step3", step3)
    
    # Add edges (define the flow)
    workflow.add_edge("step1", "step2")
    workflow.add_edge("step2", "step3")
    workflow.add_edge("step3", END)
    
    # Set entry point
    workflow.set_entry_point("step1")
    
    # Compile
    return workflow.compile()


# Step 4: Run the graph
def main():
    """Main execution function."""
    app = create_graph()
    
    # Initial state
    initial_state = {
        "input": "hello world",
        "step1_output": "",
        "step2_output": "",
        "final_output": ""
    }
    
    print("Starting graph execution...")
    print(f"Initial input: {initial_state['input']}")
    print("-" * 50)
    
    # Execute
    result = app.invoke(initial_state)
    
    print("-" * 50)
    print(f"Final output: {result['final_output']}")
    print("\nFull final state:")
    for key, value in result.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
