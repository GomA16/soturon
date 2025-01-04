import random
import sympy
import secrets

import sympy.ntheory
import sympy.ntheory.residue_ntheory

def euclid_remainder(a,b):
    res = []
    while b > 1:
        res.append([a,b,a//b,a%b])
        tmp = b
        b = a % b
        a = tmp
    return res

def modinv(num, p):
    if num < 0:
        num += p
    a = p
    b = num
    euc = euclid_remainder(a,b)
    a_coef = [1,0]
    b_coef = [0,1]
    for i in range(len(euc)):
        tmp = b_coef.copy()
        b_coef[0] = a_coef[0] - euc[i][2]*b_coef[0]
        b_coef[1] = a_coef[1] - euc[i][2]*b_coef[1]
        a_coef = tmp
    res = b_coef[1]
    if res < 0:
        return a + res
    return res


# mod pでの高速冪乗
def modPow(base, index, p):
    res = 1
    binary = str(bin(index)[2:])
    for i in range(len(binary)):
        res = (res * res) % p
        if binary[i] == '1':
            res = (res * base) % p
    return res

# 素因数を得る
def get_prime_fact(num):
    res = []
    if num in sympy.sieve:
        res.append(num)
    if num > 1:
        i = 2
        tale = num
        while i < tale:
            if num % i == 0:
                if i in sympy.sieve:
                    res.append(i)
                if (num // i) in sympy.sieve:
                    res.append(num // i)
            tale = num // i
            i += 1
    res.sort()
    return res

# 原始元かどうかの判定
def is_gen(num, p):
    ls = get_prime_fact(p -1)
    for i in range(len(ls)):
        if modPow(num, (p - 1) // ls[i], p) % p == 1:
            return False
    return True

# 原始元gの取得
def getGenerator(p):
    return sympy.ntheory.residue_ntheory.primitive_root(p, smallest=False)

def getPrimes(bits):
    while True:
        q = sympy.nextprime(secrets.randbits(bits))
        # print(q)
        if sympy.isprime(2*q+1):
            return(2*q+1, q)

def getRandomElement(q):   
    return q // 2 + secrets.randbelow(q  - (q//2) - 1)