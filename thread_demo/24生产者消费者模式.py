# -*- coding:utf-8 -*-
'''
author:zhangyu
date:2021/2/13
'''
from threading import Thread
from  queue import Queue
import time
class Producter(Thread):
    def run(self):
        global queue
        count=0
        while True:
            #判断队列的大小
            if queue.qsize()<1000:
                for i in range(100):
                    count+=1
                    msg='生产第'+str(count)+'个产品'
                    queue.put(msg)
                    print(msg)
                time.sleep(0.5)
class Consumer(Thread):
    def run(self):
        global queue
        while True:
            if queue.qsize()>100:
                for i in range(10):
                    msg=self.name+'消费'+queue.get()
                    print(msg)
                time.sleep(1)

if __name__ == '__main__':
    queue=Queue()
    p=Producter()
    c=Consumer()
    p.start()
    time.sleep(1)
    c.start()