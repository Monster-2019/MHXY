# SuperFastPython.com
# example of logging from multiple processes in a process-safe manner
from multiprocessing import Process
from multiprocessing import Queue
import logging
from worker import task
 
# executed in a process that performs logging
def logger_process(queue):
    # create a logger
    logger = logging.getLogger('app')
    # configure a stream handler
    logger.addHandler(logging.StreamHandler())
    # log all messages, debug and up
    logger.setLevel(logging.DEBUG)
    # run forever
    while True:
        message = queue.get()
        if message is None:
            break
        # print(2, message, )
        # if "id" in message.__dict__:
        msg = message.msg
        print("id", message.id, msg)
        # logger.handle(message)

# protect the entry point
if __name__ == '__main__':
    # create the shared queue
    queue = Queue()
    # create a logger
    logger = logging.getLogger('app')
    # add a handler that uses the shared queue
    # logger.addHandler(QueueHandler(queue))
    # log all messages, debug and up
    logger.setLevel(logging.DEBUG)
    # start the logger process
    logger_p = Process(target=logger_process, args=(queue,))
    logger_p.start()
    # report initial message
    logger.info('Main process started.')
    # configure child processes
    processes = [Process(target=task, args=(queue, i)) for i in range(2)]
    # start child processes
    for process in processes:
        process.start()
    # wait for child processes to finish
    for process in processes:
        process.join()
    # report final message
    logger.info('Main process done.')
    # shutdown the queue correctly
    queue.put(None)