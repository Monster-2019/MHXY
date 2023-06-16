import logging
from multiprocessing import current_process
from logging.handlers import QueueHandler
from time import sleep
from worker1 import MyClass

class MyLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        # print(1, msg, kwargs, self.extra)
        kwargs["extra"] = {"id": self.extra.get("id")}
        return msg, kwargs

def task(queue, id):
    # create a logger
    logger = logging.getLogger('app')
    # add a handler that uses the shared queue
    logger.addHandler(QueueHandler(queue))
    # log all messages, debug and up
    logger.setLevel(logging.DEBUG)
    # get the current process
    process = current_process()
    logger = MyLoggerAdapter(logger, {"id": id})
    # report initial message
    logger.info(f'Child {process.name} starting.')
    # simulate doing work
    # for i in range(2):
    #     # report a message
    #     logger.debug(f'Child {process.name} step {i}.')
    #     # block
    #     sleep(0.5)
    MyClass(logger).start()
    # report final message
    logger.info(f'Child {process.name} done.')