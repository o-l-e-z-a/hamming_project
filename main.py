from docopt import docopt
from hamming import Hamming, HammingFileHandler
from service import time_track
from hamming_numpy import HammingNumpy
doc_test = """
Usage:
  main.py run <file_name> [<n>] [<k>] [<no_numpy>] [<no_multi_proc>]
  main.py run -h | --help
  main.py -h | --help
  
  Options:
  -h --help  show this screen.
   
"""


@time_track
def main():
    arguments = docopt(doc_test)
    files = arguments['<file_name>']
    n = arguments['<n>']
    k = arguments['<k>']
    no_numpy = arguments['<no_numpy>']
    no_multi_proc = arguments['<no_multi_proc>']

    hf = HammingFileHandler(files=files, n=n, k=k, communication_channel=Hamming if no_numpy else HammingNumpy)
    hf.run(with_multiprocessing=False if no_multi_proc else True)

if __name__ == '__main__':
    main()
