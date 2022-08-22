from threading import Thread
from time import sleep
import logging
from random import randint


def thread_func(sleep_time):
    logging.info(f'started')
    sleep(sleep_time)
    logging.info(f'waited for {sleep_time} seconds')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(threadName)s: %(message)s')
    for _ in range(10):
        thread = Thread(target=thread_func, args=(randint(1, 5),))
        thread.start()
    print(thread.is_alive())
    # The mainthread is waiting for ending of thread # 10 and then print Usefull message
    thread.join()
    print(thread.is_alive())
    logging.info('Usefull message')
