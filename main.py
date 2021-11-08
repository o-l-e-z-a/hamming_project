from hamming import Hamming, HammingFileHandler
from service import time_track


@time_track
def main():
    # h = Hamming(text='101010101', config_name=r'configs/config.yaml')
    # h = Hamming(text='10101010', config_name=r'configs/config.yaml')
    # h = Hamming(text='1', config_name=r'configs/config.yaml')
    # h = Hamming(text='010', config_name=r'configs/config.yaml')
    # h.run_with_noise()

    # hf = HammingFileHandler(config_name=r'configs/config.yaml', files='forarchive/text.txt')
    hf = HammingFileHandler(config_name=r'configs/config.yaml', files='forarchive')
    # hf = HammingFileHandler(config_name=r'configs/config.yaml', files='required_set.txt')
    hf.run(with_multiprocessing=True)
    # hf.run(with_multiprocessing=False)


if __name__ == '__main__':
    main()
