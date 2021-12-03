# -*- coding:utf-8 -*-
'''
author:zhangyu
date:2021/2/13
'''
#导入模块
from multiprocessing import Process
from time import sleep
def work1(interval):
    print('执行work1')
    sleep(interval)
    print('end work1')

def work2(interval):
    print('执行work2')
    sleep(interval)
    print('end work2')

def work3(interval):
    print('执行work3')
    sleep(interval)
    print('end work3')

if __name__=='__main__':
    print('执行主进程')
    p1=Process(target=work1,args=(4,))
    p2=Process(target=work2,args=(2,))
    p3=Process(target=work3,args=(3,))
    #调用子进程
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()
    print('p1.name:',p1.name)
    print('p2.name:',p2.name)
    print('p3.name:',p3.name)
    print('主进程执行完')

