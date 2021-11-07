import random

from base import BaseCoder, BaseDecoder, BaseNoise, BaseCommunicationChannel
from service import config_parser, get_power_of_two
from maxtrix import MatrixG, MatrixH
from errors import NotValidCodeOptions


def hamming_config_parser(config_name):
    config_values = config_parser(config_name, 'n', 'k', 'd')
    print(config_values)
    if len(config_values) == 3 and all(isinstance(value, int) for value in config_values):
        n, k, d = config_values
    else:
        n, k, d = 7, 4, 3
    return n, k, d


class HammingMixin:
    def __init__(self, n, k, d):
        self._n, self._k, self._d = n, k, d
        self.power_of_two = get_power_of_two(self._n)
        self.H = MatrixH(self._n, self._k)
        self.G = MatrixG(self.H, self._n, self._k)
        print(self.H)
        print(self.G)


class HammingCoder(HammingMixin, BaseCoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def encode(self, text):
        c = self.G * text
        print('c', c)
        syndrome = c * self.H
        print('syndrome', syndrome)
        return c


class HammingDecoder(HammingMixin, BaseDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def decode(self, encoded):
        print('encoded with shum', encoded)
        decoded = encoded[:]
        syndrome = encoded * self.H
        print('syndrome', syndrome)
        syndrome_index = int(''.join(str(s) for s in syndrome), 2) - 1
        decoded[syndrome_index] = 0 if decoded[syndrome_index] else 1
        print('decoded', decoded)
        for index_of_power_2 in reversed(self.power_of_two):
            decoded.pop(index_of_power_2)
        print('decoded', decoded)
        return decoded


class HammingNoise(BaseNoise):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def make_noise(self, encoded):
        result = encoded[:]
        random_index = random.randint(0, len(encoded)-1)
        result[random_index] = 0 if result[random_index] else 1
        return result
        # return [0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1]
        # return [0, 1, 0, 1, 1, 0, 1]


class Hamming(BaseCommunicationChannel):
    def __init__(self, config_name='', *args, **kwargs):
        self._n, self._k, self._d = hamming_config_parser(config_name)
        print(self._n, self._k, self._d)
        self.check_options()
        super().__init__(
            coder=HammingCoder(self._n, self._k, self._d),
            decoder=HammingDecoder(self._n, self._k, self._d),
            noise=HammingNoise(),
            *args,
            **kwargs
        )

    def check_options(self):
        """ Проверка кода на корректность"""
        if self._d != 3 or self._d > self._n - self._k + 1 or self._n - self._k != len(get_power_of_two(self._n)):
            raise NotValidCodeOptions


# h = Hamming(text='101010101', config_name=r'configs/config.yaml')
# h = Hamming(text='10101010', config_name=r'configs/config.yaml')
# h = Hamming(text='0101', config_name=r'configs/confi1g.yaml')
h = Hamming(text='010', config_name=r'configs/config.yaml')
h.run_with_noise()
