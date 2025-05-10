# This is an implementation of the match match game.
# The game provides a list of match sticks that have two colored ends and a
# planar graph with some of the nodes colored.
# The goal is to place the match sticks on the edges of the graph such that
# the colored ends of the match sticks match the colors of the nodes they
# are connected to.

# Constraints:
# 1. Each match stick can only be placed on one edge of the graph.
# 2. Each edge can only have one match stick placed on it.
# 3. The colors of the match sticks must match the colors of the nodes they
# are connected to.
# 4. The number of match sticks must be equal to the number of edges in the graph.

import random
import numpy as np


class Node:
    # if color is 0, it means it is not colored
    def __init__(self, idx, color=0):
        self.idx = idx
        self.color = color

    def __repr__(self):
        return f"Node({self.idx}, {self.color})"


class Edge:
    def __init__(self, idx1, idx2):
        self.idx1 = idx1
        self.idx2 = idx2
        self.node1 = None
        self.node2 = None

    def __repr__(self):
        return f"Edge({self.idx1}, {self.idx2})"


class MatchStick:
    def __init__(self, color1, color2):
        self.color1 = color1
        self.color2 = color2

        if color1 == 0 and color2 == 0:
            raise ValueError("Match stick cannot be uncolored")

    def copy(self):
        return MatchStick(self.color1, self.color2)

    def flip(self):
        self.color1, self.color2 = self.color2, self.color1

    def __repr__(self):
        return f"MatchStick({self.color1}, {self.color2})"


class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.neighbors = {}

    def calculate_neighbors(self, new_edge=None):
        if new_edge is not None:
            new_edges = [new_edge]
        else:
            new_edges = self.edges

        for edge in new_edges:
            if edge.idx1 not in self.neighbors:
                self.neighbors[edge.idx1] = []
            if edge.idx2 not in self.neighbors:
                self.neighbors[edge.idx2] = []
            self.neighbors[edge.idx1].append(edge.idx2)
            self.neighbors[edge.idx2].append(edge.idx1)

    def add_nodes(self, color):
        node = Node(len(self.nodes), color)
        self.nodes.append(node)
        return node

    def set_edges(self, edges):
        self.edges = edges
        for e in edges:
            e.node1 = self.nodes[e.idx1]
            e.node2 = self.nodes[e.idx2]
        self.calculate_neighbors()

    def copy(self):
        new_graph = Graph()
        new_graph.nodes = [Node(node.idx, node.color) for node in self.nodes]
        new_graph.edges = []
        for edge in self.edges:
            new_edge = Edge(edge.idx1, edge.idx2)
            new_edge.node1 = new_graph.nodes[edge.idx1]
            new_edge.node2 = new_graph.nodes[edge.idx2]
            new_graph.edges.append(new_edge)
        new_graph.set_edges(new_graph.edges)
        return new_graph

    def __repr__(self):
        return f"Graph(nodes={self.nodes}, edges={self.edges})"


class Puzzle:
    def __init__(self, colors, graph, match_sticks):
        self.colors = colors
        self.graph = graph
        self.edges = graph.edges
        self.nodes = graph.nodes
        self.match_sticks = match_sticks

    def __repr__(self):
        return f"Puzzle(graph={self.graph}, match_sticks={self.match_sticks})"

    def copy(self):
        return Puzzle(
            self.colors.copy(), self.graph.copy(), [i.copy() for i in self.match_sticks]
        )


class PuzzleSolution:
    def __init__(self, puzzle, edge_to_match_stick_idx):
        self.puzzle = puzzle
        self.edge_to_match_stick_idx = edge_to_match_stick_idx

    def confirm_solution(self):
        puzzle_copy = self.puzzle.copy()
        # check if every edge has a match stick
        # and check if match sticks are not used more than once
        match_stick_used = set()
        for i, edge in enumerate(puzzle_copy.edges):
            if i not in self.edge_to_match_stick_idx:
                print(f"Edge {i} {edge} does not have a match stick assigned to it")
                return False
            match_stick_idx = self.edge_to_match_stick_idx[i]
            if match_stick_idx in match_stick_used:
                print(f"Match stick {match_stick_idx} is used more than once")
                return False
            match_stick_used.add(match_stick_idx)

        # check if all of the colors of the match sticks match the colors of the nodes
        for edge_idx, match_stick_idx in self.edge_to_match_stick_idx.items():
            edge = puzzle_copy.edges[edge_idx]
            node1 = edge.node1
            node2 = edge.node2
            match_stick = puzzle_copy.match_sticks[match_stick_idx]

            # if color is 0, it means it is not colored
            if node1.color == 0:
                node1.color = match_stick.color1
            if node2.color == 0:
                node2.color = match_stick.color2

            if (node1.color == match_stick.color1) and (
                node2.color == match_stick.color2
            ):
                continue
            else:
                return False
        return True

    def __repr__(self):
        return f"PuzzleSolution(puzzle={self.puzzle}, edge_to_match_stick_idx={self.edge_to_match_stick_idx})"


