import logging, sys, os
import logging.handlers

server_logger = logging.getLogger("server.6vdata")

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(level=logging.DEBUG)
server_logger.addHandler(stream_handler)

file_handler = logging.handlers.TimedRotatingFileHandler(
    os.path.join(os.path.dirname(__file__), '..', "log","log.txt"),
    when='D',
    interval=1,
    backupCount=30)
file_handler.setLevel(level=logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
server_logger.addHandler(file_handler)