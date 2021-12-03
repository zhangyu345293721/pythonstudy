# -*- coding:utf-8 -*-
'''
author:zhangyu
date:2021/2/13
'''
#导入队列模块
from multiprocessing import Queue
#创建一个队列
q=Queue(3) #可以指定队列的大小，如果不写默认的队列是无限
#向队列中插入元素
# q.put('消息1')
# q.put('消息2')
# q.put('消息3')
#put方法中可选参数 block=True,timeout=1 队列已经满了，等待1s，如果还是没有空余的空间，则跑队列已满的异常
# q.put('消息4',block=True,timeout=1)
#判断当前队列是否已满
print('判断当前队列是否已满：',q.full())

# if not q.full():
    # q.put('消息4', block=True, timeout=1)

#读取并删除元素get
# print(q.get())
# print(q.get())
# print(q.get())
# if not q.empty():
#     print(q.get(block=True,timeout=1))
#查看队列的大小
print('队列的大小：',q.qsize())
for i in range(q.qsize()):
    print(q.get())


