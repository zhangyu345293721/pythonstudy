# -*- coding:utf-8 -*-
'''
author:zhangyu
date:2021/2/13
description:测试死锁
'''
from threading import Thread, Lock
import time

# 创建互斥锁
lock_a = Lock()
lock_b = Lock()


class MyThread1(Thread):
    '''
        线程1
    '''

    def run(self):
        if lock_a.acquire():
            print(self.name, '执行')
            time.sleep(1)
            if lock_b.acquire():
                print(self.name, '执行')
                time.sleep(1)
                lock_b.release()
            lock_a.release()


class MyThread2(Thread):
    '''
        线程2
    '''

    def run(self):
        if lock_b.acquire():
            print(self.name, '执行')
            time.sleep(1)
            if lock_a.acquire():
                print(self.name, '执行')
                time.sleep(1)
                lock_a.release()
            lock_b.release()


if __name__ == '__main__':
    t1 = MyThread1()
    t2 = MyThread2()
    t1.start()
    t2.start()
