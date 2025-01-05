from Crypto.Hash import SHA256
from .parameters import Parameters
from .elgamal import ElgamalCipherText
from .commitment import Pedersen
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
    
    def recHash(self, value: list[int]|int) -> bytes:
        # print(len(value))
        t = type(value)
        if t == int:
            self.h = self.myHash(value)
            return self.h
        elif t == ElgamalCipherText:
            return self.recHash(value.cipherText)
        elif t == Pedersen:
            return self.recHash(value.cipherText)
        elif len(value) == 1:
            if type(value) == int:
                return self.myHash(value[0])
            if type(value) == list:
                 return self.recHash(value[0])
        elif len(value) > 1:
            res = self.recHash(value[0])
            for i in range(1,len(value)):
                res = b''.join([res,self.recHash(value[i])])
            self.h = res
            return res
        
    def toInt(self, params: Parameters) -> Self:
        if type(self.h) == bytes:
            self.h = int.from_bytes(self.h, byteorder='big') % params.q
        return self