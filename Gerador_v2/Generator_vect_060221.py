import pandas as pd
import numpy as np
import time
import igraph as ig
from random import sample
from datetime import datetime

def style_plot(graph):
    visual_style = {}
    out_name = "graph.png"
    # Set bbox and margin
    visual_style["bbox"] = (1700, 1200)
    visual_style["margin"] = 30
    # Set vertex colours
    visual_style["vertex_color"] = 'white'
    # Set vertex size
    visual_style["vertex_size"] = 50
    # Set vertex lable size
    visual_style["vertex_label_size"] = 40
    # Don't curve the edges
    visual_style["edge_curved"] = False

    # visual_style["target"] = cairo.Surface
    # Set the layout
    #my_layout = graph.layout_lgl()
    my_layout = graph.layout_reingold_tilford(root=0)
    # my_layout = graph.layout_fruchterman_reingold()
    # my_layout = graph.layout_circle()
    # my_layout = graph.layout_kamada_kawai()
    # my_layout = graph.layout_auto()
    # #my_layout = graph.layout_random()
    # my_layout = graph.layout_grid()
    # my_layout = graph.layout_grid_fruchterman_reingold()
    # my_layout = graph.layout_davidson_harel()
    # my_layout = graph.layout_kamada_kawai()

    # my_layout = graph.layout_reingold_tilford_circular()
    # my_layout = graph.layout_lgl()
    visual_style["layout"] = my_layout

    return visual_style

def Write_File(nr_graph,
               graph,
               MIN_DUR=5,
               MAX_DUR=10,
               MIN_CF=-100,
               MAX_CF=100,
               CP_MULT=1,
               DISC_RATE=10,
               PERC_NEG=10,
               N_LAYERS='NA'):

    # Write nodes successors
    global i_file
    print('#' * 50)
    try:
        #i_file = open("../Samples/Lotes_2a_Rodada/Lote_1/dg0%d.tpf" %(nr_graph+1), "w")
        #i_file = open("../Samples/Random_G2/06022021/dg0%d_%d_%d.tpf" %(nr_graph+1, len(graph.vs), EDGE_PROB), "w")
        #i_file = open("../Samples/Random_G2/09022021/dg0%d_%d_%d.tpf" %(nr_graph+1, len(graph.vs), len(graph.es)), "w")
        i_file = open("../Samples/Random_G2/Lote_16_320_G2_P3/dg0%d_%d_%d_%d_%d_%d.tpf"
                      %(nr_graph+1, len(graph.vs), len(graph.es), datetime.today().year, datetime.today().month, datetime.today().day), "w")

        #print(len(graph.vs), 'E'+str(CP_MULT))
        #i_file.write(str(len(graph.vs)) + ' ' + 'E'+str(CP_MULT) + '\n')
        i_file.write(str(len(graph.vs)) + ' ' + str(N_LAYERS) + ' ' + 'CACULATED_DEGREE' + ' ' +
                     str(DISC_RATE) + ' ' + str(PERC_NEG) + ' ' + 'E'+str(CP_MULT) + ' ' + 'E'+str(CP_MULT) + '\n')
        for node in range(len(graph.vs)):
            row = ""
            if len(graph.successors(node)) > 0:
                for x in graph.successors(node):
                    row = row + ' ' + str(x + 1)
            completed_line = str(node+1) + ' ' + str(len(graph.successors(node))) + row
            #print(completed_line)
            i_file.write(completed_line + '\n')
        # Write cash flow and duration
        i_file.write(str(1) + ' ' + str(0) + ' ' + str(0) + '\n')
        #for node in range(len(graph.vs)):
        for node in range(1, len(graph.vs)-1):
            #graph.vs[node]["CF"] = np.random.randint(MIN_DUR, MAX_DUR)
            completed_line = str(node + 1) + ' ' + \
                             str(np.random.randint(MIN_DUR, MAX_DUR)) + ' ' + \
                             str(graph.vs[node]["CF"])
                             #str(np.random.randint(MIN_CF, MAX_CF))

            #print(completed_line)

            i_file.write(completed_line + '\n')
        i_file.write(str(len(graph.vs)) + ' ' + str(0) + ' ' + str(0) + '\n')

        print("Nr Nodes: ", len(graph.vs))
        print("Nr Edges: ", len(graph.es))

    except Exception:
        print('Problems to write file dg!')
    finally:
        i_file.close()

