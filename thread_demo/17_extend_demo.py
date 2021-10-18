# -*- coding:utf-8 -*-
'''
author:zhangyu
date:2021/2/13
description:继承thread
'''
import threading
import time


def fun1(delay: float) -> None:
    '''
        方法1
    Args:
        delay:延迟时间
    Returns:
        None
    '''
    print('线程{}执行fun1'.format(threading.current_thread().getName()))
    time.sleep(delay)
    print('线程{}执行fun1结束'.format(threading.current_thread().getName()))


def fun2(delay: float) -> None:
    '''
           方法2
       Args:
           delay:延迟时间
       Returns:
           None
       '''
    print('线程{}执行fun2'.format(threading.current_thread().getName()))
    time.sleep(delay)
    print('线程{}执行fun2结束'.format(threading.current_thread().getName()))


class MyThread(threading.Thread):
    '''
        创建一个类MyThread 继承threading.Thread
    '''
    # 重新构造方法
    def __init__(self, func, name, args):
        super().__init__(target=func, name=name, args=args)

    def run(self):
        self._target(*self._args)


if __name__ == '__main__':
    print('开始运行')
    t1 = MyThread(fun1, 'thread-1', (2,))
    t2 = MyThread(fun2, 'thread-2', (4,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
