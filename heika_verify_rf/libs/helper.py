import inspect
from datetime import datetime


def log(content):
    caller = inspect.getframeinfo(inspect.currentframe().f_back)[2]
    print "[%s] [%s] %s" % (str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), caller, content)


def log_error(content):
    caller = inspect.getframeinfo(inspect.currentframe().f_back)[2]
    print "[***ERROR***][%s] [%s] %s" % (str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), caller, content)
