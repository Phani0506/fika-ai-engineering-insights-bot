from typing import TypedDict, Dict, Any
from langgraph.graph import StateGraph, END
from app.agents import data_harvester_node, diff_analyst_node, insight_narrator_node

class GraphState(TypedDict):
    """
    Represents the state of our graph.
    This dictionary is passed between all the nodes.
    """
    period: str
    raw_data: Dict[str, Any]
    analyzed_data: Dict[str, Any]
    narrative: str

def create_graph():
    """Creates and compiles the LangGraph agent workflow."""
    workflow = StateGraph(GraphState)

    # Define the nodes (the three agent functions)
    workflow.add_node("harvester", data_harvester_node)
    workflow.add_node("analyst", diff_analyst_node)
    workflow.add_node("narrator", insight_narrator_node)

    # Define the edges (the connections between the agents)
    # This creates the sequence: Harvester -> Analyst -> Narrator -> End
    workflow.set_entry_point("harvester")
    workflow.add_edge("harvester", "analyst")
    workflow.add_edge("analyst", "narrator")
    workflow.add_edge("narrator", END)

    # Compile the graph into a runnable object
    app_graph = workflow.compile()
    print("✅ LangGraph compiled successfully.")
    return app_graph

# Create a single, reusable instance of the graph
graph = create_graph()