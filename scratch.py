from sys import argv
from os import EX_OK
from os import path

import time
from random import randint
import threading
from threading import Thread
import socket

import socket

class MyThread(Thread):
    def __init__(self, val):
        Thread.__init__(self)
        self.val = val

    def run(self):
        for i in range(0, self.val):
            print('value %d in thread %s' %(i, self.getName()))

            seconds_to_sleep = randint(1, 5)
            print('%s sleeping for %s secs...' %(self.getName(), seconds_to_sleep))
            time.sleep(seconds_to_sleep)

def run(name, val):
    for i in range(0, val):
        print('value %d in thread %s' %(i, name))

        seconds_to_sleep = randint(1, 5)
        print('%s sleeping for %s secs...' %(name, seconds_to_sleep))
        time.sleep(seconds_to_sleep)

def main(argv):
    """
    t1 = MyThread(4)
    t1.setName('T1')

    t2 = MyThread(8)
    t2.setName('T2')
    
    t1.start()
    t2.start()

    t1.join()
    t2.join()
    """
    
    run('T1', 4)
    run('T2', 8)
    
    return EX_OK

if __name__ == '__main__':
    retval = main(argv)
