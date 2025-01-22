from fastapi import APIRouter, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ..models.election_tables import *
from pydantic import BaseModel
# from helios_crypto import *
from ..core.database import async_session, engine
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
import asyncio
from sqlalchemy import text
import ast

# 現在のスクリプトのディレクトリを取得
current_dir = os.path.dirname(__file__)

# data ディレクトリへのパスを作成
json_path = os.path.join(current_dir, "..", "data", "data.json")
# json_path = "../data/data.json"
with open(json_path, 'r') as file:
    json_data= json.load(file)
voterInfoList  = json_data["voterInfoList"]
officialKey = json_data["officialKey"]
params = Parameters()
params.setParams(json_data["election_vars"]["parameters"])
keys = ElgamalKeys()
keys.setKeys(json_data["election_vars"]["tallyKeys"])
mixedBallots = sharedResource.mixedBallots

router = APIRouter()

@router.get("/tallyBallots")
async def tallyBallots():
    try:
        encBallots = []
        async with async_session() as session:
            result = await session.execute(text("SELECT * FROM shuffled_ballots"))
            items = result.fetchall()
            for item in items:
                encBallots.append(ElgamalCipherText().setCipher(ast.literal_eval(item.candidate)))
        for item in encBallots:
            print(item)
        decBallots = [item.decryption(params, keys).plainText for item in encBallots]
        for item in decBallots:
            print(item)
        result = {}
        print(type(decBallots[0]))
        for item in decBallots:
            if item in result.keys():
                result[item] += 1
            else:
                result[item] = 1
        print(result)
        return {"reuslt": result, "decBallots": decBallots}
    except Exception as e:
        traceback.print_exc()
        return {"reuslt": result, "decBallots": decBallots}
