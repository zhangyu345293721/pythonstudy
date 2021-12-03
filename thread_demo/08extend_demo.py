# -*- coding:utf-8 -*-
'''
author:zhangyu
date:2021/2/13
'''
#导入模块
from multiprocessing import Process
from time import sleep
import time
#定义类
class ClockProcess(Process):
    #重新初始化方法
    def __init__(self,interval):
        Process.__init__(self)
        self.interval=interval

    #重新run()
    def run(self):
        print('子进程开始执行的时间:{}'.format(time.ctime()))
        sleep(self.interval)
        print('子进程结束的时间：{}'.format(time.ctime()))

if __name__ == '__main__':
    #创建子进程
    p=ClockProcess(3)
    #调用子进程
    p.start()
    p.join()
    print('主进程执行完')


