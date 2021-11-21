from docopt import docopt

from hamming import Hamming, HammingFileHandler
from hamming_numpy import HammingNumpy
from service import time_track


docopt_str = """
Usage:
  main.py run <file_name> [<n>] [<k>] [<decode_dir>] [--numpy] [--multi_proc] 
  main.py run -h | --help
  main.py -h | --help

  Options:
    -h --help  show this screen.


"""


@time_track
def main():
    arguments = docopt(docopt_str)
    files = arguments['<file_name>']
    n = arguments['<n>']
    k = arguments['<k>']
    numpy = arguments['--numpy']
    multi_proc = arguments['--multi_proc']
    decode_dir = arguments['<decode_dir>']
    hf = HammingFileHandler(files=files, n=n, k=k, communication_channel=HammingNumpy if numpy else Hamming)
    hf.run(
        with_multiprocessing=True if multi_proc else False,
        writed_dir=decode_dir if decode_dir else r'decode'
    )


if __name__ == '__main__':
    main()
