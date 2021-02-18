# -*- coding:utf-8 -*-
'''
author:zhangyu
date:2021/2/13
description:创建子进程并传递参数
'''
from multiprocessing import Process
from time import sleep


# 定义任务的函数
def run_test(name, age, **kwargs) -> None:
    '''
        运行方法
    Args:
        name: 名字
        age: 年龄
        **kwargs: 字典
    Returns:
        None
    '''
    print('子进程正在运行 name的值:%s ,age的值：%d' % (name, age))
    print('字典kwargs:', kwargs)


if __name__ == '__main__':
    print('主进程开始执行')
    # 创建子进程
    # p=Process(target=run_test,args=('test',),kwargs={'key':12})
    p = Process(target=run_test, args=('test', 23), kwargs={'key': 12})
    # 调用子进程
    p.start()
