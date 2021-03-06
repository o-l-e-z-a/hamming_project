from typing import List, Tuple

from service import get_power_of_two


class BinaryHammingMatrix:
    """ Двоичная матрица"""
    def __init__(self, n: int, k: int) -> None:
        self._n = n
        self._k = k
        self._matrix = [[0 for i in range(n)] for i in range(k)]

    def size(self) -> Tuple[int]:
        return self._n, self._k

    def __len__(self) -> int:
        return len(self._matrix)

    @property
    def n(self):
        return self._n

    @property
    def k(self):
        return self._k

    @property
    def matrix(self):
        return self._matrix

    def __mul__(self, other: List[str]) -> list:
        """Умножение матрицы на вектор"""
        other_indexes = [i for i in range(len(other)) if other[i] == '1']
        return [[column[i] for i in other_indexes].count('1') % 2 for column in list(zip(*self._matrix))]

    def __rmul__(self, other: list) -> list:
        """Умножение вектора на матрицы"""
        other_indexes = [i for i in range(len(other)) if other[i] == 1]
        return [[row[i] for i in other_indexes].count('1') % 2 for row in self._matrix]

    def __getitem__(self, index) -> list:
        return self._matrix[index]

    def __setitem__(self, index, value) -> None:
        self._matrix[index] = value

    def __repr__(self) -> str:
        result = f'{self.__class__.__name__}\n'
        for row in self._matrix:
            result += f'{row}\n'
        result += '\n'
        return result


class MatrixH(BinaryHammingMatrix):
    """ Проверочная матрица"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._matrix = [[j for j in bin(i)[2:].zfill(self._n - self._k)] for i in range(1, self._n + 1)]
        self._matrix = list(zip(*self._matrix))


class MatrixG(BinaryHammingMatrix):
    """ Порождающая матрица"""
    def __init__(self, H, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        H_ = self.get_h_(H)
        G_ = self.get_g_(H_)
        self._matrix = self.get_g(G_)

    def get_h_(self, H) -> list:
        """ Получение промежуточной матрицы H` из проверочной матрицы H"""
        H_ = list(zip(*H))
        powers_of_two = get_power_of_two(self._n)
        for index_of_power_2 in reversed(powers_of_two):
            H_.append(H_.pop(index_of_power_2))
        return H_

    def get_g_(self, H_) -> list:
        """ Получение промежуточной матрицы G` из промежуточной матрицы H`"""
        G_ = [['1' if i == j else '0' for i in range(self._k)] for j in range(self._k)]
        for i in range(self._k):
            G_[i] += H_[i]
        G_ = list(zip(*G_))
        return G_

    def get_g(self, G_) -> list:
        """ Получение порождающей матрицы G из промежуточной матрицы G`"""
        powers_of_two = get_power_of_two(self._n)
        for index_of_power_2 in powers_of_two:
            G_.insert(index_of_power_2, G_.pop(-1))
        return list(zip(*G_))
