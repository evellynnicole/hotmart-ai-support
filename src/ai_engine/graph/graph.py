from langgraph.graph import END, START, StateGraph

from src.ai_engine.nodes.customer_service_node import CustomerServiceNode
from src.ai_engine.nodes.faq_agent_node import FAQAgentNode
from src.ai_engine.nodes.journey_agent_node import JourneyAgentNode
from src.ai_engine.nodes.router_node import RouterNode
from src.ai_engine.nodes.tools_node import tool_node_faq, tool_node_journey
from src.ai_engine.states.state import ChatGraphState


class ChatGraph:
    def __init__(self):
        self.graph_builder = StateGraph(ChatGraphState)
        self._add_nodes()
        self._add_edges()
        self.graph = self.graph_builder.compile()

    def _should_continue_tools_faq(state: ChatGraphState) -> str:
        messages = state['messages']
        last_message = messages[-1]
        if last_message.tool_calls:
            return 'tools_faq'
        else:
            return END

    def _should_continue_tools_journey(state: ChatGraphState) -> str:
        messages = state['messages']
        last_message = messages[-1]
        if last_message.tool_calls:
            return 'tools_journey'
        else:
            return END

    def _should_continue_router(state: ChatGraphState) -> str:
        router_response = state['router_response']
        if router_response == 'faq':
            return 'faq_agent_node'
        elif router_response == 'journey':
            return 'journey_agent_node'
        elif router_response == 'atendente':
            return 'customer_service_node'
        else:
            return END

    def _add_nodes(self):
        self.graph_builder.add_node('router_node', RouterNode())
        self.graph_builder.add_node('faq_agent_node', FAQAgentNode())
        self.graph_builder.add_node('tools_faq', tool_node_faq)
        self.graph_builder.add_node('tools_journey', tool_node_journey)
        self.graph_builder.add_node('journey_agent_node', JourneyAgentNode())
        self.graph_builder.add_node(
            'customer_service_node', CustomerServiceNode()
        )

    def _add_edges(self):
        self.graph_builder.add_edge(START, 'router_node')
        self.graph_builder.add_conditional_edges(
            'router_node',
            self._should_continue_router,
            ['faq_agent_node', 'journey_agent_node', 'customer_service_node'],
        )
        self.graph_builder.add_edge('tools_faq', 'faq_agent_node')
        self.graph_builder.add_conditional_edges(
            'faq_agent_node',
            self._should_continue_tools_faq,
            ['tools_faq', END],
        )
        self.graph_builder.add_edge('tools_journey', 'journey_agent_node')
        self.graph_builder.add_conditional_edges(
            'journey_agent_node',
            self._should_continue_tools_journey,
            ['tools_journey', END],
        )
        self.graph_builder.add_edge('customer_service_node', END)

    def get_graph(self):
        return self.graph
