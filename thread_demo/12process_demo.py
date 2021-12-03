# -*- coding:utf-8 -*-
'''
author:zhangyu
date:2021/2/13
'''
#导入模块
from multiprocessing import Process,Queue
from time import sleep
#定义写入的方法
def write(q):
    a=['a','b','c','d']
    for i in a:
        print('开始写入的值：%s'%i)
        q.put(i)
        sleep(1)

def reader(q):
    for i in range(q.qsize()):
        print('读取到的值：%s'%q.get())
        sleep(1)

if __name__ == '__main__':
    #创建队列
    q=Queue()
    #创建进程
    pw=Process(target=write,args=(q,))
    pr=Process(target=reader,args=(q,))
    pw.start()
    pw.join()
    pr.start()
    pr.join()