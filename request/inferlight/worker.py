import logging
import multiprocessing as mp
import time
from queue import Empty

'''
author:zhangyu
description: 1)读数据将数据放入到队列中
             2）批量的进行推理
             3）一次性批量将结果放入到队列中
date:2020.1.21
'''


class BaseInferLightWorker:

    def __init__(self, data_queue: mp.Queue, result_queue: mp.Queue,
                 model_args: dict,
                 batch_size=16, max_delay=0.1,
                 ready_event=None) -> None:
        self.data_queue = data_queue
        self.result_queue = result_queue
        self.batch_size = batch_size
        self.max_delay = max_delay
        self.logger = logging.getLogger('InferLight-Worker')
        self.logger.setLevel(logging.DEBUG)

        self.load_model(model_args)

        if ready_event:
            ready_event.set()

    def run(self):
        self.logger.info('Worker started!')
        while True:
            data, task_ids = [], []
            since = time.time()
            for i in range(self.batch_size):
                try:
                    d = self.data_queue.get(block=True, timeout=self.max_delay)
                    task_ids.append(d[0])
                    data.append(d[1])
                    self.logger.info('get one new task')
                except Empty:
                    pass
                if time.time() - since >= self.max_delay:
                    break
            if len(data) > 0:
                start = time.perf_counter()
                batch = self.build_batch(data)
                results = self.inference(batch)
                end = time.perf_counter()
                time_elapsed = (end - start) * 1000
                self.logger.info(f'inference succeeded. batch size: {len(data)}, time elapsed: {time_elapsed:.3f} ms')
                for (task_id, result) in zip(task_ids, results):
                    self.result_queue.put((task_id, result))

    def build_batch(self, requests):
        raise NotImplementedError

    def inference(self, batch):
        raise NotImplementedError

    def load_model(self, model_args):
        raise NotImplementedError

    @classmethod
    def start(cls, data_queue: mp.Queue, result_queue: mp.Queue, model_args: dict, batch_size=16, max_delay=0.1,
              ready_event=None):
        w = cls(data_queue, result_queue, model_args, batch_size, max_delay, ready_event)
        w.run()
