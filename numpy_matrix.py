import numpy as np

from service import get_power_of_two


def get_numpy_h(n, k):
    matrix = [[int(j) for j in bin(i)[2:].zfill(n - k)] for i in range(1, n + 1)]
    matrix = list(zip(*matrix))
    H_np = np.array(matrix, dtype=np.int8)
    return H_np


def get_numpy_g(H_np, n, k):
    _H_np = np.copy(H_np).swapaxes(0, 1)
    power_of_two = get_power_of_two(n)

    for i in reversed(power_of_two):
        _H_np = np.delete(_H_np, i, 0)
        _H_np = np.vstack([_H_np, [H_np.swapaxes(0, 1)[i]]])
    _G = np.eye(k, k, dtype=np.int8)
    _G = np.column_stack([_G, _H_np[0:k]])

    for i in reversed(power_of_two):
        _H_np = np.delete(_H_np, i, 0)
        _H_np = np.vstack([_H_np, [H_np.swapaxes(0, 1)[i]]])
    G = np.copy(_G).swapaxes(0, 1)

    count = 0
    for i in power_of_two:
        G = np.delete(G, -1, 0)
        G = np.insert(G, i, _G.swapaxes(0, 1)[-1 + count], 0)
        count -= 1
    G = G.swapaxes(0, 1)
    return G
