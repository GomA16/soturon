from .myPrimitives import * 
from sympy.ntheory.residue_ntheory import is_primitive_root
from typing import Self

class Parameters():
    def __init__(self):
        self.p = None
        self.q = None
        self.g = None
        self.h = None
        
    def genParams(self, bits: int) -> Self:
        self.p,self.q = getPrimes(bits)
        self.g = getGenerator(self.q)
        while True:
            self.g = getGenerator(self.q)
            if is_primitive_root(self.g, self.p):
                break
        print("done")
        while True:
            h = getRandomElement(self.q)
            # print(f'{params.q}\n{is_primitive_root(h,params.q)}\n{h!=params.q}\n{h not in res}')
            if (h != self.g)and (is_primitive_root(h, self.q)):
                # print()
                self.h = h
                break
        return self
    
    def setParams(self, dict: dict) -> Self:
        self.p = int(dict["p"])
        self.q = int(dict["q"])
        self.g = int(dict["g"])
        return self
    
    def __str__(self):
        return f'p: {self.p}\nq: {self.q}\ng: {self.g}\nh:{self.h}'