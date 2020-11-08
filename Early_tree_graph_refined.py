# Refined Early Tree with plot#

from ImportGraph import import_graph
from PluginGraph.Plotter import *


def forward_pass(graph, client_algorithm="RS", file_name="Not informed!"):
    """
    This function in which the earliest completion time for each activity is computed based on traditional forward
    pass critical path calculations which allows for the construction of the corresponding early tree Forward_Backward.
    Using to denote the earliest finish time of activity j and to denote the set of its immediate predecessors.
    The original version of this function is described in section 2.1.2 on page 144 of the book
    "Project Scheduling: A Research Handbook" by authors Demeulemeester and Herroelen.

    :param graph: networkx
            The original graph with all constraints

    :param client_algorithm: str
            Three client algorithms can use the result of this function: Recursive Search "RS",
            Steepest Ascent Approach "SAA", and Hybrid Search "HS". When the client algorithm is "RS",
            the final dummy is used to represent the deadline. In this case, the final dummy is connected
            to the start dummy, in the early tree. But when clients are "SAA" and "HS",
            the final dummy is anticipated as much as possible and there is no edge between
            it and the initial dummy in the early tree.

    :param file_name: str
            Name of the file that is data source

    :return:
            early_tree: networkx
    """

    # Copies the graph on the early_tree and remove all edges
    early_tree = graph.copy()
    early_tree.deadline = graph.deadline
    early_tree.file_name = file_name
    early_tree.remove_edges_from(graph.edges)

    # Defines start dummy earliest start with 0
    early_tree.nodes[1]['EF'] = 0

    # When the client is RS:
    # .Add an edge between start and end dummies
    # .The final dummy is the deadline
    # .The final dummy is not anticipated.
    if client_algorithm == "RS":
        early_tree.add_edge(early_tree.number_of_nodes(), 1)
        early_tree.nodes[early_tree.number_of_nodes()]['EF'] = graph.deadline
        number_of_nodes = early_tree.number_of_nodes()
    else:
        # The final dummy is anticipated. The increment of 1 is necessary, because the range function works with
        # an open interval on the right side.
        # For SAA and HS, an extra arc between dummies is used with negative lag.
        graph.add_edge(early_tree.number_of_nodes(), 1)
        number_of_nodes = early_tree.number_of_nodes() + 1

    # The problem treated assumes that the activities have zero lag. Thus, the constraint closest to the initial
    # dummy is arbitrarily defined as activity 2.
    early_tree.nodes[1]['NODE_MIN_CONSTRAINT'] = 2

    # Apply anticipated
    for j in range(2, number_of_nodes):
        early_tree.nodes[j]['NODE_MIN_CONSTRAINT'] = early_tree.number_of_nodes()

        early_tree.nodes[j]['EF'] = 0
        for i in graph.predecessors(j):
            if (early_tree.nodes[i]['EF'] + early_tree.nodes[j]['DURATION']) > (early_tree.nodes[j]['EF']):
                early_tree.nodes[j]['EF'] = early_tree.nodes[i]['EF'] + early_tree.nodes[j]['DURATION']
                i_star = i
        early_tree.add_edge(i_star, j)
    for j in range(2, number_of_nodes):
        for i in graph.successors(j):
            ES_i = early_tree.nodes[i]['EF'] - early_tree.nodes[i]['DURATION']
            ES_j = early_tree.nodes[early_tree.nodes[j]['NODE_MIN_CONSTRAINT']]['EF'] - early_tree.nodes[early_tree.nodes[j]['NODE_MIN_CONSTRAINT']]['DURATION']
            # if (early_tree.nodes[i]['EF'] - early_tree.nodes[i]['DURATION']) < \
            #         (early_tree.nodes[early_tree.nodes[j]['NODE_MIN_CONSTRAINT']]['EF'] -
            #          early_tree.nodes[early_tree.nodes[j]['NODE_MIN_CONSTRAINT']]['DURATION']):
            #     early_tree.nodes[j]['NODE_MIN_CONSTRAINT'] = i
            if ES_i < ES_j:
                early_tree.nodes[j]['NODE_MIN_CONSTRAINT'] = i

        early_tree.nodes[early_tree.number_of_nodes()]['NODE_MIN_CONSTRAINT'] = 1
    #plt_general("Early Tree", 0.00, early_tree)
    # for node in early_tree.nodes:
    #     print('node: ', node, ' EF: ', early_tree.nodes[node]['EF'])
    return early_tree


def main(algo):
    #pkg_graph = import_graph('../amostra2_07072020')
    #pkg_graph = import_graph('../amostra_lote3')
    # pkg_graph = import_graph('../Samples')

    for current_file_name, original_graph in pkg_graph.items():
        et = forward_pass(original_graph, algo, current_file_name)

    #plt_17("Early Tree", 0.00, et)
    #plt_general("Early Tree", 0.00, et)

    return et, original_graph