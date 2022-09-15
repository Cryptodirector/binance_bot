import os
import time


def sync():
    try:
        while True:
            os.system('w32tm /resync')
            time.sleep(10)
            sync()
    except:
        sync()


def main():
    sync()


if __name__ == '__main__':
    main()