def generate_complete_graph_puzzle(num_nodes, number_of_uncolored_nodes):
    # Generate a complete graph with num_nodes nodes and assign
    # random colors to the nodes

    # randomly sample colors for all nodes
    colors = np.random.choice(range(1, num_nodes + 1), num_nodes).tolist()

    # reindex the colors so that none of the colors are skipped
    color_map = {color: rank + 1 for rank, color in enumerate(sorted(set(colors)))}
    colors = [color_map[color] for color in colors]

    graph = Graph()
    for i in range(num_nodes):
        graph.add_nodes(colors[i])
    edges = []
    match_sticks = []
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            edges.append(Edge(i, j))
            match_sticks.append(MatchStick(graph.nodes[i].color, graph.nodes[j].color))
    graph.set_edges(edges)

    # Mask the colors of the nodes
    uncolored_nodes = random.sample(range(num_nodes), number_of_uncolored_nodes)
    for i in uncolored_nodes:
        graph.nodes[i].color = 0

    return Puzzle(sorted(set(colors)), graph, match_sticks)


def solve_complete_graph_puzzle(puzzle):
    puzzle_copy = puzzle.copy()
    # In the set of sticks we count the number of appearances of each color
    matchstick_color_count = {}
    matchsticks_by_colors = {}
    for i, match_stick in enumerate(puzzle_copy.match_sticks):  # O(m)
        matchstick_color_count[match_stick.color1] = (
            matchstick_color_count.get(match_stick.color1, 0) + 1
        )
        matchstick_color_count[match_stick.color2] = (
            matchstick_color_count.get(match_stick.color2, 0) + 1
        )

        matchsticks_by_colors.setdefault(match_stick.color1, {}).setdefault(
            match_stick.color2, []
        ).append(i)
        if match_stick.color1 != match_stick.color2:
            matchsticks_by_colors.setdefault(match_stick.color2, {}).setdefault(
                match_stick.color1, []
            ).append(i)

    # Each color in the graph can appear at most max_color_count[color] times
    max_color_count = {
        color: matchstick_color_count[color] / (len(puzzle_copy.graph.nodes) - 1)
        for color in matchstick_color_count
    }  # O(m)

    graph_color_count = {}
    uncolored_nodes = []
    for node in puzzle_copy.graph.nodes:  # O(n)
        if node.color == 0:
            uncolored_nodes.append(node)
        else:
            graph_color_count[node.color] = graph_color_count.get(node.color, 0) + 1

    colors_to_distribute = []
    for color in puzzle_copy.colors:  # O(m)
        available = max_color_count[color] - graph_color_count.get(color, 0)
        if available > 0:
            # append the color how many times it needs to be added
            colors_to_distribute += [color] * int(available)

    # color the uncolored nodes
    for node in uncolored_nodes:  # O(uncolored_nodes)
        if len(colors_to_distribute) == 0:
            break
        node.color = colors_to_distribute.pop()

    # assign match sticks to edges
    edge_to_match_stick_idx = {}
    for i, edge in enumerate(puzzle_copy.edges):  # O(m)
        edge_to_match_stick_idx[i] = matchsticks_by_colors[edge.node1.color][
            edge.node2.color
        ].pop()

        if (
            puzzle_copy.match_sticks[edge_to_match_stick_idx[i]].color1
            != edge.node1.color
        ):
            puzzle_copy.match_sticks[edge_to_match_stick_idx[i]].flip()

        if edge.node1.color != edge.node2.color:
            matchsticks_by_colors[edge.node2.color][edge.node1.color].remove(
                edge_to_match_stick_idx[i]
            )

    return PuzzleSolution(puzzle_copy, edge_to_match_stick_idx)
