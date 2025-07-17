from langgraph.prebuilt import ToolNode

from src.ai_engine.tools import tools_faq, tools_journey

tool_node_faq = ToolNode(tools_faq)
tool_node_journey = ToolNode(tools_journey)
