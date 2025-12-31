from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# -----------------------------
# 1. Define State (shared memory)
# -----------------------------
class GraphState(TypedDict):
    question: str
    answer: str

# -----------------------------
# 2. Initialize LLM
# -----------------------------
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# -----------------------------
# 3. Define Node Functions
# -----------------------------
def ask_llm(state: GraphState):
    response = llm([
        HumanMessage(content=state["question"])
    ])
    return {"answer": response.content}

# -----------------------------
# 4. Build Graph
# -----------------------------
builder = StateGraph(GraphState)

builder.add_node("llm_node", ask_llm)

builder.set_entry_point("llm_node")
builder.add_edge("llm_node", END)

graph = builder.compile()

# -----------------------------
# 5. Run Graph
# -----------------------------
result = graph.invoke({
    "question": "Explain LangGraph in simple words"
})

print("Answer:", result["answer"])
