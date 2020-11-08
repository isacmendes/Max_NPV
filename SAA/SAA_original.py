# -*- coding: utf-8 -*-
from Early_tree_graph_refined import main as early_tree_main
from PluginGraph.Plotter import *


def Steepest_Ascent_Direction():
    global it_SAD

    Z = []
    V = st.copy()

    for i in range(1, V.number_of_nodes() + 1):
        st.nodes[i]['C'] = []
        st.nodes[i]['C'].append(i)
        st.nodes[i]['DC'] = st.nodes[i]['CF'] / ((1 + 0.01) ** (st.nodes[i]['EF']))
        st.nodes[i]['CF_CUMULATIVE'] = st.nodes[i]['DC']

    while V.number_of_nodes() != 1:
        for i in list(V.nodes):
            # For nodes other than 1
            if i is not 1:
                it_SAD += 1
                # For a node without predecessors and with only one successor
                if len(list(V.predecessors(i))) == 0 and len(list(V.successors(i))) == 1:
                    #it_SAD += 1
                    j = list(V.successors(i))[0]
                    st.nodes[j]['CF_CUMULATIVE'] += st.nodes[i]['CF_CUMULATIVE']
                    st.nodes[j]['C'].extend(st.nodes[i]['C'])
                    V.remove_node(i)

                # For a node with only a predecessor and without successor
                elif len(list(V.predecessors(i))) == 1 and len(list(V.successors(i))) == 0:
                    #it_SAD += 1
                    j = i
                    i = ([x for x in V.predecessors(i)][0])
                    if st.nodes[j]['CF_CUMULATIVE'] < 0:
                        Z.append(st.nodes[j]['C'])
                    else:
                        st.nodes[i]['CF_CUMULATIVE'] += st.nodes[j]['CF_CUMULATIVE']
                        st.nodes[i]['C'].extend(st.nodes[j]['C'])
                    V.remove_node(j)

    return Z


def Vertex_Ascent(Z):
    global it_VA_EDGES, it_VA_shifts

    for edge in list(st.edges):
        it_VA_EDGES += 1
        i, j = edge[0], edge[1]
        if (j not in st.nodes[i]['C']) and (i not in st.nodes[j]['C']):
            st.remove_edge(i, j)

    while Z != []:
        k, l, V_k_l = Compute_V_k_l(Z)

        for SA_l in Z:
            if k in SA_l:
                break
        for i in SA_l:
            it_VA_shifts += 1
            st.nodes[i]['EF'] += V_k_l
        Z.remove(SA_l)
        st.add_edge(k, l)


def Compute_V_k_l(Z):
    global call_Compute, it_Compute, graph

    call_Compute += 1
    l, k = None, None
    V_k_l = 0

    Z_dem = []
    for SA_l in Z:
        for node in SA_l:
            Z_dem.append(node)

    min_distance = st.deadline
    for pred in Z_dem:
        for suc in graph.successors(pred):
            it_Compute += 1
            if suc not in Z_dem:
                s_k = st.nodes[pred]['EF'] - st.nodes[pred]['DURATION']
                d_k = st.nodes[pred]['DURATION']
                s_l = st.nodes[suc]['EF'] - st.nodes[suc]['DURATION']
                if (s_l - st.nodes[pred]['EF']) < min_distance:
                    min_distance = s_l - st.nodes[pred]['EF']
                    if pred == graph.number_of_nodes():
                        V_k_l = s_l - s_k - (-st.deadline)
                        l = 1
                    else:
                        V_k_l = s_l - s_k - d_k
                        l = suc
                    k = pred

    return k, l, V_k_l


def main(spanning_tree, original_graph):
    global st, graph, total_main, it_SAD, it_VA_EDGES, it_VA_shifts, it_Compute, call_Compute

    # st, graph = early_tree_main("SAA")
    # total_main += 1
    it_SAD, it_VA_EDGES, it_VA_shifts, it_Compute, call_Compute = 0, 0, 0, 0, 0

    st = spanning_tree
    graph = original_graph


    call_SAD = 0
    call_VA = 0
    while True:
        call_SAD += 1
        Z = Steepest_Ascent_Direction()

        if Z == []:
            DC_FINAL = 0.00
            for node in range(1, st.number_of_nodes() + 1):
                DC_FINAL += st.nodes[node]['CF'] / ((1 + 0.01) ** (st.nodes[node]['EF']))
            #print("The optimal solution is %d" % DC_FINAL)
            # plt_17("Original SAA", DC_FINAL, st)
            #plt_general("Original SAA", DC_FINAL, st)
            # plt_main_example("Original RS", DC_FINAL, st)

            # print("-----------\nCONTADORES:\n-----------")
            # print("Iterações Main(): ", total_main)
            # print("Iterações Steepest_Ascent_Direction(): ", total_SAD)
            # print("Iterações Vertex_Ascent() EDGES: ", total_VA_EDGES)
            # print("Iterações Vertex_Ascent() SHIFT: ", total_VA_shifts)
            # print("Iterações Compute_V_K_l(): ", total_compute)
            # print('Total geral', total_main + total_SAD + total_VA_EDGES + total_VA_shifts + total_compute)

            #iterations = it_SAD + 0 + 0 + it_Compute
            iterations = it_SAD + it_VA_EDGES + it_VA_shifts + it_Compute
            #iterations = it_SAD + 0 + it_VA_shifts + it_Compute
            recursion_calls = 0

            # print('-' * 30)
            # print('SAA')
            # print('total_main: ', total_main)
            # print('total_SAD: ', total_SAD)
            # print('total_VA_EDGES: ', total_VA_EDGES)
            # print('total_VA_shifts: ', total_VA_shifts)
            # print('total_compute: ', total_compute)
            # print('-' * 30)
            # print('id st: ', id(st))

            return iterations, \
                   recursion_calls, \
                   it_SAD, \
                   call_SAD, \
                   it_VA_EDGES, \
                   it_VA_shifts, \
                   call_VA, \
                   it_Compute, \
                   call_Compute, \
                   graph.number_of_nodes(), \
                   graph.number_of_edges()

        else:
            call_VA += 1
            Vertex_Ascent(Z)


#it_SAD, it_VA_EDGES, it_VA_shifts, it_Compute, call_Compute = 0, 0, 0, 0, 0

# main()
