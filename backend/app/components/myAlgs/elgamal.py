from .myPrimitives import modPow, modinv, getPrimes, getGenerator, getRandomElement
from typing import Self

def stringToInt(str):
    return int.from_bytes(str.encode('utf-8'), byteorder='big')

def intToString(num):
    return (num.to_bytes((num.bit_length() + 7) // 8, byteorder='big')).decode('utf-8')

class Parameters():
    def __init__(self):
        self.p = None
        self.q = None
        self.g = None
        
    def genParams(self, bits: int) -> Self:
        self.p,self.q = getPrimes(bits)
        self.g = getGenerator(self.p)
        return self
    
    def setParams(self, dict: dict) -> Self:
        self.p = int(dict["p"])
        self.q = int(dict["q"])
        self.g = int(dict["g"])
        return self
    
    def __str__(self):
        return f'p: {self.p}\nq: {self.q}\ng: {self.g}'
    

class ElgamalKeys():
    def __init__(self):
        self.publicKey = None
        self.secretKey = None

    def genKeys(self, params: Parameters) -> None:
        self.secretKey = getRandomElement(params.q)
        self.publicKey = modPow(params.g, self.secretKey, params.q)

    def setKeys(self, keys: dict) -> None:
        self.publicKey = int(keys["pk"])
        self.secretKey = int(keys["sk"])

    def __str__(self):
        return f'pk: {self.publicKey}\nsk: {self.secretKey}'
    
    
class ElgamalPlainText():
    def __init__(self, message):
        self.plainText = message
    
    def __str__(self):
        return f'ptxt:{self.plainText}'
    

class ElgamalCipherText():
    def __init__(self):
        self.cipherText = None #(c1,c2) = (g^r, m*g^rx)

    def setCipher(self, cipher: list[str]) -> Self:
        self.cipherText = [int(c) for c in cipher]
        return self
    
    def encryption(self, params:Parameters, keys: ElgamalKeys, plainText:ElgamalPlainText) -> Self:
        r = getRandomElement(params.q)
        self.cipherText = (modPow(params.g, r, params.q), (plainText.plainText*modPow(keys.publicKey, r, params.q)) % params.q)
        return self

    def decryption(self, params: Parameters, keys: ElgamalKeys) -> ElgamalPlainText:
        return ElgamalPlainText(self.cipherText[1] * modinv(modPow(self.cipherText[0], keys.secretKey, params.q), params.q )%params.q)
    
    def reEncryption(self, params: Parameters, keys: ElgamalKeys) -> Self:
        r = getRandomElement(params.q)
        self.cipherText = ((self.cipherText[0]*modPow(params.g, r, params.q)) % params.q, (self.cipherText[1]* modPow(keys.publicKey, r, params.q)) % params.q)
        return self
    
    def __str__(self):
        return f'ctxt:{self.cipherText}'
    
