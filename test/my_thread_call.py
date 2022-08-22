from threading import Thread
from time import sleep
import logging
from random import randint


class MyThread:
    def __init__(self, second_num):
        self.delay = second_num

    def __call__(self):
        logging.info(f'started')
        sleep(self.delay)
        logging.info(f'waited for {self.delay} seconds')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(threadName)s: %(message)s')
    for _ in range(10):
        target = MyThread(randint(1, 5))
        thread = Thread(target=target)
        thread.start()
    logging.info('Usefull message')
