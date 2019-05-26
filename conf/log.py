import logging, sys, os
import logging.handlers

logging.basicConfig()
server_logger = logging.getLogger("server.6vdata")
server_logger.setLevel(level=logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
filehandler = logging.handlers.TimedRotatingFileHandler(
    os.path.join(os.path.dirname(__file__), '..', "log","log.txt"),
    when='D', interval=1, backupCount=30)
filehandler.suffix = "%Y-%m-%d_%H-%M-%S.log"
filehandler.setFormatter(formatter)
server_logger.addHandler(filehandler)


if __name__ == "__main__":
    server_logger.debug("debug ..")
    server_logger.info("info")
    server_logger.warning("warning")
    print(1/0)
