"""
Advanced example demonstrating the simple agent with state management.

This example shows how to use the agent with persistent state across multiple turns.
"""

from simple_agent import create_simple_agent


def interactive_conversation():
    """
    Run an interactive conversation with the agent.
    """
    print("Simple Agent - Interactive Mode")
    print("=" * 50)
    print("Type 'exit' or 'quit' to end the conversation\n")
    
    # Create the agent
    app = create_simple_agent()
    
    # Initialize conversation state
    state = {"messages": []}
    
    while True:
        # Get user input
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        # Add user message to state
        state["messages"].append({"role": "user", "content": user_input})
        
        # Run the agent
        result = app.invoke(state)
        
        # Update state with the result
        state = result
        
        # Display the agent's response
        if result["messages"]:
            last_message = result["messages"][-1]
            print(f"Agent: {last_message.content}\n")


def batch_conversation():
    """
    Demonstrate processing multiple messages in a batch.
    """
    print("\nSimple Agent - Batch Processing Example")
    print("=" * 50)
    
    # Create the agent
    app = create_simple_agent()
    
    # List of messages to process
    messages = [
        "Hello, nice to meet you!",
        "Can you help me?",
        "This is a test message.",
        "What is your purpose?",
        "Thank you for your help!"
    ]
    
    # Process each message
    state = {"messages": []}
    
    for msg in messages:
        # Add user message
        state["messages"].append({"role": "user", "content": msg})
        
        # Get response
        result = app.invoke(state)
        state = result
        
        # Display conversation
        print(f"User: {msg}")
        if result["messages"]:
            print(f"Agent: {result['messages'][-1].content}\n")


if __name__ == "__main__":
    # Run batch example first
    batch_conversation()
    
    # Then run interactive mode
    print("\n" + "=" * 50)
    response = input("\nWould you like to try interactive mode? (y/n): ")
    if response.lower() in ['y', 'yes']:
        interactive_conversation()
