# -*- coding:utf-8 -*-
'''
author:zhangyu
date:2021/2/13
description:创建子进程并运行
'''
from multiprocessing import Process


def run_test() -> None:
    '''
        运行例子
    Returns:
        None
    '''
    print('。。。test.....')


if __name__ == '__main__':
    print('主进程执行')
    # 创建子进程 target接收执行的任务
    p = Process(target=run_test)
    # 调用子进程
    p.start()
