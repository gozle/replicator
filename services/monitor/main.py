import time
from lib.stoppable_thread import StoppableThread

from .agents import *


if __name__ == '__main__':
    existence_scanner_thread = StoppableThread(target=existence_scanner)
    fs_scanner_thread = StoppableThread(target=fs_scanner)

    existence_scanner_thread.start()
    fs_scanner_thread.start()

    try:
        while True:
            time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        print('Received keyboard interrupt, quitting threads.')
        existence_scanner_thread.stop()
        fs_scanner_thread.stop()
