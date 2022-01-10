# -*- coding:utf-8 -*-
'''
author:zhangyu
date:2021/2/13
'''
#导入模块
from multiprocessing import Process
num=10
def work1():
    global num
    num+=5
    print('子进程1运行后：num的值',num)

def work2():
    global num
    num+=10
    print('子进程2运行后：num的值',num)

if __name__ == '__main__':
    print('主进程开始运行')
    #创建子进程
    p1=Process(target=work1)
    p2=Process(target=work2)
    #启动子进程
    p1.start()
    p2.start()
    #主进程等待子进程结束
    p1.join()
    p2.join()
    print('全局变量num：',num)