import secrets
from .elgamal import *
from .parameters import *
from .commitment import *
from .hash import *

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


class ShuffleProof():
    def __init__(self):
        self.votes: list[ElgamalCipherText] = None
        self.shuffled_votes: list[ElgamalCipherText] = None
        self.reEncRs: list[int] = None
        self.phai: Permutation = None
        self.pk: int = None
        self.pi: int = None

    def setVariables(self, votes: list[ElgamalCipherText], shuffled_votes: list[ElgamalCipherText], 
                 phai: Permutation, keys: ElgamalKeys):
        self.votes = votes
        self.shuffled_votes = shuffled_votes
        self.phai = phai
        self.pk = keys.publicKey
        self.reEncRs = [c.reEncR for c in shuffled_votes]

    def setProof(self, pi:int) -> Self:
        self.pi = pi
        return self

    def getChallenges(self, params: Parameters,num: int,vec: list[int]) -> list[int]:
        res = []
        hash = Hash()
        hash.recHash(vec)
        for i in range(1,num+1):
            ihash = Hash()
            ihash.recHash(i)
            chash = Hash()
            chash.recHash([hash.h, ihash.h])
            # print(type(chash.h))
            chash.toInt(params)
            res.append(chash.h)
        return res
        
    def genCommitmentChain(self, params:Parameters ,vec):
        r_hat = 0
        u_childas = 1
        c_hats_prime = [params.h]
        r_hats = []
        for item in vec:
            r_hat_i = getRandomElement(params.q)
            r_hats.append(r_hat_i)
            r_hat = (r_hat_i  + (item * r_hat) % params.q) % params.q
            u_childas = (item * u_childas) % params.p
            c_hats_prime.append((modPow(params.g, r_hat, params.p) * modPow(params.h, u_childas, params.p)) % params.p)
        return [c_hats_prime, r_hats]
        

    def genProof(self, params: Parameters) -> Self:
        com = Pedersen()
        com.setMatrix(self.phai.matrix)
        com.commitMat(params)

        num = len(self.votes)
        vec = []
        for item in self.votes:
            vec.append(item)
        for item in self.shuffled_votes:
            vec.append(item)
        for item in com.matCommitment:
            vec.append(item.commitment)
        us = self.getChallenges(params, num, vec)

        u_childas = self.phai.doPermutation(us)

        com_prime = self.genCommitmentChain(params,u_childas)

        w1 = getRandomElement(params.q)
        w2 = getRandomElement(params.q)
        w3 = getRandomElement(params.q)
        w4 = getRandomElement(params.q)

        w_hats = []
        w_childas = []
        for _ in range(len(self.votes)):
            tmp = getRandomElement(params.q)
            w_hats.append(tmp)
            tmp = getRandomElement(params.q)
            w_childas.append(tmp)

        t1 = modPow(params.g, w1, params.p)
        t2 = modPow(params.g, w2, params.p)
        t3 = modPow(params.g, w3, params.p)
        t41 = modPow(self.pk, modinv(w4, params.p), params.p)
        t42 = modPow(params.g, modinv(w4, params.p), params.p)
        for w_childa, cipher in zip(w_childas, self.shuffled_votes):
            t41 = (t41 * modPow(cipher.cipherText[1], w_childa, params.p)) % params.p
            t42 = (t42 * modPow(cipher.cipherText[0], w_childa, params.p)) % params.p

        t_hats = []
        for i in range(len(self.votes)):
            t_hats.append((modPow(params.g, w_hats[i], params.p) * modPow(com_prime[0][i], w_hats[i], params.p)) % params.p)
        
        t = [t1, t2, t3, [t41, t42], t_hats]

        y = [self.votes, self.shuffled_votes, [c.commitment for c in com.matCommitment], com_prime[0], self.pk]

        c = self.getChallenges(params, 1, [y, t])[0]

        r_bar = 0
        for comi in com.matCommitment: 
            r_bar = (r_bar + comi.r) %params.q
        s1 = (w1 - (c * r_bar) % params.q) % params.q

        n = len(self.votes)
        vs = [0 for _ in range(n)]
        if len(self.votes) != 0:
            vs[n-1] = 1
            for i in range(n-2, 0, -1):
                vs[i] = (u_childas[i+1] * vs[i+1]) % params.q

        r_hat = 0
        for ri, v in zip(com_prime, vs):
            r_hat = (r_hat + (ri[1] * v) % params.q) % params.q
        s2 = (w2 - (c * r_hat)%params.q) % params.q

        r = 0
        for ri, ui in zip(com.matCommitment, us):
            r = (r + (ri.r * ui) % params.q) % params.q
        s3 = (w3 - (c * r)%params.q) % params.q

        r_childa = 0
        for ri, ui in zip(self.reEncRs, us):
            r_childa = (r_childa + (ri * ui) % params.q) % params.q
        s4 = (w4 - (c * r_childa)%params.q) % params.q

        s_hats = []
        s_childas = []
        for i in range(n):
            s_hats.append((w_hats[i] - (c * com_prime[1][i])%params.q)%params.q)
            s_childas.append((w_childas[i] - (c * u_childas[i])%params.q)%params.q)
        
        s = [s1, s2, s3, s4, s_hats, s_childas]
        self.pi = [c,s,[c_vec.commitment for c_vec in com.matCommitment], [item[0] for item in com_prime]]
        return self
    
    # def verify(self) -> bool:

    def __str__(self):
        return f'{self.votes}\n{self.shuffled_votes}\n{self.reEncRs}\n{self.phai}\n{self.pi}\n{self.pk}'