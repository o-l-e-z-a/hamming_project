import numpy as np

from base import BaseDecoder, BaseCoder, BaseCommunicationChannel
from errors import CheckEncodingError, NotValidCodeOptions
from hamming import check_options, HammingNoise, hamming_cmd_arg_parser
from service import get_power_of_two
from numpy_matrix import get_numpy_g, get_numpy_h


class HammingNumpyMixin:
    """Миксин для добавления матриц G, H"""

    def __init__(self, n, k, d, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._n, self._k, self._d = n, k, d
        self.power_of_two = get_power_of_two(self._n)
        self.H = get_numpy_h(self._n, self._k)
        self.G = get_numpy_g(self.H, self._n, self._k)


class HammingNumpyCoder(HammingNumpyMixin, BaseCoder):
    """ Кодер ал-ма Хэмминга"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def encode(self, text):
        text = np.array([int(i) for i in text], dtype=np.int8)
        c = text @ self.G
        c %= 2
        syndrome = self.H @ c
        syndrome %= 2
        decimal_syndrome = int(''.join(str(s) for s in syndrome), 2)
        if decimal_syndrome:
            raise CheckEncodingError
        return c


class HammingNumpyDecoder(HammingNumpyCoder, BaseDecoder):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def decode(self, encoded):
        decoded = np.copy(encoded)
        syndrome = self.H @ encoded
        syndrome %= 2
        syndrome_index = int(''.join(str(s) for s in syndrome), 2) - 1
        decoded[syndrome_index] = 0 if decoded[syndrome_index] else 1
        for index_of_power_2 in reversed(self.power_of_two):
            decoded = np.delete(decoded, index_of_power_2, 0)
        return decoded


class HammingNumpy(BaseCommunicationChannel):
    def __init__(self, n='', k='', *args, **kwargs) -> None:
        self._n, self._k, self._d = *hamming_cmd_arg_parser(n, k), 3
        print(self._n, self._k, self._d)
        if not check_options(self._n, self._k, self._d):
            raise NotValidCodeOptions
        super().__init__(
            coder=HammingNumpyCoder(self._n, self._k, self._d),
            decoder=HammingNumpyDecoder(self._n, self._k, self._d),
            noise=HammingNoise(),
            *args,
            **kwargs
        )

    def run_without_noise(self) -> None:
        """ Передача данных без шума"""
        self._encoded = self._coder.encode(self._text)
        self._decoded = self._decoder.decode(self._encoded)

    def run_with_noise(self) -> None:
        """ Передача данных с шумом"""
        append_flag = False
        if len(self._text) != self._k:
            append_flag = True
            append_length = self._k - len(self._text)
            self._text += '0'*append_length
        self._encoded = self._coder.encode(self._text)
        self._encoded_with_noise = self._noise.make_noise(self._encoded)
        self._decoded = self._decoder.decode(self._encoded_with_noise)
        if append_flag:
            self._decoded = self._decoded[:append_length]

    @property
    def n(self):
        return self._n

    @property
    def k(self):
        return self._k
