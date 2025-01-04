import secrets
from .elgamal import *

class Permutation():
    def __init__(self):
        self.permutation = None
        self.matrix = None

    def genPermutation(self, n: int) -> None:
        array = list(range(n))
        res = list(range(n))
        for i in range(n):
            k = i + secrets.randbelow(n-i)
            res[i] = array[k]
            array[k] = array[i]
        self.permutation = res
        self.matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            self.matrix[array[i]][res[i]] = 1

    def doPermutation(self, data: list[int]) -> list[int]:
        res= [0 for _ in range(len(data))]
        for i in range(len(data)):
            res[i] = data[self.permutation[i]]
        return res
    
    def cipherPermutation(self, params: Parameters, keys: ElgamalKeys,ciphers: list[ElgamalCipherText]) -> list[ElgamalCipherText]:
        res= [ElgamalCipherText() for _ in range(len(ciphers))]
        for i in range(len(ciphers)):
            res[i] = ciphers[self.permutation[i]].reEncryption(params, keys)
        return res