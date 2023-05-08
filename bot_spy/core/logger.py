import logging
from sys import stdout

logger = logging.getLogger('wb_spy_bot')
logger.propagate = False
logger.setLevel(logging.DEBUG)
log_handler = logging.StreamHandler(stdout)
log_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '[%(levelname)s] %(asctime)s %(name)s: %(message)s')
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)
logger.disabled = False
