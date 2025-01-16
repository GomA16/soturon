import bigInt, { BigInteger } from "big-integer";
// import { bigint, quotelessJson } from "zod";
import {getRandomBigInt, modPow, modInverse} from "./numTheory";

export function stringToBigInt(str: string): BigInteger {
    const encoder = new TextEncoder();
    const encoded = encoder.encode(str); // UTF-8でエンコード
    let result = bigInt(0);
    for (const byte of encoded) {
        result = (result.shiftLeft(bigInt(8))).add(bigInt(byte)); // 8ビットずつシフトして加算
    }
    return result;
}

// BigInt を string に変換
export function bigIntToString(num: BigInteger): string {
    const bytes: number[] = [];
    const mask = bigInt(0xFF);
    while (num.greater(bigInt(0))) {
        bytes.unshift(Number(num.and(mask)));// 下位8ビットを取得
        num = num.shiftRight(bigInt(8)); // 8ビットシフト
    }
    const decoder = new TextDecoder();
    return decoder.decode(new Uint8Array(bytes)); // UTF-8でデコード
}

export class Parameters {
    public p: BigInteger;
    public q: BigInteger;
    public g: BigInteger;
    
    constructor() {
        this.p = bigInt(0);
        this.q = bigInt(0);
        this.g = bigInt(0);
    }

    public setParams({p,q,g}:{
        p: string;
        q: string;
        g: string;
    }) {
        this.p = bigInt(p);
        this.q = bigInt(q);
        this.g = bigInt(g);
    }
}

export class ElgamalKeys {
    public secretKey: BigInteger;
    public publicKey: BigInteger;

    constructor() {
        this.secretKey = bigInt(0);
        this.publicKey = bigInt(0);
    }

    public setKeys({pk, sk}:{pk: string, sk: string}) {
        this.secretKey = bigInt(sk);
        this.publicKey = bigInt(pk);
    }
}

export class ElgamalPlainText {
    public ptxt: BigInteger;

    constructor(message: BigInteger) {
        this.ptxt = message
    }
}

export class ElgamalCipherText {
    public ctxt: BigInteger[];

    constructor(){
        this.ctxt = [bigInt(0), bigInt(0)];
    }

    public encryption(params: Parameters, keys: ElgamalKeys, ptxt: ElgamalPlainText): ElgamalCipherText {
        const r = getRandomBigInt(params.p)
        this.ctxt = [modPow(params.g, r,params.p), (ptxt.ptxt.multiply(modPow(keys.publicKey, r, params.p))).mod(params.p)]
        return this
    }

    public decryption(params: Parameters, keys: ElgamalKeys): ElgamalPlainText {
        // return ElgamalPlainText(self.cipherText[1] * modinv(modPow(self.cipherText[0], keys.secretKey, params.p), params.p )%params.p)
        return new ElgamalPlainText((this.ctxt[1].multiply(modInverse(modPow(this.ctxt[0], keys.secretKey, params.p),params.p))).mod(params.p))
    }
}