import random
import os.path

import bitstring

from base import BaseCoder, BaseDecoder, BaseNoise, BaseCommunicationChannel, BaseFileHandler
from service import config_parser, get_power_of_two, make_file_dir
from matrix import MatrixG, MatrixH
from errors import NotValidCodeOptions, CheckEncodingError


def check_options(n, k, d) -> bool:
    """ Проверка кода на корректность"""
    if d != 3 or d > n - k + 1 or n - k != len(get_power_of_two(n)):
        return False
    return True


def hamming_config_parser(config_name) -> tuple:
    """ парсер парамметров кода Хэмминга """
    config_values = config_parser(config_name, 'n', 'k', 'd')
    if len(config_values) == 3 and all(isinstance(value, int) for value in config_values):
        n, k, d = config_values
    else:
        n, k, d = 7, 4, 3
    return n, k, d


def hamming_cmd_arg_parser(n=255, k=247) -> tuple:
    """ парсер парамметров кода Хэмминга из командной строки """
    parameters = 'параметры командной строки'
    use_str = ', используем n=255, k=247'
    try:
        return int(n), int(k)
    except ValueError:
        n = k = None
    if not all([k, n]):
        print(f'{parameters.capitalize()} не заданы{use_str}')
    else:
        print(f'Неверные {parameters}{use_str}')
    return 255, 247


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

    def encode(self, text) -> list:
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

    def decode(self, encoded) -> list:
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

    def make_noise(self, encoded) -> list:
        result = encoded[:]
        random_index = random.randint(0, len(encoded)-1)
        result[random_index] = 0 if result[random_index] else 1
        return result


class Hamming(BaseCommunicationChannel):
    def __init__(self, n='', k='', config_name='', *args, **kwargs) -> None:
        self._n, self._k, self._d = *hamming_cmd_arg_parser(n, k), 3
        print(self._n, self._k, self._d)
        if not check_options(self._n, self._k, self._d):
            raise NotValidCodeOptions
        super().__init__(
            coder=HammingCoder(self._n, self._k, self._d),
            decoder=HammingDecoder(self._n, self._k, self._d),
            noise=HammingNoise(),
            *args,
            **kwargs
        )

    @property
    def n(self):
        return self._n

    @property
    def k(self):
        return self._k


class HammingFileHandler(BaseFileHandler):
    def __init__(self, config_name='', n='', k='', communication_channel=Hamming, *args, **kwargs):
        super().__init__(communication_channel=communication_channel(n=n, k=k), *args, **kwargs)

    def file_handle(self, file, writed_dir='decode'):
        """ чтение информации из файла, запуск канала связи, запись результата в файл"""
        make_file_dir(file, writed_dir)
        # for text in self.read_binary(file):
        #     pass
        decoded = ''
        for text in self.read_binary(file):
            step = self._communication_channel.k
            for i in range(0, len(text), step):
                self._communication_channel.text = text[i:i+step]
                self._communication_channel.run_with_noise()
                decoded += ''.join(str(s) for s in self._communication_channel.decoded[:len(text[i:i+step])])
        # decoded = ''.join(str(i) for i in [1 for i in range(255)])
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
        # f = open(os.path.abspath(os.path.join(writed_dir, file)), 'wb')
        # bitstring.Bits(bin=text).tofile(f)
        with open(os.path.abspath(os.path.join(writed_dir, file)), 'wb') as f:
            bitstring.Bits(bin=text).tofile(f)

