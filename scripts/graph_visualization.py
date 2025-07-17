from src.ai_engine.graph.graph import ChatGraph
from src.ai_engine.graph_visualization.graph_visualization import (
    save_graph_visualization,
)

chat_graph = ChatGraph().get_graph()
save_graph_visualization(chat_graph)
