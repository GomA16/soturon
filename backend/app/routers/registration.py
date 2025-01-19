from fastapi import APIRouter, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from databases import Database
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, insert, select
from pydantic import BaseModel
# from helios_crypto import *
from ..models.election_tables import people, electoral_roll
from ..core.database import database
from ..components.myAlgs.myPrimitives import getRandomElement
from ..data.variables import vars
from ..components.myAlgs.permutations import *
from ..components.myAlgs.myPrimitives import * 
from ..components.myAlgs.elgamal import *
from ..components.myAlgs.commitment import *
from ..components.myAlgs.hash import *
from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from .shareResource import sharedResource
import base64
import traceback
import json
import os

# 現在のスクリプトのディレクトリを取得
current_dir = os.path.dirname(__file__)

# data ディレクトリへのパスを作成
json_path = os.path.join(current_dir, "..", "data", "data.json")
# json_path = "../data/data.json"
with open(json_path, 'r') as file:
    json_data= json.load(file)
voterInfoList  = json_data["voterInfoList"]
officialKey = json_data["officialKey"]
router = APIRouter()

@router.get("/challenge")
async def getChallenge():
    r = getRandomElement(int(vars["parameters"]["p"]))
    return {"challenge": str(r)}

class VoterData(BaseModel):
    name: str
    Age: str
    Gender: str
    challenge: str
    signature: str

@router.post("/verifyVoter")
async def verifyVoter(data: VoterData):
    print("response data", data)
    # name, age, genderをデータベースと照合して対応するpkを得る
    pk = ""
    for item in voterInfoList:
        if data.name == item["name"] and data.Age == str(item["Age"]) and data.Gender == item["Gender"]:
            pk = item["verifyKey"]
    # pkで署名を確認
    try:
        # print(base64.b64decode(data.challenge))
        # todo: できればデコードしたチャレンジがバックエンドが送信したものと一致するか確認したい
        hash_value = SHA256.new((data.challenge.encode('utf-8')))
        public_key = ECC.import_key(pk, curve_name='prime256v1')
        # print(f"pk import done {public_key}")
        dec_signature = base64.b64decode(data.signature)
        print(f"{dec_signature}")
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
    
class OfficialResponse(BaseModel):
    message: str
    signature: str

@router.post("/verifyOfficial")
async def verifyOfficial(data: OfficialResponse):
    pk = officialKey["verifyKey"]
    # pkで署名を確認
    try:
        print(base64.b64decode(data.message))
        # todo: できればデコードしたチャレンジがバックエンドが送信したものと一致するか確認したい
        hash_value = SHA256.new((data.message.encode('utf-8')))
        public_key = ECC.import_key(pk, curve_name='prime256v1')
        # print(f"pk import done {public_key}")
        dec_signature = base64.b64decode(data.signature)
        print(f"{dec_signature}")
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

class PINdata(BaseModel):
    pk: str
    PIN: list[str]
@router.post("/registerPIN")
async def registerPIN(data: PINdata):
    print("done")
    params = Parameters()
    params.setParams(json_data["election_vars"]["parameters"])
    keys = ElgamalKeys()
    keys.setKeys(json_data["election_vars"]["authKeys"])
    cipher = ElgamalCipherText()
    cipher.setCipher(data.PIN)
    pin = cipher.decryption(params, keys)
    print(pin)
    sharedResource.updatePINList(data.pk, pin.plainText)
    sharedResource.getPINList()
    return {"status": "success"}