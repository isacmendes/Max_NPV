import numpy as np

# VERSION 1
###############
# nr_layers = 32
# nr_vertices = 1528
# nr_vertices_for_layers  = []
#
# print(nr_vertices_for_layers)
#
# for i in range(50):
#     range_random = nr_vertices - nr_layers
#     nr_vertices_for_layers = []
#
#     for idx in range(nr_layers):
#         nr_vertices_for_layers.append(1)
#
#     for idx in range(len(nr_vertices_for_layers)):
#         current_value = np.random.randint(0, range_random + 1, 1)[0]
#
#         if range_random >= current_value:
#             if idx == len(nr_vertices_for_layers) - 1:
#                 current_value = nr_vertices - np.sum(nr_vertices_for_layers)
#                 nr_vertices_for_layers[idx] = current_value + 1
#             else:
#                 nr_vertices_for_layers[idx] = (current_value + 1)//2
#             range_random -= current_value
#
#     print(nr_vertices_for_layers, np.sum(nr_vertices_for_layers))

# VERSION 2
############
import matplotlib.pyplot as plt
import numpy as np

nr_layers = 10
mean_vertices = 5
deviation_standard = 1

for i in range(50):
    dados = np.random.normal(loc=10, scale=3, size=5)
    sigma = 3
    mu = 5
    print(dados, np.sum(dados, dtype='int64'))

count, bins, ignored = plt.hist(dados, 30, density=True)
plt.plot(bins, 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(- (bins - mu) ** 2 / (2 * sigma ** 2)), linewidth = 2, color = 'r')
plt.show()
