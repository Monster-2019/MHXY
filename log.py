from loguru import logger

logger.add('run.log', rotation="1 week", encoding="utf-8", retention="7 days", backtrace=True, catch=True, enqueue=True)

def log(msg, err = False):
    if err:
        logger.error(msg)
    else:
        logger.info(msg)
