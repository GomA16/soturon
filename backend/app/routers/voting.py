from fastapi import APIRouter, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from databases import Database
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, insert, select
from pydantic import BaseModel
from ..models.election_tables import people, electoral_roll, candidate_list, bulletin_board
from ..core.database import database
from ..components.myAlgs.myPrimitives import * 
from ..components.myAlgs.elgamal import *
from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
import base64
import traceback
import json
import os
from .shareResource import *

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

ballotList = []
revocationlist = []

@router.get("/challenge")
async def getChallenge():
    r = getRandomElement(int(vars["parameters"]["p"]))
    return {"challenge": str(r)}
router = APIRouter()



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
    
# class GetCandidateList(BaseModel):
#     district: str

@router.get("/getCandidateList")
async def getCandidateList():
    try:
        candidateList = json_data["candidateList"]
        print(candidateList)
        # response = []
        # for item in candidateList:
        #     if item["district"] == data.district:
        #         response.append(item["name"])
        # print("response",response)
        return ({"candidateList": candidateList})
    except Exception as e:
        traceback.print_exc()

class candidateChoice(BaseModel):
    candidate: list[str]
    pin: list[str]
    pk: str

@router.post("/submitBallot")
async def submitBallot(data: candidateChoice):
    print(data)
    try:
        params = Parameters()
        params.setParams(json_data["election_vars"]["parameters"])
        keys = ElgamalKeys()
        keys.setKeys(json_data["election_vars"]["authKeys"])
        encPIN = ElgamalCipherText()
        encPIN.setCipher(data.pin)
        pin = encPIN.decryption(params, keys)
        print("pin",pin)
        ballot = []
        if {"pk": data.pk, "PIN": pin} in sharedResource.sharedPIN:
            ballot = [data.candidate, data.pin, data.pk]
        else:
            dumy = ElgamalPlainText(1)
            encDumy = ElgamalCipherText()
            encDumy.encryption(params, keys, dumy)
            ballot = [encDumy.cipherText, data.pin, data.pk]
        for item in sharedResource.ballots:
            if item.pk == data.pk and item.pin == data.pin:
                sharedResource.addRevocationList(item)
        sharedResource.addBallot(ballot)
        sharedResource.showBallots()
        sharedResource.showRevocationList()
        return {"status": "success"}
    except Exception as e:
        traceback.print_exc()
        return {"states": "failed"}