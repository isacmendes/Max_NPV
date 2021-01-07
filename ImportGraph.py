from os import listdir
from os.path import isfile, join
import time

import networkx as nx
import matplotlib.pyplot as plt
import os
import numpy as np

def import_graph(my_path):
    all_files = [f for f in listdir(my_path) if isfile(join(my_path, f))]
    pkg_graph = dict()
    for current_file_name in all_files:
        if current_file_name.split(".")[1] != 'tpf':
            continue
        else:
            try:
                # New graph
                graph = nx.DiGraph()

                # Open current file
                file = open(my_path + '/' + current_file_name, 'r')
                file_lines = file.readlines()

                # Get discounted rate
                graph.discounted_rate = float(my_path.split('-')[-3])

                # Get deadline
                if file_lines[0].split()[1] == 'E1':
                    graph.deadline = 1000
                else:
                    graph.deadline = int(file_lines[0].split()[1])
                nr_nodes = int(file_lines[0].split()[0])

                # Add nodes on graph and define Cash Flow (CF) for start dummy
                graph.add_nodes_from(range(1, nr_nodes))
                graph.nodes[1]['CF'] = 0
                graph.name = current_file_name

                # Add edges
                for line in file_lines[1: nr_nodes + 1]:
                    if int(line.split()[0]) != nr_nodes:
                        for succ in line.split()[2:]:
                            graph.add_edge(int(line.split()[0]), int(succ))

                # Add 'DURATION', 'CASH FLOW (CF)', 'EARLIEST_START (ES)', and 'EARLIEST_FINISH (EF)'.
                for line in file_lines[nr_nodes + 1: 2 * nr_nodes + 1]:
                    node = int(line.split()[0])
                    graph.nodes[node]['DURATION'] = int(line.split()[1])
                    graph.nodes[node]['CF'] = float(line.split()[2])
                    graph.nodes[node]['ES'] = 0
                    graph.nodes[node]['EF'] = 0

                # Show some attributes
                # print('Deadline is: %d' % graph.deadline)
                # for node in range(1, graph.number_of_nodes() + 1):
                #    print('Node: ', node, ', Duration:', graph.nodes[node]['DURATION'], ' CF: ', graph.nodes[node]['CF'])

                # Customizes the node labels
                # custom_labels_1, custom_labels_2 = dict(), dict()
                # for node in graph.nodes:
                #     # Node and duration
                #     custom_labels_1[node] = str(node) + ') ' + str(graph.nodes[node]['DURATION'])
                #     # Node, duration and cash
                #     custom_labels_2[node] = str(node) + ') ' + str(graph.nodes[node]['DURATION']) + ": " + str(graph.nodes[node]['CF'])

                # Plot the graph
                #nx.draw_networkx(graph, nx.circular_layout(graph), with_labels=True)
                # nx.draw_networkx(graph, pos, with_labels=True)
                # nx.draw_networkx(graph, nx.fruchterman_reingold_layout(graph), with_labels=True)
                # #nx.draw_networkx(graph, nx.circular_layout(graph), with_labels=True, labels=custom_labels_2)
                #nx.draw_networkx(graph, nx.planar_layout(graph), with_labels=True)
                #
                #plt.title('Original Graph\n File name: ' + current_file_name)
                # plt.text(-1.4, -1.4, 'Duration:')
                # plt.text(-1.4, -1.5, [graph.nodes[node]['DURATION'] for node in graph.nodes], size=9)
                # plt.text(-1.4, -1.7, 'Cash flow:')
                # plt.text(-1.4, -1.8, [graph.nodes[node]['CF'] for node in graph.nodes], size=9)
                #plt.show()
                # print(file.name)

                # Add current graph on the package
                pkg_graph[current_file_name] = graph
                print("On the file: ", graph.name)
                print("Number of nodes is: ", len(graph.nodes))
                print("Number of edges is: ", len(graph.edges))
            except Exception as e:
                print("Problems with file: '%s'" % file.name)
                print("The error is: %s" % e)
            finally:
                file.close()

    return pkg_graph

#############
# Unit test #
#############
# t1 = time.time()
# #pkg_graph = import_graph('amostra_lote3')
# pkg_graph = import_graph('amostra2_07072020')
# t2 = time.time()
# print(len(pkg_graph), ' time: ', t2 - t1)
# print('Imported files:')
# [print(g) for g in pkg_graph.keys()]

#pkg_graph = import_graph('Samples/temp')