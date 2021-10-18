# -*- coding:utf-8 -*-
'''
author:zhangyu
date:2021/10/15
description:获取pdf里面的链表，并将连接持久化存储到文档当中
'''

import PyPDF2
import json

url_list = []
for i in range(1, 10):
    if i == 5:
        for j in range(1, 3):
            dir = "D:\\算法\\" + str(i) + "\\" + str(i) + "_" + str(j) + ".pdf"
            PDFFile = open(dir, 'rb')
            PDF = PyPDF2.PdfFileReader(PDFFile)
            pages = PDF.getNumPages()
            key = '/Annots'
            uri = '/URI'
            ank = '/A'
            for page in range(pages):
                # print("Current Page: {}".format(page))
                pageSliced = PDF.getPage(page)
                pageObject = pageSliced.getObject()
                if key in pageObject.keys():
                    ann = pageObject[key]
                    for a in ann:
                        u = a.getObject()
                        if uri in u[ank].keys():
                            # print(u[ank][uri])
                            url_list.append(u[ank][uri])
    else:
        dir = "D:\\算法\\" + str(i) + "\\" + str(i) + ".pdf"
        PDFFile = open(dir, 'rb')
        PDF = PyPDF2.PdfFileReader(PDFFile)
        pages = PDF.getNumPages()
        # print(pages)
        key = '/Annots'
        uri = '/URI'
        ank = '/A'
        for page in range(pages):
            # print("Current Page: {}".format(page))
            pageSliced = PDF.getPage(page)
            pageObject = pageSliced.getObject()
            if key in pageObject.keys():
                ann = pageObject[key]
                # print(ann)
                for a in ann:
                    u = a.getObject()
                    print(u)
                    if uri in u[ank].keys():
                        # print(u[ank][uri])
                        print(u[ank])
                        url_list.append(u[ank][uri])
questions = set(url_list)
result = {}
index = 1
for q in questions:
    result[index] = q
    index += 1

print(result)
print(len(result))

q_data = json.dumps(result)
print(q_data)
with open("d:/code.json", "w") as f:
    f.write(q_data)
