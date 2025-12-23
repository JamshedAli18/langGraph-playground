# Example Files

This directory contains working code examples demonstrating LangGraph concepts.

## Structure

- `basic/` - Fundamental examples for beginners
- `intermediate/` - More complex patterns
- `advanced/` - Production-ready patterns and agent systems

## Installation

Before running examples, install the required dependencies:

```bash
pip install -r ../requirements.txt
```

Or install individual packages:

```bash
pip install langgraph langchain langchain-openai
```

## Running Examples

### Basic Examples
```bash
cd basic
python 01_sequential_graph.py
python 02_conditional_routing.py
python 03_state_accumulation.py
```

### Intermediate Examples
```bash
cd intermediate
python 01_loop_with_exit.py
```

### Advanced Examples
```bash
cd advanced
python 01_simple_agent.py
```

## Learning Path

1. Start with `basic/01_sequential_graph.py` - Learn the fundamentals
2. Progress to `basic/02_conditional_routing.py` - Understand branching
3. Try `basic/03_state_accumulation.py` - Master state management
4. Move to `intermediate/01_loop_with_exit.py` - Learn about cycles
5. Challenge yourself with `advanced/01_simple_agent.py` - Build agents

## Example Descriptions

### Basic Examples

#### 01_sequential_graph.py
A simple linear flow through multiple processing steps. Perfect for understanding:
- State definition
- Node creation
- Edge connections
- Graph execution

#### 02_conditional_routing.py
Demonstrates dynamic routing based on state values. Learn:
- Conditional edges
- Router functions
- Multiple execution paths

#### 03_state_accumulation.py
Shows how to accumulate data across nodes using reducers. Covers:
- State reducers (operator.add)
- List accumulation
- Progress tracking

### Intermediate Examples

#### 01_loop_with_exit.py
Implements a loop with an exit condition. Understand:
- Cycles in graphs
- Exit conditions
- Iterative processing

### Advanced Examples

#### 01_simple_agent.py
A basic agent that can reason and use tools. Explore:
- Agent decision-making
- Tool calling
- ReAct pattern
- Multi-step workflows

## Tips

- Read the code comments for detailed explanations
- Modify examples to experiment
- Use print statements to understand flow
- Test with different inputs

## Need Help?

- Check the [documentation](../docs/)
- Review the [Getting Started guide](../docs/GETTING_STARTED.md)
- See [Resources](../docs/RESOURCES.md) for more information
