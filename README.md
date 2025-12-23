# langGraph-playground

A playground repository for experimenting with LangGraph agents.

## Overview

This repository contains examples of agents built using LangGraph, a framework for building stateful, multi-actor applications with LLMs.

## Simple Agent

The `simple_agent.py` file demonstrates a basic agent implementation that:
- Maintains conversation state
- Processes user messages
- Returns responses in a stateful manner

### Setup

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

### Usage

Run the simple agent example:
```bash
python simple_agent.py
```

You can also import and use the agent in your own code:
```python
from simple_agent import run_simple_agent, create_simple_agent

# Quick usage
response = run_simple_agent("Hello!")
print(response)

# Or create and use the agent directly
app = create_simple_agent()
result = app.invoke({"messages": [{"role": "user", "content": "Hi!"}]})
print(result["messages"][-1].content)
```

## Features

- **Simple State Management**: Uses LangGraph's StateGraph for managing conversation state
- **Message Handling**: Leverages LangGraph's message annotation system
- **Easy to Extend**: Built as a foundation for more complex agent implementations

## Requirements

- Python 3.8+
- LangGraph 0.2.0+
- LangChain 0.3.0+

## License

MIT