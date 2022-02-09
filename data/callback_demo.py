# -*- coding:utf-8 -*-
'''
author:zhangyu
description:回调函数demo
'''


# 生成一个2k形式的偶数
def double(x):
    '''
        获取偶数
    Args:
        x: 数值
    Returns:
        回调函数1
    '''
    return x * 2


def quadruple(x):
    '''
        生成一个4k形式的偶数
    Args:
        x: 数值
    Returns:
        回调函数2
    '''
    return x * 4


def getOddNumber(k, getEvenNumber):
    '''
        中间函数
        接受一个生成偶数的函数作为参数
    Args:
        k: 数k
        getEvenNumber: 获取基数
    Returns:
        返回一个奇数
    '''
    return 1 + getEvenNumber(k)


if __name__ == "__main__":
    k = 1
    res = getOddNumber(k, double)
    print(res)
    res = getOddNumber(k, quadruple)
    print(res)
    res = getOddNumber(k, lambda x: x * 8)
    print(res)