def Generator_layers(n_layers, vertices):
    delivered = 0
    current_max = vertices - n_layers
    vertices_per_layer = np.array(np.random.randint(vertices // n_layers, vertices // n_layers + 1, size=n_layers))
    # print('vertices_per_layer: ', vertices_per_layer)
    idx = 0
    while (delivered < vertices) and (current_max > 1) and (idx < n_layers):
        # limits the upper value to 25 percent of the remaining value
        if int(current_max * 0.25 + 1) > 1:
            delivered_current = np.random.randint(1, current_max * 0.25 + 1)
        else:
            delivered_current = 1
        current_max -= delivered_current
        delivered += delivered_current
        vertices_per_layer[np.random.randint(0, len(vertices_per_layer))] = delivered_current
        idx += 1
    if np.array(vertices_per_layer).sum() < vertices:
        vertices_per_layer[np.random.randint(0, len(vertices_per_layer))] += vertices - vertices_per_layer.sum()

    return(vertices_per_layer)


def Bacth_Generator(n_iterations=1):
    global EDGE_PROB

    for i_iteration in range(n_iterations):
        MIN_LAYERS = 2
        MAX_LAYERS = 'n'
        EDGE_PROB = np.random.randint(5, 100)
        MIN_VERTICES = 16
        MAX_VERTICES = 320
        DISC_RATE = np.random.randint(1, 21)
        PERC_NEG = np.random.randint(0, 101)

        # Node parameters
        MIN_DUR = 5
        MAX_DUR = 10
        MIN_CF = 0
        MAX_CF = 100
        CP_MULT = np.random.randint(1, 3)
        vertex_for_layer = []

        # Sort number of layers and vertices
        if MAX_LAYERS != 'n':
            pass
        else:
            total_vertices = np.random.randint(MIN_VERTICES, MAX_VERTICES + 1)
            MAX_LAYERS = total_vertices

        if MIN_LAYERS > MAX_LAYERS:
            raise Exception('MAX_LAYERS must be greater than or equal MIN_LAYERS!')
        elif MIN_LAYERS == MAX_LAYERS:
            n_layers = np.random.randint(MIN_LAYERS, MAX_LAYERS + 1)
        else:
            n_layers = np.random.randint(MIN_LAYERS, MAX_LAYERS)

        # Delivery number's vertices per layer
        ######################################################################################
        layers = Generator_layers(n_layers, total_vertices)
        ######################################################################################

        graph = ig.Graph(directed=True)
        graph.add_vertices(total_vertices + 2)

        start = 1
        for idx_current_layer in range(len(layers)):
            adjacency_h = pd.DataFrame(pd.Series(range(start, start + layers[idx_current_layer]),
                                                 index=list(range(start, start + layers[idx_current_layer]))))
            # New line
            if start == start + layers[idx_current_layer]:
                vertex_for_layer.append(range(start, start + layers[idx_current_layer] + 1))
            else:
                vertex_for_layer.append(range(start, start + layers[idx_current_layer]))

            #vertex_for_layer.append(range(start, start + layers[idx_current_layer]))

            # Adjacency matrix
            for vertex in range(start+layers[idx_current_layer], total_vertices + 1):
                adjacency_h.insert(loc=len(adjacency_h.columns), column=vertex, value=np.nan)

                # Sort adjacency with EDGE_PROB
                adjacency_h[vertex] = np.where(np.random.randint(1,101,len(adjacency_h[vertex])) <= EDGE_PROB, vertex, np.nan)

                # Get and add edges
                edges_df = pd.DataFrame(pd.Series(adjacency_h[0]))
                edges_df.insert(len(edges_df.columns), vertex, pd.Series(adjacency_h[vertex]))
                edges = list(zip(edges_df.dropna()[0], pd.Series(edges_df.dropna()[vertex], dtype='int64')))
                graph.add_edges(edges)

            start += layers[idx_current_layer]
            #print('\n', adjacency_h)

        # Connects all vertices on the first layer with the initial dummy
        for i_vertex in range(1, layers[0] + 1):
            graph.add_edge(0, i_vertex)

        # Connects all vertices on the last layer with the finish dummy
        s = (layers.sum() - layers[-1] + 1)

        for i_vertex in range((layers.sum() - layers[-1]), total_vertices + 1):
            t = (i_vertex, total_vertices + 3)
            graph.add_edge(i_vertex, total_vertices + 1)

        # Checks and ensures that every vertex has an input and output degree of 1.
        nr_vertex = len(graph.vs)
        for i_vertex in range(1, nr_vertex):
            if graph.degree(i_vertex, mode='IN') == 0:
                for idx_layer, i_layer in enumerate(vertex_for_layer):
                    if i_vertex in i_layer:
                        idx_back_layer = idx_layer - 1
                        if len(vertex_for_layer[idx_back_layer]) > 1:
                            j_vertex = np.random.randint(min(vertex_for_layer[idx_back_layer]),
                                                         max(vertex_for_layer[idx_back_layer]))
                        else:
                            j_vertex = vertex_for_layer[idx_back_layer][0]

                            #print('idx_back_layer', idx_back_layer)
                            #t = len(vertex_for_layer[idx_back_layer])
                            # try:
                            #     j_vertex = vertex_for_layer[idx_back_layer][0]
                            # except:
                            #     j_vertex = vertex_for_layer[idx_back_layer]

                        if (i_vertex, j_vertex) not in graph.get_edgelist() or \
                                (j_vertex, i_vertex) not in graph.get_edgelist():
                            edges.append((j_vertex, i_vertex))
                            graph.add_edge(j_vertex, i_vertex)
                            # print("Complement IN: ", j_vertex, ",", i_vertex)
                        break

            if graph.degree(i_vertex, mode='OUT') == 0:
                for idx_layer, i_layer in enumerate(vertex_for_layer):
                    if i_vertex in i_layer:
                        idx_front_layer = idx_layer + 1
                        try:
                            teste = len(vertex_for_layer[idx_front_layer])
                        except:
                            idx_front_layer = -1
                        if len(vertex_for_layer[idx_front_layer]) > 1:
                            j_vertex = np.random.randint(min(vertex_for_layer[idx_front_layer]),
                                                         max(vertex_for_layer[idx_front_layer]))
                        else:
                            j_vertex = vertex_for_layer[idx_front_layer][0]

                        if (i_vertex, j_vertex) not in graph.get_edgelist() or \
                                (j_vertex, i_vertex) not in graph.get_edgelist():
                            edges.append((i_vertex, j_vertex))
                            try:
                                graph.add_edge(i_vertex, j_vertex)
                            except:
                                print(graph.vs, '\n', graph.es)
                                i_teste, j_teste = i_vertex, j_vertex

                            # print("Complement OUT: ", i_vertex, ",", j_vertex)
                        break

        # print('Degree IN: ', [x for x in graph.degree(graph.vs, mode='IN')])
        # print('Degree OUT: ', [x for x in graph.degree(graph.vs, mode='OUT')])
        # print('Vertices: ', len(graph.vs))
        # print('Edges: ', len(graph.es))

        # Adds labels
        for i in range(len(graph.vs)):
            graph.vs[i]["id"] = i + 1
            graph.vs[i]["label"] = str(i + 1)
            graph.vs[i]["CF"] = np.random.randint(MIN_DUR, MAX_DUR)

        # Adds percent negatives
        lt = sample(range(len(graph.vs)), int(PERC_NEG/100 * (len(graph.vs) - 1)) + 1)
        for i in lt:
            graph.vs[i]["CF"] *= -1


        Write_File(i_iteration,
                   graph,
                   MIN_DUR,
                   MAX_DUR,
                   MIN_CF,
                   MAX_CF,
                   CP_MULT,
                   DISC_RATE,
                   PERC_NEG,
                   n_layers)

        # ig.plot(graph, **style_plot(graph))
        print('Generated instance ', i_iteration + 1, '!')
        #

########
# Main #
########

t1 = time.time()
Bacth_Generator(1000)
t2 = time.time()

print('Tempo decorrido: ', t2 - t1)