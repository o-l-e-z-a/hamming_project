from service import get_power_of_two


class BinaryHammingMatrix:
    """ Двоичная матрица"""
    def __init__(self, n, k):
        self._n = n
        self._k = k
        self._matrix = [[0 for i in range(n)] for i in range(k)]

    def size(self):
        return self._n, self._k

    def __len__(self):
        return len(self._matrix)

    @property
    def n(self):
        return self._n

    @property
    def k(self):
        return self._k

    def __mul__(self, other):
        """Умножение на вектор"""
        other_indexes = [i for i in range(len(other)) if other[i] == '1']
        return [[column[i] for i in other_indexes].count('1') % 2 for column in list(zip(*self._matrix))]

    def __rmul__(self, other):
        other_indexes = [i for i in range(len(other)) if other[i] == 1]
        return [[column[i] for i in other_indexes].count('1') % 2 for column in self._matrix]

    def __getitem__(self, index):
        return self._matrix[index]

    def __setitem__(self, index, value):
        self._matrix[index] = value

    def __repr__(self):
        result = f'{self.__class__.__name__}'
        for row in self._matrix:
            result += f'{row}\n'
        result += '\n'
        return result


class MatrixH(BinaryHammingMatrix):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._matrix = [[j for j in bin(i)[2:].zfill(self._n - self._k)] for i in range(1, self._n + 1)]
        self._matrix = list(zip(*self._matrix))


class MatrixG(BinaryHammingMatrix):
    def __init__(self, H, *args, **kwargs):
        super().__init__(*args, **kwargs)
        H_ = self.get_h_(H)
        G_ = self.get_g_(H_)
        self._matrix = self.get_g(G_)

    def get_h_(self, H):
        H_ = list(zip(*H))
        powers_of_two = get_power_of_two(self._n)
        for index_of_power_2 in reversed(powers_of_two):
            H_.append(H_.pop(index_of_power_2))
        return H_

    def get_g_(self, H_):
        G_ = [['1' if i == j else '0' for i in range(self._k)] for j in range(self._k)]
        for i in range(self._k):
            G_[i] += H_[i]
        G_ = list(zip(*G_))
        return G_

    def get_g(self, G_):
        powers_of_two = get_power_of_two(self._n)
        for index_of_power_2 in powers_of_two:
            G_.insert(index_of_power_2, G_.pop(-1))
        return list(zip(*G_))
