"""
自定义异常类
"""


class DatabaseInsertException(Exception):
    def __init__(self, info):
        super().__init__(info)
        self.info = info

    def __str__(self):
        return self.info
