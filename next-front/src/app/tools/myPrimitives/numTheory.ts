import bigInt from "big-integer";

// 素因数分解を行う
export function getPrimeFactors(num: bigInt.BigInteger): bigInt.BigInteger[] {
    const factors: bigInt.BigInteger[] = [];
    let divisor = bigInt(2);

    while (divisor.multiply(divisor).lesserOrEquals(num)) {
        while (num.mod(divisor).equals(0)) {
            factors.push(divisor);
            num = num.divide(divisor);
        }
        divisor = divisor.next();
    }
    if (num.greater(1)) {
        factors.push(num);
    }
    return Array.from(new Set(factors));
}

// モジュラ逆数を計算する
export function modInverse(num: bigInt.BigInteger, modulo: bigInt.BigInteger): bigInt.BigInteger {
    return num.modInv(modulo); // bigInt の `modInv` を直接利用
}

// モジュラの高速累乗
export function modPow(
    base: bigInt.BigInteger,
    exponent: bigInt.BigInteger,
    modulo: bigInt.BigInteger
): bigInt.BigInteger {
    return base.modPow(exponent, modulo); // bigInt の `modPow` を直接利用
}

// 原始元を探す
export function getPrimitiveRoot(prime: bigInt.BigInteger): bigInt.BigInteger {
    const phi = prime.subtract(1);
    const factors = getPrimeFactors(phi);

    for (let candidate = bigInt(2); candidate.lesser(prime); candidate = candidate.next()) {
        let isPrimitiveRoot = true;

        for (const factor of factors) {
            if (candidate.modPow(phi.divide(factor), prime).equals(1)) {
                isPrimitiveRoot = false;
                break;
            }
        }

        if (isPrimitiveRoot) {
            return candidate;
        }
    }

    throw new Error("No primitive root found.");
}

// 安全な乱数生成
export function getRandomBigInt(max: bigInt.BigInteger): bigInt.BigInteger {
    return bigInt.randBetween(max.divide(bigInt(2)), max);
}