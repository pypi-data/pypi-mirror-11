import logging

RECV_SIZE = 1024
ENC = "json"
OK = None

log_format = "[%(mode)s] %(message)s"
logging.basicConfig(format=log_format)
logger = logging.getLogger(__name__)
