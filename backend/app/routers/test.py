from fastapi import APIRouter, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from databases import Database
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, insert, select
from pydantic import BaseModel
from ..models.election_tables import people, electoral_roll, candidate_list, bulletin_board
from ..core.database import database
from ..helios_crypto import algs
from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
import base64
import traceback
from ..components.myAlgs.elgamal import *
from ..components.myAlgs.permutations import *
from ..data.variables import *

router = APIRouter()

params = Parameters()
params.setParams(vars["parameters"])
keys = ElgamalKeys()
keys.setKeys(vars["tallyKeys"])

class Data(BaseModel):
    message: str
    private_key_pem: str
    public_key_pem: str
    enc_signature: str

@router.post("/sign")
async def test(data: Data):
    try:
        print(base64.b64decode(data.message))
        hash_value = SHA256.new((data.message.encode('utf-8')))
        # print("hash done")

        private_key = ECC.import_key(data.private_key_pem, curve_name='prime256v1')
        generated_signature = DSS.new(private_key, "fips-186-3").sign(hash_value)
        # print(f"Generated signature (hex): {len(generated_signature)}")
        public_key = ECC.import_key(data.public_key_pem, curve_name='prime256v1')
        # print(f"pk import done {public_key}")
        dec_signature = base64.b64decode(data.enc_signature)
        # print(f"{dec_signature}")
        # print(f"Decoded signature length: {len(dec_signature)}")
        verifier = DSS.new(public_key, "fips-186-3", encoding="der")
        # print("gen verifier done")
        verifier.verify(hash_value, dec_signature)
        print("Signature is valid.")
        return { "status":"success"}

    except ValueError as e:
        print("value error", e)
        traceback.print_exc()
        return{ "status": "value error"}
    except Exception as e:
        print("error")
        traceback.print_exc()
        return{ "status": "error"}
class Ballot(BaseModel):
    ciphers: list[list[str]]

@router.post("/elg")
async def elg(data: Ballot):
    # print(data)
    try:
        ciphers = []
        for cipher in data.ciphers:
            tmp = ElgamalCipherText()
            tmp.setCipher(cipher)
            ciphers.append(tmp)
        permut = Permutation()
        permut.genPermutation(len(ciphers))
        shuffled_ciphers = permut.cipherPermutation(params,keys,ciphers)
        re_shuffled = permut.cipherPermutation(params, keys, shuffled_ciphers)
        res = []
        for item in re_shuffled:
            print(item.decryption(params, keys).plainText)
            res.append(intToString(item.decryption(params, keys).plainText))
        for item in res:
            print(item)
        return {"status": "success"}
    except Exception as e:
        print(e)
        traceback.print_exc()
        return {"status": "fail"}