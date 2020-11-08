# Original Early Tree #

def forward_pass():
    et_suc[-1] = [1]
    et_pred[0] = [len(et_pred)]

    et_fs[0] = 0
    et_fs[len(et_fs) - 1] = delta_n

    for j in range(2, len(gp_duration)):
        et_fs[j-1] = 0;
        for i in gp_pred[j-1]:
            if (et_fs[i-1] + gp_duration[j-1]) > et_fs[j-1]:
                et_fs[j-1] = et_fs[i-1] + gp_duration[j-1]
                i_star = i
        et_suc[i_star-1].append(j)
        et_pred[j-1].append(i_star)


#####################
#       Main        #
#####################

# Original project #
"""
global DC_FINAL
"""
delta_n = 44

#List of predecessors (early tree)
et_pred = [[]     ,  [],     [], [],  [],  [],    [],  [],  [],  [],  [],       [],     [],         []]
#List of successors (original graph)
et_suc  = [[]     ,  [],     [], [],  [],  [],    [],  [],  [],  [],  [],       [],     [],         []]

#List of early start (current tree)
et_es  = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
et_fs  = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Gabarito
#et_es   = [0      ,   0,      0,  0,   6,   6,     6,   8,   7,   7,   8,       12,     15,     delta_n]
#List of early finish (current tree)
#et_ef   = [0      ,   6,      5,  3,   6,  11,     7,   8,  10,   9,   9,       14,     19,     delta_n]

#List of predecessors (original graph)
gp_pred = [[]     , [1],    [1],[1], [3], [3],   [3], [4,7], [2], [5], [7],[6,10,11], [8,12],      [9,13]]
#List of successors (original graph)
gp_suc  = [[2,3,4], [9],[5,6,7],[8],[10],[12],[8,11],[13],[14],[12],[12],     [13],   [14],         []]
#List of duration (original graph)
gp_duration  = [0      ,   6,      5,  3,   1,   6,     2,   1,   4,   3,   2,        3,      5,           0]


forward_pass()
print("Early Tree start:")
print(et_es)
print("Early Tree finish:")
print(et_fs)

print("Pred:")
print(et_pred)
print("Succ:")
print(et_suc)