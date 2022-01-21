from enum import Enum

'''
author:zhangyu
description:推理返回状态
date:2020.1.21
'''


class InferStatus(Enum):
    '''
        推理状态
    '''
    SUCCEED = 0
    TIMEOUT = 1


class InferResponse:
    def __init__(self, status: InferStatus, result) -> None:
        """
            推理返回结果
        Args:
            status: 状态
            result: 结果
        """
        self.status = status
        self.result = result

    def succeed(self):
        '''
            状态码返回信息
        Returns:
            布尔值
        '''
        return self.status == InferStatus.SUCCEED
