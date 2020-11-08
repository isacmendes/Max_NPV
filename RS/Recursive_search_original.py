# -*- coding: utf-8 -*-
from Early_tree_graph_refined import main as early_tree_main
from PluginGraph.Plotter import *

global CA, SS

def Step_3():
    global CA, total_Step_3, it_Shift
    total_Step_3 += 1

    CA = set()
    Recursion(1)

def Recursion(node):
    global CA, total_Recursion, it_Shift
    total_Recursion += 1

    SA = {node}
    DC = ct.nodes[node]['CF'] / ((1 + 0.01) ** (ct.nodes[node]['EF']))
    CA.add(node)
    #print('node: ', node)

    ct_suc = list(ct.successors(node))
    for i in ct_suc:
        if i not in CA:
            SA_l, DC_l = Recursion(i)
            if DC_l >= 0:
                SA = SA.union(sorted(SA_l))
                DC += DC_l
            else:
                k, l, V_k_l = Compute_V_k_l(SA_l)
                #print("SA_l: ", SA_l)
                for element in SA_l:
                    it_Shift += 1
                    ct.nodes[element]['EF'] += V_k_l
                ct.add_edge(k, l)

                if (node, i) in ct.edges:
                    ct.remove_edge(node, i)
                Step_3()

    ct_pred = list(ct.predecessors(node))
    for j in ct_pred:
        if j not in CA:
            SA_l, DC_l = Recursion(j)
            SA = SA.union(sorted(SA_l))
            DC += DC_l

    return SA, DC

def Compute_V_k_l(Z):
    global call_Compute, it_Compute

    call_Compute += 1
    V_k_l = 0

    min_distance = ct.deadline
    for pred in Z:
        for suc in graph.successors(pred):
            it_Compute += 1
            if suc not in Z:
                s_k = ct.nodes[pred]['EF'] - ct.nodes[pred]['DURATION']
                d_k = ct.nodes[pred]['DURATION']
                s_l = ct.nodes[suc]['EF'] - ct.nodes[suc]['DURATION']
                if (s_l - ct.nodes[pred]['EF']) < min_distance:
                    min_distance = s_l - ct.nodes[pred]['EF']
                    if pred == graph.number_of_nodes():
                        V_k_l = s_l - s_k - (-ct.deadline)
                        l = 1
                    else:
                        V_k_l = s_l - s_k - d_k
                        l = suc
                    k = pred
    return k, l, V_k_l

def main(current_tree, original_graph):
    global ct, graph, total_Step_3, total_Recursion, call_Compute, it_Compute, it_Shift

    #total_Step_3, total_Recursion, total_Compute = 0, 0, 0
    total_Step_3, total_Recursion, call_Compute, it_Compute, it_Shift = 0, 0, 0, 0, 0
    #ct, graph = early_tree_main("RS")
    ct = current_tree
    graph = original_graph


    Step_3()

    DC_FINAL = 0.00
    for node in range(1, ct.number_of_nodes() + 1):
        DC_FINAL += ct.nodes[node]['CF'] / ((1 + 0.01) ** (ct.nodes[node]['EF']))
    #print('DC_FINAL: ', DC_FINAL)
    # print("-----------\nCONTADORES:\n-----------")
    # print("Chamadas recursivas Step_3(): ", total_Step_3)
    # print("Chamadas recursivas Recursion(): ", total_Recursion)
    # print("Iterações Compute_V_K_l(): ", total_Compute)
    # print("Total geral: ", total_Step_3 + total_Recursion + total_Compute)

    #plt_17("Original RS", DC_FINAL, ct)
    #plt_general("Original RS", DC_FINAL, ct)
    #plt_main_example("Original RS", DC_FINAL, ct)

    #iterations = call_Compute + it_Compute + it_Shift
    iterations = it_Compute + it_Shift
    #recursion_calls = total_Step_3 + total_Recursion
    recursion_calls = 0 + total_Recursion

    # print('-' * 30)
    # print('RS')
    # print('total_Step_3: ', total_Step_3)
    # print('total_Recursion: ', total_Recursion)
    # print('total_compute: ', total_Compute)
    # print('-' * 30)
    # print('id ct: ', id(ct))

    return iterations, \
           recursion_calls, \
           total_Step_3, \
           total_Recursion, \
           it_Shift, \
           it_Compute, \
           call_Compute, \
           graph.number_of_nodes(), \
           graph.number_of_edges(), ct




#main()