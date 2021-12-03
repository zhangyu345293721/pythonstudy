# -*- coding:utf-8 -*-
'''
author:zhangyu
date:2021/2/13
'''
#导入模块
import multiprocessing
import time
#进程执行的任务函数
def func(msg):
    print('start:',msg)
    time.sleep(3)
    print('end:',msg)

if __name__ == '__main__':
    #创建初始化3的进程池
    pool=multiprocessing.Pool(3)
    #添加任务
    for i in range(1,6):
        msg='任务%d'%i
        pool.apply_async(func,(msg,))

    #如果进程池不再接收新的请求 调用close
    pool.close()
    #等待子进程结束
    pool.join()