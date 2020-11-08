import numpy as np
import pandas as pd
import igraph as ig

MIN_PER_LAYER = 2
MAX_PER_LAYER = 2
MIN_LAYERS = 2
MAX_LAYERS = 2
EDGE_PROB = 5
MAX_FAN_IN = 3
MAX_FAN_OUT = 3
plotGraph = True

g = ig.Graph(directed=True)

# Add the initial dummy
g.add_vertices(1)

# Randomize the layer number
n_Layers = np.random.randint(MIN_LAYERS, MAX_LAYERS + 1)

# Structure with the length of the MAX_PER_LAYER
vertex_for_layer = pd.DataFrame(index=range(1, MAX_PER_LAYER + 1))
start = 1

edges = []
nodes = []

# Randomize the vertex number per layer
for i_layer in range(n_Layers):
    random_vertex = np.random.randint(MIN_PER_LAYER, MAX_PER_LAYER + 1)

    vertex_for_layer.insert(i_layer,
                            i_layer,
                            pd.Series(np.array(range(start, (start + random_vertex + 1))), dtype=np.int64))
    nr = vertex_for_layer[i_layer]
    nr2 = np.array(range(start, (start + random_vertex + 1)))
    nr3 = [x for x in vertex_for_layer[i_layer]]
    nr4 = vertex_for_layer[i_layer]
    g.add_vertices([x for x in nr])
    nodes.append([x for x in vertex_for_layer[i_layer]])
    start += random_vertex

print(vertex_for_layer)

# Cycle 1 - Ensures that vertices will have degree (in and out) of at least one
for i_layer in vertex_for_layer:
    for i_vertex in vertex_for_layer[i_layer]:
        next_layer = i_layer + 1

        # for vertex on the first layer, one vertex of a forward layer is sorted
        if i_layer == 0:
            if len(vertex_for_layer) > 2:
                if (i_layer + 1) < len(vertex_for_layer)-2:
                    sorted_layer = np.random.randint((i_layer + 1), len(vertex_for_layer)-2)
                else:
                    sorted_layer = i_layer + 1
            else:
                sorted_layer = len(vertex_for_layer) - 1
            j_vertex_sorted = np.random.randint(vertex_for_layer[sorted_layer].min()-1,
                                                 vertex_for_layer[sorted_layer].max()-1)
            # Adds edge
            if (i_vertex is not np.nan) and (j_vertex_sorted is not np.nan) and (i_vertex != j_vertex_sorted):
                g.add_edge(i_vertex-1, j_vertex_sorted-1)

        # for vertex between second and penultimante layer, one vertex of a forward layer and backward layers are sorted
        elif i_layer != len(vertex_for_layer) - 2:
            # forward
            if len(vertex_for_layer) > 2:
                if (i_layer + 1) < len(vertex_for_layer) - 2:
                    sorted_layer = np.random.randint((i_layer + 1), len(vertex_for_layer)-2)
                else:
                    sorted_layer = i_layer + 1
            else:
                sorted_layer = len(vertex_for_layer) - 2
            j_vertex_sorted = np.random.randint(vertex_for_layer[sorted_layer].min() - 1,
                                                 vertex_for_layer[sorted_layer].max() - 1)

            # Adds edge forward
            if (i_vertex is not np.nan) and (j_vertex_sorted is not np.nan) and (i_vertex != j_vertex_sorted):
                g.add_edge(i_vertex-1, j_vertex_sorted-1)

            # backward
            if (i_layer + 1) < len(vertex_for_layer) - 2:
                sorted_layer = np.random.randint((i_layer - 1), len(vertex_for_layer) - 2)
            else:
                sorted_layer = i_layer + 1
            j_vertex_sorted = np.random.randint(vertex_for_layer[sorted_layer].min() - 1,
                                                 vertex_for_layer[sorted_layer].max() - 1)
            # Adds edge backward
            if (i_vertex is not np.nan) and (j_vertex_sorted is not np.nan) and (i_vertex != j_vertex_sorted):
                g.add_edge(j_vertex_sorted-1, i_vertex-1)

        else:
            # backward
            sorted_layer = i_layer
            j_vertex_sorted = np.random.randint(vertex_for_layer[sorted_layer].min() - 1,
                                                 vertex_for_layer[sorted_layer].max() - 1)
            # Adds edge backward
            if (i_vertex is not np.nan) and (j_vertex_sorted is not np.nan) and (i_vertex != j_vertex_sorted):
                g.add_edge(j_vertex_sorted-1, i_vertex-1)


# # Cycle 2 - Rondomizes edges between current layer and forward layer
# for i_layer in vertex_for_layer:
#     for i_vertex in vertex_for_layer[i_layer]:
#         # if pd.notna(i_vertex):
#         #     g.add_vertex(int(i_vertex))
#         next_layer = i_layer + 1
#         nodes.append(i_vertex)
#         #g.add_vertex(name=i_vertex)
#         while next_layer < len(vertex_for_layer.columns):
#             for j_vertex in vertex_for_layer[next_layer]:
#                 # if pd.notna(j_vertex):
#                 #     g.add_vertex(int(j_vertex))
#                 if (np.random.randint(1, 101) <= EDGE_PROB) and (not pd.isna(i_vertex) and not pd.isna(j_vertex)):
#
#                     edges.append((int(i_vertex)-1, int(j_vertex)-1))
#                     #g.add_edge(int(i_vertex), int(j_vertex))
#             next_layer += 1

# Adds nodes and edges between dummies
g.add_vertices(nodes)
g.add_edges(edges)

# Adds finish dummy
finish_dummy = len(nodes) + 1
g.add_vertex(finish_dummy)

# Connects the initial dummy with the first layer

# for i_vertex in vertex_for_layer[0]:
#     g.add_edge(0, i_vertex-1)



# for i_vertex in vertex_for_layer[len(vertex_for_layer.columns)-1]:
#     g.add_edge(i_vertex-1, finish_dummy)


print("nodes: ", g.vs.indices)
print("Edges: ", g.get_edgelist())
#g.add_edges([(1,6)])

visual_style = {}
out_name = "graph.png"
# Set bbox and margin
visual_style["bbox"] = (400, 400)
visual_style["margin"] = 27
# Set vertex colours
visual_style["vertex_color"] = 'white'
# Set vertex size
visual_style["vertex_size"] = 20
# Set vertex lable size
visual_style["vertex_label_size"] = 15
# Don't curve the edges
visual_style["edge_curved"] = False
# Set the layout
#my_layout = g.layout_lgl()
#my_layout = g.layout_reingold_tilford(root=0)
#my_layout = g.layout_fruchterman_reingold()
#my_layout = g.layout_circle()
#my_layout = g.layout_kamada_kawai()
my_layout = g.layout_auto()
#my_layout = g.layout_reingold_tilford_circular()
#my_layout = g.layout_reingold_tilford_circular()

visual_style["layout"] = my_layout
# Plot the graph

#g.add_vertices(6)

for i in range(len(g.vs)):
    g.vs[i]["id"] = i + 1
    g.vs[i]["label"] = str(i + 1)

#ig.plot(g, layout=g.layout_reingold_tilford())
#ig.plot(g, layout=g.layout_reingold_tilford_circular(root=0), bbox=(400, 400), vertex_color="white", label=True)
ig.plot(g, **visual_style)



