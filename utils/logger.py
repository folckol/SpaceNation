import os
import time
from sys import stderr

from loguru import logger

logger.remove()
logger.add(stderr, format='<white>{time:HH:mm:ss}</white>'
                          ' | <level>{level: <8}</level>'
                          ' | <white>{message}</white>')

logger.add("LogsBackUp/logs.log", format='<white>{time:HH:mm:ss}</white>'
                                   ' | <level>{level: <8}</level>'
                                   ' -| <white>{message}</white>')


class MultiThreadLogger:

    def __init__(self, thread_number):

        self.thread_number = thread_number

        folder_path = f'{os.getcwd()}/Logs2'
        if not os.path.exists(folder_path):
            try:
                os.makedirs(folder_path)

            except OSError as e:
                ...
        else:
            ...

        self.file_path = f'{os.getcwd()}/Logs2/logs{thread_number}.txt'
        if not os.path.exists(folder_path):
            try:
                with open(self.file_path, 'w', encoding='utf-8') as file:
                    file.write('')

            except OSError as e:
                ...
        else:
            ...


    def success(self, msg):
        with open(self.file_path, 'a+', encoding='utf-8') as file:
            file.write('{} | {} | {}\n'.format(time.strftime("%H:%M:%S"), 'SUCCESS'.ljust(8), msg))

    def error(self, msg):
        with open(self.file_path, 'a+', encoding='utf-8') as file:
            file.write('{} | {} | {}\n'.format(time.strftime("%H:%M:%S"), 'ERROR'.ljust(8), msg))

    def info(self, msg):
        with open(self.file_path, 'a+', encoding='utf-8') as file:
            file.write('{} | {} | {}\n'.format(time.strftime("%H:%M:%S"), 'INFO'.ljust(8), msg))

    def warning(self, msg):
        with open(self.file_path, 'a+', encoding='utf-8') as file:
            file.write('{} | {} | {}\n'.format(time.strftime("%H:%M:%S"), 'WARNING'.ljust(8), msg))

    def skip(self):
        with open(self.file_path, 'a+', encoding='utf-8') as file:
            file.write('\n')




