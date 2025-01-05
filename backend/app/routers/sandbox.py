from ..components.myAlgs.permutations import *
from ..components.myAlgs.myPrimitives import * 
from ..components.myAlgs.elgamal import *
from ..components.myAlgs.commitment import *
from ..components.myAlgs.hash import *
from ..data.variables import *
import sympy.ntheory.residue_ntheory as resd


param = Parameters()
# param.genParams(512)
param.setParams(vars512["parameters"])

while True:
    h = getRandomElement(param.q)
    # print(f'{params.q}\n{is_primitive_root(h,params.q)}\n{h!=params.q}\n{h not in res}')
    if (h != param.g)and (is_primitive_root(h, param.q)):
        # print()
        param.h = h
        break
print(param)

def test3():
    keys = ElgamalKeys()
    st_keys = vars512["keys"]
    # print(st_keys)
    keys.setKeys(st_keys)
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
    
    sp = ShuffleProof()
    # shuffled[len(shuffled)-1] = dumy
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
    mes = [[1,0,0],
           [0,1,0],
           [0,0,1]]
    com = Pedersen()
    com.setMatrix(mes)
    com.commitMat(param)
    for item in com.matCommitment:
        print(item.commitment)

def test1():
    hash = Hash()
 
def main():
    # print(test1())
    # test1()
    test3()

if __name__ == '__main__':
    main()