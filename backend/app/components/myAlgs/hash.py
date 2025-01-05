from Crypto.Hash import SHA256
from .parameters import Parameters
from typing import Self

class Hash():
    def __init__(self):
        self.h: bytes|int = None

    def myHash(self,value: int | bytes) -> bytes:
        res = b''
        if type(value) == int:
            sha = SHA256.new((str(value)).encode())
            res = sha.digest()
        if type(value) == bytes:
            sha = SHA256.new(value)
            res = sha.digest()
        return res
    
    def recHash(self, value: list[int]|int) -> Self:
        # print(len(value))
        if type(value) == int:
            self.h = self.myHash(value)
            return self
        if len(value) == 1:
            if type(value) == int:
                self.h = self.myHash(value[0])
            if type(value) == list:
                self.h = self.recHash(value[0])
            return self
        if len(value) > 1:
            res = self.myHash(value[0])
            for i in range(1,len(value)):
                res = b''.join([res,self.myHash(value[i])])
            self.h = res
            return self
        
    def toInt(self, params: Parameters) -> Self:
        if type(self.h) == bytes:
            self.h = int.from_bytes(self.h, byteorder='big') % params.q
        return self