# -*- coding:utf-8 -*-
'''
author:zhangyu
date:2022/1/11
description:统计货箱在暂存区时间已经货箱搬运次数
'''
from typing import Dict, Tuple, List
from datetime import datetime
import pandas as pd


def get_box_buffer_area_time(robot_task_event: pd.DataFrame) -> Dict[str, Tuple[str, str]]:
    '''
        根据robot_task_event事件获取货箱去暂存区的开始时间和结束时间
    Args:
        robot_task_event:机器人事件，包含task_id,instruction,exe_status,box_code,execute_time,update_time,robot_type等字段
    Returns:
        箱子在缓存区开始时间和结束数据的字典，key为箱子编号，value为（start_time,end_time）的链表
    '''
    boxes = {}
    for k, v in robot_task_event.groupby(['box_code']):
        v = v[v['exe_status'] != 'CANCELED']
        v = v.sort_values(by="update_time", ascending=True)
        box_time = []
        start = None
        end = None
        for ind, row in v.iterrows():
            if row['instruction'] == 'GO_RETURN_BOX' and row['robot_type'] == 'RS5-D':
                start = row['update_time']
                if end:
                    start = row['execute_time']
                    box_time.append((min(end, start), max(end, start)))
                    start = None
                    end = None
            if row['instruction'] == 'ADJUST_MECHANISM_HEIGHT' and row['robot_type'] == 'P40':
                end = row['update_time']
                if start:
                    box_time.append((min(end, start), max(end, start)))
                    start = None
                    end = None
        boxes[k] = box_time
    return boxes


def get_box_carry_count(robot_task_event: pd.DataFrame) -> Dict[str, List]:
    '''
        获取货箱在搬运次数
    Args:
         robot_task_event:机器人事件，包含task_id,instruction,exe_status,box_code,execute_time,update_time,robot_type等字段
    Returns:
        箱子在缓存区开始时间和结束数据的字典，key为箱子编号，value为搬运次数
    '''
    box_time = {}
    for k, v in robot_task_event.groupby(['box_code']):
        v = v[v['exe_status'] != 'CANCELED']
        v = v.sort_values(by="update_time", ascending=True)
        for ind, row in v.iterrows():
            if row['instruction'] == 'ADJUST_MECHANISM_HEIGHT' and row['robot_type'] == 'P40':
                if k in box_time:
                    box_time[k] += 1
                else:
                    box_time[k] = 1
    for box_code in box_time:
        box_time[box_code] = int(box_time[box_code] / 2)
    return box_time


def get_box_stay_time(boxes: Dict[str, List]) -> Dict[str, List]:
    '''
        获取货箱停留在暂存区时间
    Args:
         boxes:货箱状态事件
    Returns:
        箱子在缓存区开始时间和结束数据的字典，key为箱子编号，value为搬运时间链表(停留时间为秒)
    '''
    box_stay_time = {}
    for b in boxes:
        res = []
        for tup in boxes[b]:
            end = datetime.strptime(tup[1], "%Y-%m-%d %H:%M:%S.%f").timestamp()
            start = datetime.strptime(tup[0], "%Y-%m-%d %H:%M:%S.%f").timestamp()
            gap = abs(int(end - start))
            res.append(gap)
        box_stay_time[b] = res
    return box_stay_time


if __name__ == '__main__':
    robot_task_event = pd.read_csv(r'data\robot_task_event.csv')
    boxes = get_box_buffer_area_time(robot_task_event)
    stay_time = get_box_stay_time(boxes)
    print(stay_time)
