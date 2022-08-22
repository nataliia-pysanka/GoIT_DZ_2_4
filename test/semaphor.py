from threading import Thread, Semaphore
from time import sleep, time
import logging
from random import randint


class MyThread:
    def __init__(self, second_num):
        self.delay = second_num

    def __call__(self, cond, name):
        cond.acquire()
        logging.info(f'{name} got semaphore')
        sleep(self.delay)
        cond.release()
        logging.info(f'{name} finish')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(threadName)s: %(message)s')
    pool = Semaphore(3)
    for i in range(10):
        name = f'Thread-{i}'
        target = MyThread(randint(1, 5))
        thread = Thread(target=target, args=(pool, name))
        thread.start()
    logging.info('Usefull message')
