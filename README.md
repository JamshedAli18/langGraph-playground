# LangGraph Playground

A collection of simple and practical examples demonstrating various LangGraph patterns and capabilities.

## 📋 Overview

This repository contains hands-on examples for learning and experimenting with [LangGraph](https://github.com/langchain-ai/langgraph), a library for building stateful, multi-agent applications with LLMs.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/JamshedAli18/langGraph-playground.git
cd langGraph-playground
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional) Set up environment variables for examples that use LLMs:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

## 📚 Examples

### 1. Simple Sequential Chain
**File:** `examples/01_simple_sequential_chain.py`

Demonstrates a basic LangGraph with nodes executing in sequence. Each node transforms the state before passing it to the next node.

**Key Concepts:**
- Basic state definition
- Sequential node execution
- State transformation

**Run:**
```bash
python examples/01_simple_sequential_chain.py
```

### 2. Conditional Branching
**File:** `examples/02_conditional_branching.py`

Shows how to implement conditional routing based on state values. The graph takes different paths depending on the conditions.

**Key Concepts:**
- Conditional edges
- Dynamic routing
- Multiple execution paths

**Run:**
```bash
python examples/02_conditional_branching.py
```

### 3. Cyclic Graph with State
**File:** `examples/03_cyclic_graph.py`

Demonstrates a graph with cycles that loops until a condition is met, showing state management across iterations.

**Key Concepts:**
- Graph cycles
- Loop conditions
- State accumulation

**Run:**
```bash
python examples/03_cyclic_graph.py
```

### 4. Human-in-the-Loop
**File:** `examples/04_human_in_the_loop.py`

Shows how to interrupt graph execution to wait for human input, useful for approval workflows or interactive applications.

**Key Concepts:**
- Graph interruption
- Checkpointing
- Human feedback integration

**Run:**
```bash
python examples/04_human_in_the_loop.py
```

### 5. Parallel Processing
**File:** `examples/05_parallel_processing.py`

Demonstrates parallel node execution where multiple nodes process data simultaneously and results are merged.

**Key Concepts:**
- Parallel execution
- Multiple entry points
- Result aggregation

**Run:**
```bash
python examples/05_parallel_processing.py
```

## 🛠️ Project Structure

```
langGraph-playground/
├── examples/
│   ├── 01_simple_sequential_chain.py
│   ├── 02_conditional_branching.py
│   ├── 03_cyclic_graph.py
│   ├── 04_human_in_the_loop.py
│   └── 05_parallel_processing.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 📖 Learning Path

If you're new to LangGraph, we recommend following the examples in order:

1. Start with **Simple Sequential Chain** to understand basic concepts
2. Move to **Conditional Branching** to learn about routing
3. Explore **Cyclic Graph** to see how loops work
4. Try **Human-in-the-Loop** for interactive patterns
5. Finally, check **Parallel Processing** for advanced patterns

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add new examples
- Improve existing examples
- Fix bugs or typos
- Enhance documentation

## 📝 License

This project is open source and available under the MIT License.

## 🔗 Resources

- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph GitHub](https://github.com/langchain-ai/langgraph)

## 💡 Tips

- Each example is self-contained and can run independently
- Examples use print statements to show execution flow
- State is explicitly defined using TypedDict for clarity
- All examples include detailed comments explaining the concepts