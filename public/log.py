# import logging
# import datetime
# import os
# today = datetime.date.today()
# logger = logging.getLogger(__name__)
# logger.setLevel(level = logging.INFO)
# handler = logging.FileHandler(str(today) + '.txt')
# handler.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s - %(message)s')
# handler.setFormatter(formatter)

# console = logging.StreamHandler()
# console.setLevel(logging.INFO)

# logger.addHandler(handler)
# logger.addHandler(console)

# def log(msg, err = False):
#     if err:
#         logger.warning(msg)
#     else:
#         logger.info(msg)

# def clearFile():
#     file = open(str(today) + '.txt', 'w')
#     file.truncate()

from loguru import logger

logger.add("logger.log", format="{time} | {level} | {message}", enqueue=True)

def log(msg, err = False):
    if err:
        logger.error(msg)
    else:
        logger.info(msg)
