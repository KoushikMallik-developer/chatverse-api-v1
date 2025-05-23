from abc import ABC


class GenericBaseException(ABC, Exception):
    def __init__(self, msg: str):
        if msg:
            self.msg = msg
