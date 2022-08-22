from threading import Thread
from time import sleep
import logging
from random import randint


class MyThread(Thread):
    def __init__(self, second_num):
        super().__init__()
        self.delay = second_num

    def run(self):
        logging.info(f'started')
        sleep(self.delay)
        logging.info(f'waited for {self.delay} seconds')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(threadName)s: %(message)s')
    for _ in range(10):
        t = MyThread(randint(1, 5))
        t.start()
    logging.info('Usefull message')
