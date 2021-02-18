# -*- coding:utf-8 -*-
'''
author:zhangyu
date:2021/2/13
'''
from time import sleep


def sing() -> None:
    '''
        唱歌
    Returns:
        None
    '''
    for i in range(3):
        print('正在唱歌...%d' % i)
        dance()
        sleep(1)


def dance() -> None:
    '''
        跳舞
    Returns:
        None
    '''
    for i in range(3):
        print('正在跳舞...%d' % i)
        sleep(1)

if __name__ == '__main__':
    sing()
    # dance()
