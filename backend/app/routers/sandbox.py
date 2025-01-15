from ..components.myAlgs.permutations import *
from ..components.myAlgs.myPrimitives import * 
from ..components.myAlgs.elgamal import *
from ..components.myAlgs.commitment import *
from ..components.myAlgs.hash import *
from ..data.variables import *
import sympy.ntheory.residue_ntheory as resd


param = Parameters()
# param.genParams(4)
# param.setParams(vars512["parameters"])
param.setParams(vars["parameters"])

# while True:
#     h = getRandomElement(param.q)
#     # print(f'{params.q}\n{is_primitive_root(h,params.q)}\n{h!=params.q}\n{h not in res}')
#     if (h != param.g)and (is_primitive_root(h, param.q)):
#         # print()
#         param.h = h
#         break
print(param)
keys = ElgamalKeys()
st_keys = vars["mixKeys"]
# print(st_keys)
keys.setKeys(st_keys)

def test3():
    votes = []
    for i in range(1,5):
        plain = ElgamalPlainText(i*100+i*10+i)
        tmp = ElgamalCipherText()
        tmp.encryption(param, keys, plain)
        votes.append(tmp)

    phai = Permutation()
    phai.genPermutation(len(votes))
    shuffled = phai.cipherPermutation(param, keys, votes)

    dumyplain = ElgamalPlainText(666)
    dumy = ElgamalCipherText()
    dumy.encryption(param, keys, dumyplain)
    dumy.reEncR = 11111
    print(phai.permutation)
    print(phai.matrix)
    # shuffled[len(shuffled)-1] = dumy
    
    sp = ShuffleProof()


    print("votes")
    for item in votes:
        print(item.decryption(param, keys))
    print("shuffle")
    for item in shuffled:
        print(item.decryption(param, keys))
    sp.setVariables(votes, shuffled, phai, keys)
    # print(sp)
    sp.genProof(param)
    # for item in sp.pi:
    #     print(item)
    print(sp.verify(param))

def test2():
    # param.genParams(256)
    # print(param)
    # elgkeys = ElgamalKeys()
    # elgkeys.genKeys(param)
    print(keys)
    plains = [ElgamalPlainText(111), ElgamalPlainText(222), ElgamalPlainText(333)]
    ciphers = [ElgamalCipherText() for _ in range(len(plains))]
    ciphers = [cipher.encryption(param, keys, plain) for cipher, plain in zip(ciphers, plains)]
    print(ciphers)
    for cipher in ciphers:
        print(cipher)
    phai = Permutation()
    phai.genPermutation(len(plains))
    shuffled = phai.cipherPermutation(param, keys, ciphers)
    for item in shuffled:
        print(item.decryption(param, keys))
    

def test1():
    # param.genParams(8)
    # keys.genKeys(param)
    elgKeys = ElgamalKeys()
    elgKeys.genKeys(param)
    print(elgKeys)
 
def main():
    # print(test1())
    # test1()
    test2()
    # test3()

if __name__ == '__main__':
    main()