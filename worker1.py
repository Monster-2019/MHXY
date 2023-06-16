from time import sleep

class MyClass(object):
    def __init__(self, logger):
        self.logger = logger

    def start(self):
        for i in range(10):
            self.logger.info(i)
            sleep(1)