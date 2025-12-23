"""
Advanced Example: Simple Agent with Tools

This example demonstrates a basic agent pattern that can:
1. Decide whether it needs to use a tool
2. Use tools when needed
3. Provide a final answer

Concepts covered:
- Agent reasoning loop
- Tool calling
- Decision-making
- Multi-step workflows
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END


# Define state
class AgentState(TypedDict):
    """State for the agent."""
    question: str
    thought: str
    action: str
    observation: str
    answer: str
    iterations: int
    max_iterations: int


# Simulated tools
def calculator_tool(expression: str) -> str:
    """Simple calculator tool.
    
    Note: In a production environment, use a proper math parser
    or library like 'numexpr' or 'simpleeval' for safe evaluation.
    """
    # For demonstration, we'll handle simple operations safely
    try:
        # Remove whitespace
        expression = expression.strip()
        
        # Basic validation - only allow numbers and basic operators
        allowed_chars = set('0123456789+-*/(). ')
        if not all(c in allowed_chars for c in expression):
            return "Error: Invalid characters in expression"
        
        # Use ast.literal_eval for safer evaluation of simple expressions
        # Note: This is still limited; for production use a proper math parser
        import ast
        import operator
        
        # Simple expression parser for basic operations
        operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv
        }
        
        def eval_expr(node):
            if isinstance(node, ast.Constant):  # <number>
                return node.value
            elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
                return operators[type(node.op)](eval_expr(node.left), eval_expr(node.right))
            elif isinstance(node, ast.UnaryOp):  # <operator> <operand>
                return operators[type(node.op)](eval_expr(node.operand))
            else:
                raise TypeError(node)
        
        result = eval_expr(ast.parse(expression, mode='eval').body)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: Could not evaluate expression. {str(e)}"


def search_tool(query: str) -> str:
    """Simulated search tool."""
    # In reality, this would call an actual search API
    return f"Search results for '{query}': [Simulated information about {query}]"


# Node functions
def agent_think(state: AgentState) -> dict:
    """
    Agent decides what to do next.
    
    In a real implementation, this would use an LLM.
    """
    question = state["question"]
    iterations = state["iterations"]
    
    print(f"\n--- Iteration {iterations + 1} ---")
    print(f"Question: {question}")
    
    # Simple logic to demonstrate the pattern
    # In reality, an LLM would make this decision
    if "calculate" in question.lower() or "+" in question or "*" in question:
        thought = "I need to use the calculator tool"
        action = "calculator"
    elif "search" in question.lower() or "what is" in question.lower():
        thought = "I need to search for information"
        action = "search"
    else:
        thought = "I can answer this directly"
        action = "finish"
    
    print(f"Thought: {thought}")
    print(f"Action: {action}")
    
    return {
        "thought": thought,
        "action": action,
        "iterations": iterations + 1
    }


def use_tool(state: AgentState) -> dict:
    """Execute the chosen tool."""
    action = state["action"]
    question = state["question"]
    
    if action == "calculator":
        # Extract expression from question (simplified)
        # In reality, LLM would extract this
        observation = calculator_tool("10 + 5")
    elif action == "search":
        observation = search_tool(question)
    else:
        observation = "No tool needed"
    
    print(f"Observation: {observation}")
    
    return {"observation": observation}


def finalize_answer(state: AgentState) -> dict:
    """Generate final answer."""
    observation = state.get("observation", "")
    answer = f"Based on my analysis: {observation}"
    
    print(f"Final Answer: {answer}")
    
    return {"answer": answer}


# Router function
def should_continue(state: AgentState) -> Literal["use_tool", "finish"]:
    """
    Decide whether to use a tool or finish.
    """
    action = state["action"]
    iterations = state["iterations"]
    max_iterations = state["max_iterations"]
    
    # Safety check: prevent infinite loops
    if iterations >= max_iterations:
        return "finish"
    
    if action == "finish":
        return "finish"
    else:
        return "use_tool"


# Build graph
def create_agent_graph():
    """Create the agent graph."""
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("think", agent_think)
    workflow.add_node("use_tool", use_tool)
    workflow.add_node("finalize", finalize_answer)
    
    # Set entry point
    workflow.set_entry_point("think")
    
    # Add conditional edge from thinking
    workflow.add_conditional_edges(
        "think",
        should_continue,
        {
            "use_tool": "use_tool",
            "finish": "finalize"
        }
    )
    
    # After using tool, go back to thinking
    workflow.add_edge("use_tool", "think")
    
    # End after finalizing
    workflow.add_edge("finalize", END)
    
    return workflow.compile()


# Run examples
def main():
    """Test the agent with different questions."""
    app = create_agent_graph()
    
    questions = [
        "What is the capital of France?",
        "Calculate 10 + 5",
        "Search for information about LangGraph"
    ]
    
    for question in questions:
        print("\n" + "=" * 70)
        print(f"QUESTION: {question}")
        print("=" * 70)
        
        result = app.invoke({
            "question": question,
            "thought": "",
            "action": "",
            "observation": "",
            "answer": "",
            "iterations": 0,
            "max_iterations": 3
        })
        
        print("\n" + "-" * 70)
        print(f"ANSWER: {result['answer']}")


if __name__ == "__main__":
    main()
