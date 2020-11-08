import numpy as np
import pandas as pd
import networkx as nx
from PluginGraph.Plotter import *
import igraph as ig
import time

t1 = time.time()

def Write_File(nr_graph,
               graph,
               MIN_DUR=5,
               MAX_DUR=10,
               MIN_CF=-100,
               MAX_CF=100,
               CP_MULT=1):

    # Write nodes successors
    print('#' * 50)
    try:
        #i_file = open("../Samples/Lotes_2a_Rodada/Lote_1/dg0%d.tpf" %(nr_graph+1), "w")
        i_file = open("../Samples/dg0%d.tpf" %(nr_graph+1), "w")

        print(len(graph.vs), 'E'+str(CP_MULT))
        i_file.write(str(len(graph.vs)) + ' ' + 'E'+str(CP_MULT) + '\n')
        for node in range(len(graph.vs)):
            row = ""
            if len(graph.successors(node)) > 0:
                for x in graph.successors(node):
                    row = row + ' ' + str(x + 1)
            completed_line = str(node+1) + ' ' + str(len(graph.successors(node))) + row
            print(completed_line)
            i_file.write(completed_line + '\n')
        # Write cash flow and duration
        i_file.write(str(1) + ' ' + str(0) + ' ' + str(0) + '\n')
        #for node in range(len(graph.vs)):
        for node in range(1, len(graph.vs)-1):
            completed_line = str(node + 1) + ' ' + \
                             str(np.random.randint(MIN_DUR, MAX_DUR)) + ' ' + \
                             str(np.random.randint(MIN_CF, MAX_CF))
            print(completed_line)

            i_file.write(completed_line + '\n')
        i_file.write(str(len(graph.vs)) + ' ' + str(0) + ' ' + str(0) + '\n')

        print("Nr Nodes: ", len(graph.vs))
        print("Nr Edges: ", len(graph.es))

    except Exception:
        print('Problems to write file dg!')
    finally:
        i_file.close()


