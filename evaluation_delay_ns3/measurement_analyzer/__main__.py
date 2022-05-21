import logging

from .analyzer import main

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
