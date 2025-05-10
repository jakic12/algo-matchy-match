from puzzle import Puzzle, Graph, Node, Edge
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches

COLORS = [
    "#FFFFFF",
    "#0000FF",
    "#00FFFF",
    "#FF00FF",
    "#FF0000",
    "#00FF00",
    "#F0F8FF",
    "#FAEBD7",
    "#00FFFF",
    "#7FFFD4",
    "#F0FFFF",
    "#F5F5DC",
    "#FFE4C4",
    "#FFEBCD",
    "#8A2BE2",
    "#A52A2A",
    "#DEB887",
    "#5F9EA0",
    "#7FFF00",
    "#D2691E",
    "#FF7F50",
    "#6495ED",
    "#FFF8DC",
    "#DC143C",
    "#00008B",
    "#008B8B",
    "#B8860B",
    "#A9A9A9",
    "#A9A9A9",
    "#006400",
    "#BDB76B",
    "#8B008B",
    "#556B2F",
    "#FF8C00",
    "#9932CC",
    "#8B0000",
    "#E9967A",
    "#8FBC8F",
    "#483D8B",
    "#2F4F4F",
    "#2F4F4F",
    "#00CED1",
    "#9400D3",
    "#FF1493",
    "#00BFFF",
    "#696969",
    "#696969",
    "#1E90FF",
    "#B22222",
    "#FFFAF0",
    "#228B22",
    "#DCDCDC",
    "#F8F8FF",
    "#FFD700",
    "#DAA520",
    "#808080",
    "#808080",
    "#008000",
    "#ADFF2F",
    "#F0FFF0",
    "#FF69B4",
    "#CD5C5C",
    "#4B0082",
    "#FFFFF0",
    "#F0E68C",
    "#E6E6FA",
    "#FFF0F5",
    "#7CFC00",
    "#FFFACD",
    "#ADD8E6",
    "#F08080",
    "#E0FFFF",
    "#FAFAD2",
    "#D3D3D3",
    "#D3D3D3",
    "#90EE90",
    "#FFB6C1",
    "#FFA07A",
    "#20B2AA",
    "#87CEFA",
    "#778899",
    "#778899",
    "#B0C4DE",
    "#FFFFE0",
    "#32CD32",
    "#FAF0E6",
    "#FF00FF",
    "#800000",
    "#66CDAA",
    "#0000CD",
    "#BA55D3",
    "#9370DB",
    "#3CB371",
    "#7B68EE",
    "#00FA9A",
    "#48D1CC",
    "#C71585",
    "#191970",
    "#F5FFFA",
    "#FFE4E1",
    "#FFE4B5",
    "#FFDEAD",
    "#000080",
    "#FDF5E6",
    "#808000",
    "#6B8E23",
    "#FFA500",
    "#FF4500",
    "#DA70D6",
    "#EEE8AA",
    "#98FB98",
    "#AFEEEE",
    "#DB7093",
    "#FFEFD5",
    "#FFDAB9",
    "#CD853F",
    "#FFC0CB",
    "#DDA0DD",
    "#B0E0E6",
    "#800080",
    "#663399",
    "#BC8F8F",
    "#4169E1",
    "#8B4513",
    "#FA8072",
    "#F4A460",
    "#2E8B57",
    "#FFF5EE",
    "#A0522D",
    "#C0C0C0",
    "#87CEEB",
    "#6A5ACD",
    "#708090",
    "#708090",
    "#FFFAFA",
    "#00FF7F",
    "#4682B4",
    "#D2B48C",
    "#008080",
    "#D8BFD8",
    "#FF6347",
    "#40E0D0",
    "#EE82EE",
    "#F5DEB3",
    "#F5F5F5",
    "#FFFF00",
    "#9ACD32",
]


def visualize_puzzle(puzzle):
    G = nx.Graph()

    for node in puzzle.graph.nodes:
        G.add_node(node.idx, color=COLORS[node.color])
    for edge in puzzle.graph.edges:
        G.add_edge(edge.idx1, edge.idx2)
    pos = nx.spring_layout(G)
    node_colors = [G.nodes[node]["color"] for node in G.nodes()]
    nx.draw(G, pos, node_color=node_colors, with_labels=True)
    plt.show()

    # visualize match sticks
    match_sticks = puzzle.match_sticks

    fig, ax = plt.subplots(figsize=(4, len(match_sticks)))

    for i, m in enumerate(match_sticks):
        y = len(match_sticks) - i - 1  # Draw from top to bottom

        # Left half
        rect1 = patches.Rectangle(
            (0, y), 0.5, 0.3, facecolor=COLORS[m.color1], edgecolor="black"
        )
        ax.add_patch(rect1)

        # Right half
        rect2 = patches.Rectangle(
            (0.5, y), 0.5, 0.3, facecolor=COLORS[m.color2], edgecolor="black"
        )
        ax.add_patch(rect2)

    # Adjust plot
    ax.set_xlim(0, 1)
    ax.set_ylim(0, len(match_sticks))
    ax.set_aspect("equal")
    ax.axis("off")
    plt.tight_layout()
    plt.show()


def visualize_puzzle_solution(solution):
    puzzle = solution.puzzle
    G = nx.Graph()

    for node in puzzle.graph.nodes:
        G.add_node(node.idx, color=COLORS[node.color])
    for edge in puzzle.graph.edges:
        G.add_edge(edge.idx1, edge.idx2)
    pos = nx.spring_layout(G)
    # draw edge labels
    edge_labels = {}
    print(solution.edge_to_match_stick_idx)
    for edge_idx, match_stick_idx in solution.edge_to_match_stick_idx.items():
        print(edge_idx, match_stick_idx)
        print("edge", puzzle.edges[edge_idx])
        print("node1", puzzle.edges[edge_idx].node1)
        print("node2", puzzle.edges[edge_idx].node2)
        print("match stick", puzzle.match_sticks[match_stick_idx])

        stick = puzzle.match_sticks[match_stick_idx]
        edge_labels[(puzzle.edges[edge_idx].idx1, puzzle.edges[edge_idx].idx2)] = (
            f"{stick.color1}-{stick.color2}"
        )

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    node_colors = [G.nodes[node]["color"] for node in G.nodes()]
    # node labels
    node_labels = {node.idx: f"c:{node.color}" for node in puzzle.graph.nodes}
    nx.draw_networkx_labels(G, pos, labels=node_labels)
    nx.draw(G, pos, node_color=node_colors, with_labels=False)
    plt.show()
