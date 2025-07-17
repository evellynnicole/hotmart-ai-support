"""LangGraph Graph visualization tool"""

import os

from langchain_core.runnables.graph import (
    CurveStyle,
    MermaidDrawMethod,
    NodeStyles,
)
from langgraph.graph import StateGraph


def save_graph_visualization(
    graph: StateGraph,
    output_dir: str = 'src/ai_engine/graph_visualization',
    generate_png: bool = True,
):
    """
    Save both Mermaid syntax and optionally PNG visualization of the graph.

    Args:
        graph: The StateGraph to visualize
        output_dir: Directory to save visualizations
        generate_png: Generating PNG visualization (default: True)
    """
    os.makedirs(output_dir, exist_ok=True)

    mermaid_syntax = graph.get_graph().draw_mermaid()

    mermaid_file = os.path.join(output_dir, 'chat_flow.mmd')
    with open(mermaid_file, 'w', encoding='utf-8') as f:
        f.write(mermaid_syntax)

    print(f'Saved Mermaid syntax to: {mermaid_file}')

    if generate_png:
        try:
            png_data = graph.get_graph().draw_mermaid_png(
                draw_method=MermaidDrawMethod.API,
                curve_style=CurveStyle.LINEAR,
                node_colors=NodeStyles(
                    first='#ffdfba',
                    last='#baffc9',
                    default='#f2f0ff',
                ),
                wrap_label_n_words=9,
            )

            png_file = os.path.join(output_dir, 'chat_flow.png')
            with open(png_file, 'wb') as f:
                f.write(png_data)
            print(f'Saved PNG visualization to: {png_file}')
        except Exception as e:
            print(f'Warning: Failed to generate PNG visualization: {str(e)}')
            print(
                'Skipping PNG generation. You can still use the Mermaid'
            )
