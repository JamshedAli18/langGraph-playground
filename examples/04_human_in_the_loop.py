"""
Example 4: Human-in-the-Loop

This example demonstrates a graph that can be interrupted for human input.
It shows how to pause execution and wait for user feedback.
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver


# Define the state
class State(TypedDict):
    question: str
    answer: str
    human_feedback: str
    status: str


# Define nodes
def ask_question(state: State) -> State:
    """Prepare a question"""
    print(f"\nPreparing question: {state['question']}")
    return {
        "question": state["question"],
        "answer": "",
        "human_feedback": state.get("human_feedback", ""),
        "status": "waiting_for_human"
    }


def process_feedback(state: State) -> State:
    """Process the human feedback"""
    feedback = state.get("human_feedback", "")
    print(f"\nProcessing feedback: {feedback}")
    
    answer = f"Thank you for your input: '{feedback}'"
    
    return {
        "question": state["question"],
        "answer": answer,
        "human_feedback": feedback,
        "status": "completed"
    }


def should_continue(state: State) -> Literal["process", "wait"]:
    """Check if we have human feedback"""
    if state.get("human_feedback"):
        return "process"
    else:
        return "wait"


def create_graph():
    """Create and configure the graph"""
    # Create the graph with memory for checkpointing
    workflow = StateGraph(State)
    
    # Add nodes
    workflow.add_node("ask", ask_question)
    workflow.add_node("process_feedback", process_feedback)
    
    # Set entry point
    workflow.set_entry_point("ask")
    
    # Add conditional edge
    workflow.add_conditional_edges(
        "ask",
        should_continue,
        {
            "process": "process_feedback",
            "wait": END  # End here, waiting for human input
        }
    )
    
    workflow.add_edge("process_feedback", END)
    
    # Compile with checkpointer for interruption support
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)


def main():
    """Main function to run the example"""
    # Create the graph
    app = create_graph()
    
    print("\n=== Running Human-in-the-Loop Example ===\n")
    
    # Initial state
    initial_state = {
        "question": "What is your favorite programming language?",
        "answer": "",
        "human_feedback": "",
        "status": "pending"
    }
    
    # Configuration for thread
    config = {"configurable": {"thread_id": "1"}}
    
    # First invocation - will stop before process_feedback
    print("First run - preparing question...")
    result = app.invoke(initial_state, config)
    print(f"Status: {result['status']}")
    
    # Simulate getting human input
    print("\n[Simulating human providing feedback...]")
    human_input = "Python"
    
    # Continue with human feedback
    print(f"\nContinuing with human feedback: '{human_input}'")
    result["human_feedback"] = human_input
    
    # Second invocation - will process the feedback
    final_result = app.invoke(result, config)
    
    print(f"\n=== Final Result ===")
    print(f"Question: {final_result['question']}")
    print(f"Human feedback: {final_result['human_feedback']}")
    print(f"Answer: {final_result['answer']}")
    print(f"Status: {final_result['status']}")


if __name__ == "__main__":
    main()
