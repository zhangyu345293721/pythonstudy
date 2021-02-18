# -*- coding:utf-8 -*-
'''
author:zhangyu
date:2021/2/13
'''
import _thread
import time
def fun1(thread_name,delay):
    print('开始运行fun1，线程的名：',thread_name)
    time.sleep(delay)
    print('运行fun1结束')

def fun2(thread_name,delay):
    print('开始运行fun2，线程的名：',thread_name)
    time.sleep(delay)
    print('运行fun2结束')

if __name__ == '__main__':
    print('开始运行')
    #创建线程
    _thread.start_new_thread(fun1,('thread-1',3))
    _thread.start_new_thread(fun2,('thread-2',3))
    time.sleep(7)
