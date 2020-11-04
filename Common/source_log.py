import logging
from logging.handlers import TimedRotatingFileHandler
import concurrent_log_handler
import random


class MyLogger(object):
    # 封装日志模块
    def __init__(self, logger=None):
        num = ''
        i = 0
        while i < 10:
            num_str = random.choice('abcdefghi_jklmnopqishuvwxyz')
            num += num_str
            i += 1
            logger = num
        self.my_logger = logging.getLogger(logger)
        print('logger', logger)

    def create_logger(self):
        self.my_logger.setLevel('INFO')

        # 控制台处理器
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel('INFO')
        self.my_logger.addHandler(stream_handler)

        # 基于时间滚动的处理器
        file_log_handler = TimedRotatingFileHandler(r'../Log/mylogfile.log', when='M', interval=1, backupCount=10)
        file_log_handler.setLevel('INFO')
        self.my_logger.addHandler(file_log_handler)

        # rotateHandler = concurrent_log_handler.ConcurrentRotatingFileHandler('../Log/mylogfile.log','a', 512 * 1024, 5)
        # my_logger.addHandler(rotateHandler)
        # my_logger.setLevel(logging.INFO)

        # 设置日志格式
        formatter = logging.Formatter('%(asctime)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s')
        stream_handler.setFormatter(formatter)
        file_log_handler.setFormatter(formatter)
        # rotateHandler.setFormatter(formatter)

        return self.my_logger


if __name__ == '__main__':
    log = MyLogger().create_logger()
    log.info("test-info")
    log.error("test-error")
