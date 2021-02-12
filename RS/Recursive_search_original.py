# -*- coding: utf-8 -*-
from Early_tree_graph_refined import main as early_tree_main
from PluginGraph.Plotter import *
import time
import sys
sys.setrecursionlimit(590000000)

global CA, SS

def Step_3():
    global CA, total_Step_3, it_Shift
    total_Step_3 += 1

    CA = set()
    Recursion(1)

def Recursion(node):
    global CA, total_Recursion, it_Shift, DISCOUNTED_RATE
    total_Recursion += 1

    SA = {node}
    DC = ct.nodes[node]['CF'] / ((1 + DISCOUNTED_RATE) ** (ct.nodes[node]['EF']))
    CA.add(node)
    # print('node RS: ', node)
    # print('edges: ', len(ct.edges))

    #graph = nx.DiGraph()

    ct_suc = list(ct.successors(node))
    for i in ct_suc:
        if i not in CA:
            ############################################################################################################
            # Encontrar em conjunto como 'union-find disjoint-set considerar em tempo O(1)'. Verificar método de Python.
            ############################################################################################################
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
                ###########################
                # Custo da adição da aresta
                ###########################

                if (node, i) in ct.edges:
                    ct.remove_edge(node, i)
                    #############################
                    # Custo da adição da remoção
                    #############################
                Step_3()

    ct_pred = list(ct.predecessors(node))
    for j in ct_pred:
        if j not in CA:
            ############################################################################################################
            # Encontrar em conjunto como 'union-find disjoint-set considerar em tempo O(1)'. Verificar método de Python.
            ############################################################################################################
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
                ##############################################
                # Incluir o custo do 'in', usando union find #
                ##############################################
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
    global ct, graph, total_Step_3, total_Recursion, call_Compute, it_Compute, it_Shift, DISCOUNTED_RATE

    #plt_general("Original RS", 100, current_tree)

    DISCOUNTED_RATE = float(current_tree.discounted_rate)/100

    total_Step_3, total_Recursion, call_Compute, it_Compute, it_Shift = 0, 0, 0, 0, 0
    #ct, graph = early_tree_main("RS")
    ct = current_tree
    graph = original_graph

    # Get Early Finish of the penultimate task
    EF_penul_activity = max(np.array([x['EF'] for x in dict(ct.nodes.data()).values()])[1:-2])

    t1 = time.time()
    Step_3()
    t2 = time.time()

    DC_FINAL = 0.00
    for node in range(1, ct.number_of_nodes() + 1):
        DC_FINAL += ct.nodes[node]['CF'] / ((1 + DISCOUNTED_RATE) ** (ct.nodes[node]['EF']))
    print('RS - DC_FINAL: ', DC_FINAL)

    # Get all cash flow
    cfs = np.array([x['CF'] for x in dict(graph.nodes.data()).values()])


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


    # print('in ...', list(dict(graph.in_degree()).values()))
    # print('out ...', list(dict(graph.in_degree()).values()))
    # print('in ...', list(dict(graph.in_degree()).values()), np.sum(list(dict(graph.in_degree()).values())))
    # print('out...', list(dict(graph.out_degree()).values()), np.sum(list(dict(graph.out_degree()).values())))

    unit_effort = recursion_calls + it_Shift + it_Compute

    return graph.number_of_nodes(), \
           graph.number_of_edges(), \
           nx.diameter(graph), \
           max(list(dict(graph.in_degree()).values())[1:-2]), \
           min(list(dict(graph.in_degree()).values())[1:-2]), \
           np.mean(list(dict(graph.in_degree()).values())[1:-2]), \
           max(list(dict(graph.out_degree()).values())[1:-2]), \
           min(list(dict(graph.out_degree()).values())[1:-2]), \
           np.mean(list(dict(graph.out_degree()).values())[1:-2]), \
           DISCOUNTED_RATE, \
           len(cfs[cfs<0])/len(cfs)*100, \
           ct.deadline, \
           EF_penul_activity, \
           unit_effort, \
           DC_FINAL, \
           float(t2 - t1)


#main()