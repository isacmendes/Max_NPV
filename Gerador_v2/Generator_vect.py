# import pandas as pd
# import numpy as np
#
# n_layer = [1,2,3]
#
# n_layer_1 = pd.DataFrame(pd.Series(range(4,9)))
#
# for c in n_layer:
#      n_layer_1.insert(c, c, np.where(np.random.randint(1,101,len(n_layer_1)) <= 50, c, False))
#
# for column in n_layer_1.columns[1:]:
#      print(pd.merge(n_layer_1[0], n_layer_1[column], left_on=0, right_index=True))
#
# ############################
#
# df = pd.DataFrame()
# df_v = pd.DataFrame(df.loc[0].T.dropna())
# df_v.insert(loc=0, column=1, value=1)
# edges = list(zip(df_v[1], pd.Series(df_v[0], dtype='int64')))
#
# df = pd.DataFrame(pd.Series(range(33)))
# df_v = pd.DataFrame(df.loc[0].T.dropna())
#
# for i in range(1,1025):
#     df.insert(loc=len(df.columns), column=i, value='NaN')
#
# for current_layer in range(33):
#      df_v.insert(loc=0, column=1, value=1)


###################################
import pandas as pd
import numpy as np
import time
import igraph as ig

t1 = time.time()
g = ig.Graph(directed=True)
g.add_vertices(1026)
layers = np.random.randint(32, 33, 32)

# g.add_vertices(18)
# layers = np.random.randint(4, 5, 4)

PROB_ADJ = 100

#layers = [5, 4, 6, 3]
#total_vertices = 20
total_vertices = layers.sum()

start = 1
for idx_current_layer in range(len(layers)):
    adjacency_h = pd.DataFrame(pd.Series(range(start, start + layers[idx_current_layer]),
                                         index=list(range(start, start + layers[idx_current_layer]))))
    #
    for vertex in range(start+layers[idx_current_layer], total_vertices + 1):
        adjacency_h.insert(loc=len(adjacency_h.columns), column=vertex, value=np.nan)

        adjacency_h[vertex] = np.where(np.random.randint(1,101,len(adjacency_h[vertex])) <= PROB_ADJ, vertex, np.nan)

        edges_df = pd.DataFrame(pd.Series(adjacency_h[0]))
        edges_df.insert(len(edges_df.columns), vertex, pd.Series(adjacency_h[vertex]))

        #edges = list(zip(edges_df.dropna()[0], pd.Series(edges_df.dropna()[vertex], dtype='int64')))

        #g.add_edges(edges)

    start += layers[idx_current_layer]
    print('\n', adjacency_h)

# Connects all vertices on the first layer with the initial dummy
for i_vertex in range(1,33):
    g.add_edge(0, i_vertex)

# Connects all vertices on the last layer with the finish dummy
for i_vertex in range(993, 1025):
    g.add_edge(i_vertex, 1025)

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

# visual_style["target"] = cairo.Surface
# Set the layout
# my_layout = g.layout_lgl()
#my_layout = g.layout_reingold_tilford(root=0)
# my_layout = graph.layout_fruchterman_reingold()
my_layout = g.layout_reingold_tilford()
# my_layout = graph.layout_circle()
# my_layout = g.layout_kamada_kawai()
# my_layout = graph.layout_auto()
# my_layout = graph.layout_random()
# my_layout = graph.layout_grid()
# my_layout = graph.layout_grid_fruchterman_reingold()
# my_layout = graph.layout_davidson_harel()
# my_layout = graph.layout_kamada_kawai()

# my_layout = graph.layout_reingold_tilford_circular()
# my_layout = graph.layout_lgl()
visual_style["layout"] = my_layout

# Adds labels
for i in range(len(g.vs)):
    g.vs[i]["id"] = i + 1
    g.vs[i]["label"] = str(i + 1)
#
ig.plot(g, **visual_style)

t2 = time.time()
print(t2 - t1)