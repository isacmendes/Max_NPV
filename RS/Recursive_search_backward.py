# -*- coding: utf-8 -*-
from Early_tree_graph_refined import main as early_tree_main
from PluginGraph.Plotter import *
import time
import sys
import networkx as nx
sys.setrecursionlimit(590000000)

global CA, SS

def Step_3():
    global CA, total_Step_3, it_Shift
    total_Step_3 += 1
    #print('Passei no STEP_3() ', total_Step_3)

    CA = set()
    Recursion(ct.number_of_nodes())

def Recursion(node):
    global CA, total_Recursion, it_Shift, DISCOUNTED_RATE, ct
    total_Recursion += 1
    quebrado = False
    SA = {node}
    DC = ct.nodes[node]['CF'] / ((1 + DISCOUNTED_RATE) ** (ct.nodes[node]['EF']))
    #DC = ct.nodes[node]['CF'] / ((1 + DISCOUNTED_RATE) ** (ct.deadline - ct.nodes[node]['EF'] - ct.nodes[node]['DURATION']))
    #DC = ct.nodes[node]['CF'] / ((1 + DISCOUNTED_RATE) ** (ct.deadline - ct.nodes[node]['EF']))
    #DC = ct.nodes[node]['DC']
    CA.add(node)
    # print('node RS: ', node)
    # print('edges: ', len(ct.edges))

    #graph = nx.DiGraph()
    #ct_suc = list(ct.successors(node))
    ct_pred = list(ct.predecessors(node))
    #for i in ct_suc:
    e = ct.edges
    n = ct.nodes
    for i in ct_pred:
        if i not in CA:
            SA_l, DC_l = Recursion(i)
            #if len(list(ct.successors(node))) == 0:
            if len(list(ct.predecessors(node))) == 0:
                break
            if DC_l < 0:
                SA = SA.union(sorted(SA_l))
                DC += DC_l
            else:
                k, l, V_k_l = Compute_V_k_l(SA_l)
                #print("SA_l: ", SA_l)
                for element in SA_l:
                    it_Shift += 1
                    #ct.nodes[element]['EF'] += V_k_l
                    ct.nodes[element]['EF'] -= V_k_l
                #ct.add_edge(k, l)
                ct.add_edge(l, k)
                #print("Aresta adicionada ", '(', l, ', ', k, ')')

                if (i, node) in ct.edges:
                    ct.remove_edge(i, node)
                    #print("Aresta removida ", '(', i, ', ', node,')')
                Step_3()

    #ct_pred = list(ct.predecessors(node))
    ct_suc = list(ct.successors(node))
    for j in ct_suc:
        if j not in CA:
            SA_l, DC_l = Recursion(j)
            SA = SA.union(sorted(SA_l))
            DC += DC_l

    return SA, DC

def Compute_V_k_l(Z):
    #print("Z do RS ", Z)
    global call_Compute, it_Compute, edge_verified, ct
    call_Compute += 1
    V_k_l = 0
    k, l = None, None
    min_distance = ct.deadline
    #min_distance = 0

    for node in sorted(Z):
        #for suc in graph.successors(node):
        for pred in sorted(graph.predecessors(node)):
            it_Compute += 1
            edge_verified += 1
            #print("Edge RS: ", '(', pred, suc, ')')
            if pred not in Z:
                edge_verified += 1
                # s_k = ct.nodes[node]['EF'] - ct.nodes[node]['DURATION']
                # d_k = ct.nodes[node]['DURATION']
                # s_l = ct.nodes[pred]['EF'] - ct.nodes[pred]['DURATION']
                s_k = ct.nodes[node]['EF'] - ct.nodes[node]['DURATION']
                d_k = ct.nodes[node]['DURATION']
                f_l = ct.nodes[pred]['EF']
                e = f_l - s_k
                if f_l - s_k < 0:
                    e *= -1
                if k is None:
                    k = node
                if l is None:
                    l = pred
               # if (f_l - s_k) < min_distance:
                if e <= min_distance:
                    #min_distance = f_l - s_k
                    min_distance = e
                    if node == graph.number_of_nodes():
                        V_k_l = f_l - s_k -(-ct.deadline)
                        l = 1
                    else:
                        #V_k_l = f_l - s_k - d_k
                        V_k_l = f_l - s_k
                        l = pred
                    k = node
                    if V_k_l < 0:
                        V_k_l *= -1
    #print(edge_verified, " arestas contadas no Compute_v_k_l() RS")
    return k, l, V_k_l

def main(current_tree, original_graph):
    global ct, graph, total_Step_3, total_Recursion, call_Compute, it_Compute, it_Shift, DISCOUNTED_RATE, edge_verified

    #plt_general("Original RS", 100, current_tree)

    DISCOUNTED_RATE = float(current_tree.discounted_rate)/100
    DISCOUNTED_RATE = 1.6/100

    total_Step_3, total_Recursion, call_Compute, it_Compute, it_Shift, edge_verified = 0, 0, 0, 0, 0, 0
    #ct, graph = early_tree_main("RS")
    ct = current_tree
    graph = original_graph

    # Get Early Finish of the penultimate task
    EF_penul_activity = max(np.array([x['EF'] for x in dict(ct.nodes.data()).values()])[1:-2])

    #

    # # ANTES DE ESCALONAR
    # for node in range(1, ct.number_of_nodes() + 1):
    #     print("Late tree RSBK: ", node, ' ', str(ct.nodes[node]['EF']))
    # print(ct.edges)

    # for node in range(1, ct.number_of_nodes() + 1):
    #     #ct.nodes[node]['DC'] = ct.nodes[node]['CF'] / ((1 + DISCOUNTED_RATE) ** (ct.deadline - ct.nodes[node]['EF'] - ct.nodes[node]['DURATION']))
    #     ct.nodes[node]['DC'] = ct.nodes[node]['CF'] / ((1 + DISCOUNTED_RATE) ** (ct.deadline - ct.nodes[node]['EF']))

    print("A current tree é RSBK ANTES DE ESCALONAR: ", ct.edges)

    t1 = time.time()
    Step_3()
    t2 = time.time()

    print("A current tree é RSBK: ", ct.edges)

    # DEPOIS DE ESCALONAR
    for node in range(1, ct.number_of_nodes() + 1):
        print("Current tree RSBK: ", node, ' ', str(ct.nodes[node]['EF']))

    DC_FINAL = 0.00
    for node in range(1, ct.number_of_nodes() + 1):
        #DC_FINAL += ct.nodes[node]['CF'] / ((1 + DISCOUNTED_RATE) ** (ct.deadline - ct.nodes[node]['EF']))
        DC_FINAL += ct.nodes[node]['CF'] / ((1 + DISCOUNTED_RATE) ** (ct.nodes[node]['EF']))
        #print("Scheduled RSBK: ", node, ' ', str(ct.nodes[node]['EF']))
    #print('RS - DC_FINAL: ', DC_FINAL)

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

    all_cost = recursion_calls + it_Shift + it_Compute
    asymptotic = recursion_calls + it_Compute

    #print(edge_verified, "Arestas verificadas em Compute_v_k_l() RS")

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
           DC_FINAL, \
           float(t2 - t1), \
           nx.density(graph)*2*100, \
           all_cost, \
           asymptotic, \
           total_Step_3, \
           call_Compute


#main()