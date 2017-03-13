import logging
import logging.handlers

log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)

handler = logging.handlers.SysLogHandler(address = ('localhost',514), facility=logging.handlers.SysLogHandler.LOG_LOCAL1)

formatter = logging.Formatter('%(module)s.%(funcName)s: %(message)s')
handler.setFormatter(formatter)

log.addHandler(handler)


def hello():
    log.debug('this is debug')
    log.critical('this is critical')

if __name__ == '__main__':
    hello()
