import random
import os.path

import bitstring

from base import BaseCoder, BaseDecoder, BaseNoise, BaseCommunicationChannel, BaseFileHandler
from service import config_parser, get_power_of_two, make_file_dir
from matrix import MatrixG, MatrixH
from errors import NotValidCodeOptions, CheckEncodingError


def hamming_config_parser(config_name) -> tuple[int]:
    """ парсер парамметров кода Хэмминга """
    config_values = config_parser(config_name, 'n', 'k', 'd')
    if len(config_values) == 3 and all(isinstance(value, int) for value in config_values):
        n, k, d = config_values
    else:
        n, k, d = 7, 4, 3
    return n, k, d


class HammingMixin:
    """Миксин для добавления матриц G, H"""
    def __init__(self, n, k, d, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._n, self._k, self._d = n, k, d
        self.power_of_two = get_power_of_two(self._n)
        self.H = MatrixH(self._n, self._k)
        self.G = MatrixG(self.H, self._n, self._k)


class HammingCoder(HammingMixin, BaseCoder):
    """ Кодер ал-ма Хэмминга"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # print(self.H)
        # print(self.G)

    def encode(self, text) -> list[int]:
        c = self.G * text
        # print('c', c)
        syndrome = c * self.H
        decimal_syndrome = int(''.join(str(s) for s in syndrome), 2)
        if decimal_syndrome:
            raise CheckEncodingError

        # print('syndrome', syndrome)
        # print('decimal_syndrome', decimal_syndrome)
        return c


class HammingDecoder(HammingMixin, BaseDecoder):
    """ Декодер ал-ма Хэмминга"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def decode(self, encoded) -> list[int]:
        # print('encoded with shum', encoded)
        decoded = encoded[:]
        syndrome = encoded * self.H
        # print('syndrome', syndrome)
        syndrome_index = int(''.join(str(s) for s in syndrome), 2) - 1
        decoded[syndrome_index] = 0 if decoded[syndrome_index] else 1
        # print('decoded', decoded)
        for index_of_power_2 in reversed(self.power_of_two):
            decoded.pop(index_of_power_2)
        # print('decoded', decoded)
        return decoded


class HammingNoise(BaseNoise):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def make_noise(self, encoded) -> list[int]:
        result = encoded[:]
        random_index = random.randint(0, len(encoded)-1)
        result[random_index] = 0 if result[random_index] else 1
        return result
        # return [0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1]
        # return [0, 1, 0, 1, 1, 0, 1]


class Hamming(BaseCommunicationChannel):
    def __init__(self, config_name='', *args, **kwargs) -> None:
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

    def check_options(self) -> None:
        """ Проверка кода на корректность"""
        if self._d != 3 or self._d > self._n - self._k + 1 or self._n - self._k != len(get_power_of_two(self._n)):
            raise NotValidCodeOptions

    @property
    def n(self):
        return self._n

    @property
    def k(self):
        return self._k


class HammingFileHandler(BaseFileHandler):
    def __init__(self, config_name, *args, **kwargs):
        super().__init__(communication_channel=Hamming(config_name=config_name), *args, **kwargs)

    def file_handle(self, file):
        """ чтение информации из файла, запуск канала связи, запись результата в файл"""
        decoded = ''
        for text in self.read_binary(file):
            step = self._communication_channel.k
            for i in range(0, len(text), step):
                self._communication_channel.text = text[i:i+step]
                self._communication_channel.run_with_noise()
                decoded += ''.join(str(s) for s in self._communication_channel.decoded[:len(text[i:i+step])])
            self.write_binary(file, decoded, 'decode')

    def read_binary(self, file, mode='r', encoding='utf-8'):
        """ чтение из файла в бинарном виде"""
        b = bitstring.ConstBitStream(filename=file)
        k = self._communication_channel.k
        chunk_size = k if not k % 8 else k * 8
        length = len(b) // chunk_size if not len(b) % chunk_size else len(b) // chunk_size + 1
        for i in range(length):
            if b.pos + chunk_size > len(b):
                reading = b.read(len(b) - b.pos)
            else:
                reading = b.read(chunk_size)
            yield reading.bin

    def write_binary(self, file, text, mode='w', encoding='utf-8', writed_dir='decode'):
        """ запись из файла"""
        make_file_dir(file, writed_dir)
        f = open(os.path.join(writed_dir, file), 'wb')
        bitstring.Bits(bin=text).tofile(f)
