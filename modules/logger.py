import os
import zlib
import uuid
import logging
from logging import handlers


def rotator(source, dest):
    with open(source, "rb") as sf:
        data = sf.read()
        compressed = zlib.compress(data, 9)
        with open(dest, "wb") as df:
            df.write(compressed)
    os.remove(source)


class ContextFilter(logging.Filter):
    def __init__(self):
        self.uuid = uuid.uuid4()

    def update_uuid(self):
        self.uuid = uuid.uuid4()

    def filter(self, record):
        record.uuid = self.uuid
        return True


context = ContextFilter()


def create_file_handler(log_filename):
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(uuid)s] %(message)s')
    handler = handlers.TimedRotatingFileHandler(log_filename, 'midnight', 1, backupCount=90)
    handler.setLevel(logging.DEBUG)
    handler.addFilter(context)
    handler.setFormatter(formatter)
    handler.rotator = rotator
    return handler
