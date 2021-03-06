import datetime as dt

INFO = "info"
ERROR = "error"
DEBUG = "debug"


class log:

    def __init__(self, *str):
        self.level = INFO
        self.__logPy = str

    def error(self, *str):
        if self.level == ERROR:
            self.__print(ERROR, str)

    def info(self, *str):
        if self.level == INFO:
            self.__print(INFO, str)

    def debug(self, *str):
        if self.level == DEBUG:
            self.__print(DEBUG, str)

    def __print(self, level, *str):
        now = dt.datetime.now()
        timeStr = now.strftime("%Y-%m-%d %X")
        # when level from which py
        print(timeStr, "[", level, "][", self.__logPy, "]:", str)
