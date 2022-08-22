import logging.config
import logging

logging.config.fileConfig("log.ini")
logger = logging.getLogger('fileLogger')
