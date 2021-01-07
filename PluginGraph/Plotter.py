# Nodes plotter

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def plt_main_example(algo_name, DC_FINAL, ct):

    layer = 6
    height = 5

    pos = {1: np.array([0, 0.5]),
           2: np.array([1 / layer, 4 / height]), 3: np.array([1 / layer, 2.5 / height]),
           4: np.array([1 / layer, 1 / height]),
           9: np.array([2 / layer, 5 / height]), 5: np.array([2 / layer, 3 / height]),
           6: np.array([2 / layer, 2.5 / height]), 7: np.array([2 / layer, 2 / height]),
           10: np.array([3 / layer, 3 / height]), 11: np.array([3 / layer, 2 / height]),
           8: np.array([3 / layer, 1 / height]),
           12: np.array([4 / layer, 2.5 / height]),
           13: np.array([5 / layer, 2.5 / height]),
           14: np.array([1, 1])}

    nx.draw_networkx(ct, pos, with_labels=True)
    # nx.draw_networkx(st, nx.circular_layout(st), with_labels=True)

    plt.title('Scheduled ' + str(algo_name) + '\n File name: ' + ct.file_name)
    plt.text(-0.15, -0.01, 'Deadline: ' + str(ct.deadline), size=10)
    plt.text(-0.15, -0.07, 'Cash flow:', size=10)
    plt.text(-0.15, -0.12, [ct.nodes[node]['CF'] for node in ct.nodes], size=8)
    if algo_name is not 'Early Tree':
        plt.text(-0.15, -0.19, 'Early finish:', size=10)
        plt.text(-0.15, -0.25, [ct.nodes[node]['EF'] for node in ct.nodes], size=9)
        plt.text(-0.15, -0.32, ('NPV: ' + str(DC_FINAL)), size=10)

    plt.show()


def plt_17(algo_name, DC_FINAL, ct):

    layer = 7
    height = 3
    pos = {1: np.array([0, 0.5]),
           2: np.array([1 / layer, 3 / height]), 3: np.array([1.3 / layer, 2 / height]),
           4: np.array([1 / layer, 1 / height]),
           5: np.array([2 / layer, 3.1 / height]), 6: np.array([2.3 / layer, 2.1 / height]),
           7: np.array([2 / layer, 1.1 / height]),
           8: np.array([3 / layer, 2.8 / height]), 9: np.array([3.3 / layer, 1.8 / height]),
           10: np.array([3 / layer, 0.8 / height]),
           11: np.array([4 / layer, 2.7 / height]), 12: np.array([4.3 / layer, 1.7 / height]),
           13: np.array([4 / layer, 0.7 / height]),
           14: np.array([5 / layer, 2.6 / height]), 15: np.array([5.3 / layer, 1.6 / height]),
           16: np.array([5 / layer, 0.6 / height]),
           17: np.array([1, 1])}

    nx.draw_networkx(ct, pos, with_labels=True)
    # nx.draw_networkx(st, nx.circular_layout(st), with_labels=True)

    plt.title('Scheduled ' + str(algo_name) + '\n File name: ' + ct.file_name)
    plt.text(-0.15, -0.01, 'Deadline: ' + str(ct.deadline), size=10)
    plt.text(-0.15, -0.07, 'Cash flow:', size=10)
    plt.text(-0.15, -0.12, [ct.nodes[node]['CF'] for node in ct.nodes], size=8)
    if algo_name is not 'Early Tree':
        plt.text(-0.15, -0.19, 'Early finish:', size=10)
        plt.text(-0.15, -0.25, [ct.nodes[node]['EF'] for node in ct.nodes], size=9)
        plt.text(-0.15, -0.32, ('NPV: ' + str(DC_FINAL)), size=10)

    plt.show()

def plt_general(algo_name=None, DC_FINAL=0, ct=None):

    nx.draw_networkx(ct, nx.circular_layout(ct), with_labels=True)
    #nx.draw_networkx(ct, nx.planar_layout(ct), with_labels=True)
    #nx.draw_networkx(ct, nx.fruchterman_reingold_layout(ct), with_labels=True)
    #nx.draw_networkx(ct, nx.fruchterman_reingold_layout(ct), with_labels=True)

    if algo_name != None:
        plt.title('Scheduled ' + str(algo_name) + '\n File name: ' + ct.file_name)
        plt.text(-0.15, -0.01, 'Deadline: ' + str(ct.deadline), size=10)
        plt.text(-0.15, -0.07, 'Cash flow:', size=10)
        plt.text(-0.15, -0.12, [ct.nodes[node]['CF'] for node in ct.nodes], size=8)
        if algo_name is not 'Early Tree':
            plt.text(-0.15, -0.19, 'Early finish:', size=10)
            plt.text(-0.15, -0.25, [ct.nodes[node]['EF'] for node in ct.nodes], size=9)
            plt.text(-0.15, -0.32, ('NPV: ' + str(DC_FINAL)), size=10)

    plt.show()