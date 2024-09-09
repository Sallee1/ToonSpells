import customExceptions

# 定义一些自定义的异常，用于提示错误消息


class bl_Operator_Error(Exception):
    def __init__(self, message):
        self.message = message
