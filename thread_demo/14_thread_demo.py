# -*- coding:utf-8 -*-
'''
author:zhangyu
date:2021/2/13
description:
'''

import _thread
import time


def fun1() -> None:
    '''
        方法1
    Returns:
        None
    '''
    print('开始运行fun1')
    time.sleep(4)
    print('运行fun1结束')


def fun2() -> None:
    '''
        方法2
    Returns:
        None
    '''
    print('开始运行fun2')
    time.sleep(2)
    print('运行fun2结束')


if __name__ == '__main__':
    print('开始运行')
    # 创建线程
    _thread.start_new_thread(fun1, ())
    _thread.start_new_thread(fun2, ())
    time.sleep(7)
