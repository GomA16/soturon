from .myPrimitives import *
from .parameters import Parameters
from typing import Self
from sympy.ntheory.residue_ntheory import is_primitive_root

class Pedersen():
    def __init__(self):
        self.messages: list[int] = None
        self.hs: list[int] = None
        self.matrix: list[list[int]] = None
        self.r: int = None
        self.commitment: int = None
        self.matCommitment: list[Pedersen] = None

    def setMessages(self, messages: list[int]) -> Self :
        self.messages = messages
        return self

    def setMatrix(self, mat: list[list[int]]) -> Self:
        self.matrix = mat
        return self
    
    def getHs(self, params: Parameters, length: int) -> list[int]:
        res = []
        for _ in range(length):
            while True:
                h = getRandomElement(params.q)
                # print(f'{params.q}\n{is_primitive_root(h,params.q)}\n{h!=params.q}\n{h not in res}')
                if (h != params.g) and ((h not in res )and (is_primitive_root(h, params.q))):
                    # print()
                    res.append(h)
                    break
        # print(res)
        return res


    def commit(self, params: Parameters) -> Self:
        self.hs = self.getHs(params, len(self.messages))
        self.r = getRandomElement(params.q)
        self.commitment = modPow(params.g, self.r, params.q)
        for h,m in zip(self.hs, self.messages):
            self.commitment = (self.commitment * modPow(h, m, params.q)) % params.q
        return self
    
    def commitMat(self, params: Parameters) -> Self:
        self.matCommitment = []
        for i in range(len(self.matrix)):
            column = [row[i] for row in self.matrix]
            child = Pedersen()
            child.setMessages(column)
            child.commit(params)
            self.matCommitment.append(child)
        return self 
    

    
