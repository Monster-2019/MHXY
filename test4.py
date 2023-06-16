import logging
from multiprocessing import current_process
from logging.handlers import QueueHandler
from multiprocessing import Queue

# 创建共享队列
queue = Queue()

# 自定义日志记录对象
class CustomLogRecord(logging.LogRecord):
    def __init__(self, *args, **kwargs):
        self.process_name = kwargs.pop('process_name', None)
        super().__init__(*args, **kwargs)

# 创建日志记录器
logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)

# 创建使用共享队列的处理程序
queue_handler = QueueHandler(queue)
logger.addHandler(queue_handler)

# 设置日志记录器的格式化器
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - [%(process_name)s] - %(message)s')
queue_handler.setFormatter(formatter)

# 添加进程信息到LoggerAdapter
logger_adapter = logging.LoggerAdapter(logger, {'process_name': current_process().name})

# 向队列发送日志消息
logger_adapter.info('This is a log message')

# 从队列中获取日志消息
message = queue.get()
log_record = message.msg
process_name = log_record.process_name  # 从LogRecord中获取进程信息

print(process_name)  # 输出当前进程的名称
