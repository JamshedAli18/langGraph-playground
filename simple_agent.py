"""
Simple Agent using LangGraph

This module demonstrates a basic agent implementation using LangGraph.
The agent can process messages and maintain conversation state.
"""

from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """State definition for the agent."""
    messages: Annotated[list, add_messages]


def chatbot(state: AgentState) -> AgentState:
    """
    Simple chatbot function that echoes back messages.
    
    Args:
        state: Current agent state containing messages
        
    Returns:
        Updated state with response message
    """
    messages = state["messages"]
    
    if not messages:
        return state
    
    # Get the last user message
    last_message = messages[-1]
    
    # Create a simple response
    response = f"Echo: {last_message.content}"
    
    return {"messages": [{"role": "assistant", "content": response}]}


def create_simple_agent():
    """
    Creates and configures a simple agent graph.
    
    Returns:
        Compiled graph representing the agent
    """
    # Create the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("chatbot", chatbot)
    
    # Set entry point
    workflow.set_entry_point("chatbot")
    
    # Add edge to end
    workflow.add_edge("chatbot", END)
    
    # Compile the graph
    app = workflow.compile()
    
    return app


def run_simple_agent(user_input: str) -> str:
    """
    Run the simple agent with a user input.
    
    Args:
        user_input: The user's message
        
    Returns:
        The agent's response
    """
    app = create_simple_agent()
    
    # Create initial state with user message
    initial_state = {
        "messages": [{"role": "user", "content": user_input}]
    }
    
    # Run the agent
    result = app.invoke(initial_state)
    
    # Get the last message (response)
    if result["messages"]:
        return result["messages"][-1].content
    
    return "No response"


if __name__ == "__main__":
    # Example usage
    print("Simple Agent Example")
    print("=" * 50)
    
    # Test the agent with a few messages
    test_messages = [
        "Hello!",
        "How are you?",
        "What can you do?"
    ]
    
    for msg in test_messages:
        print(f"\nUser: {msg}")
        response = run_simple_agent(msg)
        print(f"Agent: {response}")
