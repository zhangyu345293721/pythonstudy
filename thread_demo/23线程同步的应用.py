# -*- coding:utf-8 -*-
'''
author:zhangyu
date:2021/2/13
'''
from threading import Thread,Lock
import time
#创建3把互斥锁
lock1=Lock()
lock2=Lock()
lock3=Lock()
#对lock2和lock3上锁
lock2.acquire()
lock3.acquire()

class Task1(Thread):
    def run(self):
        while True:
            if lock1.acquire():
                print('...task1...')
                time.sleep(1)
                #释放lock2的锁
                lock2.release()

class Task2(Thread):
    def run(self):
        while True:
            if lock2.acquire():
                print('...task2...')
                time.sleep(1)
                lock3.release()

class Task3(Thread):
    def run(self):
        while True:
            if lock3.acquire():
                print('...task3...')
                time.sleep(1)
                lock1.release()

if __name__ == '__main__':
    t1=Task1()
    t2=Task2()
    t3=Task3()
    t1.start()
    t2.start()
    t3.start()