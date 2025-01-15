from .myPrimitives import modPow, modinv, getPrimes, getGenerator, getRandomElement
from .parameters import *
from typing import Self

def stringToInt(str):
    return int.from_bytes(str.encode('utf-8'), byteorder='big')

def intToString(num: int):
    return (num.to_bytes((num.bit_length() + 7) // 8, byteorder='big')).decode('utf-8')
    

class ElgamalKeys():
    def __init__(self):
        self.publicKey = None
        self.secretKey = None

    def genKeys(self, params: Parameters) -> Self:
        self.secretKey = getRandomElement(params.p)
        self.publicKey = modPow(params.g, self.secretKey, params.p)
        return self

    def setKeys(self, keys: dict) -> Self:
        self.publicKey = int(keys["pk"])
        self.secretKey = int(keys["sk"])
        return self

    def __str__(self):
        return f'pk: {self.publicKey}\nsk: {self.secretKey}'
    
    
class ElgamalPlainText():
    def __init__(self, message: int):
        self.plainText:int = message
    
    def __str__(self):
        return f'ptxt:{self.plainText}'
    

class ElgamalCipherText():
    def __init__(self):
        self.cipherText: list[int] = None #(c1,c2) = (g^r, m*g^rx)
        self.reEncR: int  = None

    def setCipher(self, cipher: list[str]) -> Self:
        self.cipherText = [int(c) for c in cipher]
        return self
    
    def encryption(self, params:Parameters, keys: ElgamalKeys, plainText:ElgamalPlainText) -> Self:
        r = getRandomElement(params.p)
        self.cipherText = (modPow(params.g, r, params.p), (plainText.plainText*modPow(keys.publicKey, r, params.p)) % params.p)
        return self

    def decryption(self, params: Parameters, keys: ElgamalKeys) -> ElgamalPlainText:
        return ElgamalPlainText(self.cipherText[1] * modinv(modPow(self.cipherText[0], keys.secretKey, params.p), params.p )%params.p)
    
    def reEncryption(self, params: Parameters, keys: ElgamalKeys) -> Self:
        r = getRandomElement(params.p)
        self.reEncR = r
        self.cipherText = ((self.cipherText[0]*modPow(params.g, r, params.p)) % params.p, (self.cipherText[1]* modPow(keys.publicKey, r, params.p)) % params.p)
        return self
    
    def __str__(self):
        return f'ctxt:{self.cipherText}'
    
