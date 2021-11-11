# from .hamming import Hamming, HammingFileHandler, HammingCoder, HammingMixin, HammingNoise, HammingDecoder
from .hamming import Hamming, HammingFileHandler
# from .matrix import MatrixH,MatrixG, BinaryHammingMatrix
# from .base import BaseFileHandler, BaseNoise, BaseCoder, BaseDecoder, BaseCommunicationChannel
# import base
# import hamming
# import matrix
#
# __all__ = ['hamming', 'base', 'matrix']
__all__ = [str(i) for i in [Hamming, HammingFileHandler]]
