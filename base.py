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

    def __init__(self, text='', coder=BaseCoder(), decoder=BaseDecoder(), noise=BaseNoise()):
        self._text = text
        self._coder = coder
        self._decoder = decoder
        self._noise = noise
        self._encoded, self._decoded, self._encoded_with_noise = '', '', ''

    def run_without_noise(self):
        """ Передача данных без шума"""
        self._encoded = self._coder.encode(self._text)
        self._decoded = self._decoder.decode(self._encoded)

    def run_with_noise(self):
        """ Передача данных с шумом"""
        self._encoded = self._coder.encode(self._text)
        self._encoded_with_noise = self._noise.make_noise(self._encoded)
        self._decoded = self._decoder.decode(self._encoded_with_noise)
