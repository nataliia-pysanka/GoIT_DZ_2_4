from threading import Thread, RLock
from time import sleep, time
import logging
from random import randint


class MyThread:
    def __init__(self, second_num):
        self.delay = second_num

    def __call__(self, locker):
        logging.info(f'started')
        timer = time()
        locker.acquire()
        sleep(self.delay)
        locker.release()
        logging.info(f'done in {time() - timer} seconds')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(threadName)s: %(message)s')
    lock = RLock()
    for _ in range(10):
        target = MyThread(randint(1, 5))
        thread = Thread(target=target, args=(lock,))
        thread.start()
    logging.info('Usefull message')