def Bacth_Generator(n_iterations=1):
    # Graph parameters
    # MIN_PER_LAYER = 4
    # MAX_PER_LAYER = 4
    # MIN_LAYERS = 4
    # MAX_LAYERS = 20
    # EDGE_PROB = 100
    plotGraph = False

    # # # Lote_1 (2a Rodada)
    # MIN_PER_LAYER = 2
    # MAX_PER_LAYER = 4
    # MIN_LAYERS = 2
    # MAX_LAYERS = 4
    # EDGE_PROB = 5

    # # Lote_2 (2a Rodada)
    # MIN_PER_LAYER = 4
    # MAX_PER_LAYER = 6
    # MIN_LAYERS = 4
    # MAX_LAYERS = 6
    # EDGE_PROB = 10

    # # Lote_3 (2a Rodada)
    # MIN_PER_LAYER = 8
    # MAX_PER_LAYER = 10
    # MIN_LAYERS = 8
    # MAX_LAYERS = 10
    # EDGE_PROB = 5

    # Lote_4 (2a Rodada)
    MIN_PER_LAYER = 32
    MAX_PER_LAYER = 32
    MIN_LAYERS = 32
    MAX_LAYERS = 32
    EDGE_PROB = 100

    # Node parameters
    MIN_DUR = 5
    MAX_DUR = 10
    MIN_CF = -100
    MAX_CF = 100
    CP_MULT = 4

    count = 0
    while count < n_iterations:
        # Structures for each net
        vertex_for_layer = []
        start = 2
        edges = []
        nodes = []
        graph = ig.Graph(directed=True)

        # Randomize the layer number, between dummies
        if MIN_LAYERS > MAX_LAYERS:
            raise Exception('MAX_LAYERS must be greater than or equal MIN_LAYERS!')
        elif MIN_LAYERS == MAX_LAYERS:
            n_layers = np.random.randint(MIN_LAYERS, MAX_LAYERS + 1)
        else:
            n_layers = np.random.randint(MIN_LAYERS, MAX_LAYERS )

        # Randomize the vertex number per layer
        for i_layer in range(1, n_layers + 1):
            if MIN_PER_LAYER > MAX_PER_LAYER:
                raise Exception('MAX_PER_LAYER must be greater than or equal MIN_PER_LAYER!')
            elif MIN_PER_LAYER == MAX_PER_LAYER:
                random_vertex = np.random.randint(MIN_PER_LAYER, MAX_PER_LAYER + 1)
            else:
                random_vertex = np.random.randint(MIN_PER_LAYER, MAX_PER_LAYER)

            vertex_for_layer.append(list(range(start, start + random_vertex)))
            start += random_vertex
        print(vertex_for_layer)

        graph.add_vertices(start)

        for i_layer in range(len(vertex_for_layer)):
            for i_vertex in vertex_for_layer[i_layer]:
                # if pd.notna(i_vertex):
                #     g.add_vertex(int(i_vertex))
                next_layer = i_layer + 1
                nodes.append(i_vertex)
                #g.add_vertex(name=i_vertex)
                while next_layer < len(vertex_for_layer):
                    for j_vertex in vertex_for_layer[next_layer]:
                        # if pd.notna(j_vertex):
                        #     g.add_vertex(int(j_vertex))
                        if (np.random.randint(1, 101) <= EDGE_PROB):
                            edges.append((int(i_vertex)-1, int(j_vertex)-1))
                            graph.add_edge(int(i_vertex)-1, int(j_vertex)-1)
                    next_layer += 1

        # Connects all vertices on the first layer with the initial dummy
        for i_vertex in vertex_for_layer[0]:
            edges.append((0, i_vertex-1))
            graph.add_edge(0, i_vertex-1)

        # Connects all vertices on the last layer with the finish dummy
        for i_vertex in vertex_for_layer[-1]:
            edges.append((i_vertex - 1, vertex_for_layer[-1][-1]))
            graph.add_edge(i_vertex - 1, vertex_for_layer[-1][-1])

        # Checks and ensures that every vertex has an input and output degree of 1.
        for i_vertex in range(1, len(graph.vs)-1):
            if graph.degree(i_vertex, mode='IN') == 0:
                for idx_layer, i_layer in enumerate(vertex_for_layer):
                    if i_vertex + 1 in i_layer:
                        idx_back_layer = idx_layer - 1
                        if len(vertex_for_layer[idx_back_layer]) > 1:
                            j_vertex = np.random.randint(min(vertex_for_layer[idx_back_layer]),
                                                         max(vertex_for_layer[idx_back_layer]))
                        else:
                            j_vertex = vertex_for_layer[idx_back_layer][0]

                        if (i_vertex, j_vertex) not in graph.get_edgelist() or \
                                (j_vertex, i_vertex) not in graph.get_edgelist():
                            edges.append((j_vertex, i_vertex))
                            graph.add_edge(j_vertex, i_vertex)
                            #print("Complement IN: ", j_vertex, ",", i_vertex)
                        break

            if graph.degree(i_vertex, mode='OUT') == 0:
                for idx_layer, i_layer in enumerate(vertex_for_layer):
                    if i_vertex + 1 in i_layer:
                        idx_front_layer = idx_layer + 1
                        if len(vertex_for_layer[idx_front_layer]) > 1:
                            j_vertex = np.random.randint(min(vertex_for_layer[idx_front_layer]),
                                                         max(vertex_for_layer[idx_front_layer]))
                        else:
                            j_vertex = vertex_for_layer[idx_front_layer][0]


                        if (i_vertex, j_vertex) not in graph.get_edgelist() or \
                                (j_vertex, i_vertex) not in graph.get_edgelist():
                            edges.append((i_vertex, j_vertex))
                            graph.add_edge(i_vertex, j_vertex)
                        #print("Complement OUT: ", i_vertex, ",", j_vertex)
                        break

        print('Degree IN: ', [x for x in graph.degree(graph.vs, mode='IN')])
        print('Degree OUT: ', [x for x in graph.degree(graph.vs, mode='OUT')])





        # g = nx.DiGraph()
        # #g.add_nodes_from(range(1, start - random_vertex))
        # g.add_nodes_from(range(1, start))
        # plt_general(ct=g)




        visual_style = {}
        out_name = "graph.png"
        # Set bbox and margin
        visual_style["bbox"] = (1700, 1200)
        visual_style["margin"] = 30
        # Set vertex colours
        visual_style["vertex_color"] = 'white'
        # Set vertex size
        visual_style["vertex_size"] = 30
        # Set vertex lable size
        visual_style["vertex_label_size"] = 20
        # Don't curve the edges
        visual_style["edge_curved"] = False

        #visual_style["target"] = cairo.Surface
        # Set the layout
        #my_layout = g.layout_lgl()
        #my_layout = graph.layout_reingold_tilford(root=0)
        #my_layout = graph.layout_fruchterman_reingold()
        #my_layout = graph.layout_reingold_tilford()
        #my_layout = graph.layout_circle()
        #my_layout = g.layout_kamada_kawai()
        #my_layout = graph.layout_auto()
        my_layout = graph.layout_random()
        #my_layout = graph.layout_grid()
        #my_layout = graph.layout_grid_fruchterman_reingold()
        #my_layout = graph.layout_davidson_harel()
        #my_layout = graph.layout_kamada_kawai()

        #my_layout = graph.layout_reingold_tilford_circular()
        #my_layout = graph.layout_lgl()
        visual_style["layout"] = my_layout

        # Adds labels
        for i in range(len(graph.vs)):
            graph.vs[i]["id"] = i + 1
            graph.vs[i]["label"] = str(i + 1)
        #
        ig.plot(graph, **visual_style)



        Write_File(count,
                   graph,
                   MIN_DUR,
                   MAX_DUR,
                   MIN_CF,
                   MAX_CF,
                   CP_MULT)

        count += 1


##########
## main ##
##########
Bacth_Generator(1)

t2 = time.time()
print("Run time: ", t2-t1)