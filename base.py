from service import file_distribution
from multiprocessing import Pool


class BaseCoder:
    """Кодер канала связи"""

    def encode(self, text):
        """ кодирование """


class BaseDecoder:
    """Декодер канала связи"""

    def decode(self, encoded):
        """ декодирование """


class BaseNoise:
    """Шума канала связи"""

    def make_noise(self, encoded):
        """ добавление шума """


class BaseCommunicationChannel:
    """Базовый класс канала связи"""

    def __init__(self, text='', coder=BaseCoder(), decoder=BaseDecoder(), noise=BaseNoise()) -> None:
        self._text = text
        self._coder = coder
        self._decoder = decoder
        self._noise = noise
        self._encoded, self._decoded, self._encoded_with_noise = '', '', ''

    def run_without_noise(self) -> None:
        """ Передача данных без шума"""
        self._encoded = self._coder.encode(self._text)
        self._decoded = self._decoder.decode(self._encoded)

    def run_with_noise(self) -> None:
        """ Передача данных с шумом"""
        self._encoded = self._coder.encode(self._text)
        self._encoded_with_noise = self._noise.make_noise(self._encoded)
        self._decoded = self._decoder.decode(self._encoded_with_noise)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def encoded(self):
        return self._encoded

    @property
    def decoded(self):
        return self._decoded

    @property
    def encoded_with_noise(self):
        return self._encoded_with_noise


class BaseFileHandler:
    def __init__(self, files, communication_channel=BaseCommunicationChannel()) -> None:
        self._communication_channel = communication_channel
        self._files_names = file_distribution(files)

    def file_handle(self, file):
        self._communication_channel.text = self.read(file)
        self._communication_channel.run_with_noise()
        self.write(f'decoded_{file}', self._communication_channel.decoded)

    def run(self, with_multiprocessing=False):
        if with_multiprocessing:
            pool = Pool()
            pool.map(self.file_handle, self._files_names)
        else:
            for file in self._files_names:
                self.file_handle(file)

    @staticmethod
    def read(file, mode='r', encoding='utf-8'):
        with open(file, mode, encoding=encoding) as f:
            for line in f:
                yield line

    @staticmethod
    def write(file, text, mode='w', encoding='utf-8'):
        with open(file, mode, encoding=encoding) as f:
            f.write(text)
