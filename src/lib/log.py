import logging
import logging.handlers

import src.lib.base as base
from src.lib.fmanager import FileFolderManager

f = FileFolderManager()


class Streamer(logging.StreamHandler):
    def emit(self, record):
        if base.ws['client'] is not None:
            msg = self.format(record)
            server = base.ws['server']
            client = base.ws['client']
            server.send_message_to_all(msg)


def setup_logger(logger_name, log_file, rotate=False, stream=True):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p')

    if rotate:
        file_handler = logging.handlers.RotatingFileHandler(
            '.\logs\\' + log_file, mode='w', maxBytes=1*1024*1024, backupCount=3)
    else:
        file_handler = logging.FileHandler('%s\%s\%s' % (f.workingdir, f.logfolder, log_file), 'w')

    file_handler.setFormatter(formatter)

    level = getattr(logging, base.config['log_level'])
    l.setLevel(level)
    l.addHandler(file_handler)

    if stream:
        formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        l.addHandler(stream_handler)

    streamer = None
    if streamer is None:
        streamer = Streamer()
    streamer.setFormatter(formatter)
    l.addHandler(streamer)
