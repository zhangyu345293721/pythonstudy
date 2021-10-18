# -*- coding:utf-8 -*-
'''
author:zhangyu
date:2021/10/15
description:读取文件里面所有题目，然后返回一道或者几道题目
'''
import sys

sys.path.append(".")
import json
import random
from flask import request
import flask

server = flask.Flask(__name__)
data = None


@server.route("/getQuestions", methods=["GET"])
def getQuestions():
    if request.method == "GET":
        num = int(request.args.get("num")) if request.args.get("num") else 1
        global data
        # 如果已经读取了文件就不重复读取
        if not data:
            with open("algo_code.json", 'r') as f:
                line = f.readline()
            data = json.loads(line)
        res = get_questions(num, data)
        response = ""
        for i in range(0, num):
            arr = res[i].split("/")
            # 拼接成html可以解析的字符串
            response += "<a href = " + res[i] + " >" + arr[len(arr) - 2] + "<br>" + "</a>"
        return response
    else:
        raise Exception("Exception!!")


def get_questions(num=1, data=None):
    """
        随机获取leetcode题目
    """
    result = []
    i = 0
    while i < num:
        rand_num = random.randint(1, len(data))
        result.append(data[str(rand_num)])
        i += 1
    return result


if __name__ == '__main__':
    server.run(port=8001, debug=True, host="127.0.0.1", threaded=True)
