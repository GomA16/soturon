from fastapi import APIRouter, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from ..models.election_tables import *
from pydantic import BaseModel
from ..core.database import async_session, engine
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
import asyncio
import ast
from sqlalchemy import text

# 現在のスクリプトのディレクトリを取得
current_dir = os.path.dirname(__file__)

# data ディレクトリへのパスを作成
json_path = os.path.join(current_dir, "..", "data", "data.json")
# json_path = "../data/data.json"
with open(json_path, 'r') as file:
    json_data= json.load(file)
voterInfoList  = json_data["voterInfoList"]
officialKey = json_data["officialKey"]
params = json_data["election_vars"]["parameters"]

router = APIRouter()

@router.get("/mixBallots")
async def mixBallots():
    ballots = []
    async with async_session() as session:
        result = await session.execute(text("SELECT * FROM all_ballots"))
        items = result.fetchall()
        for item in items:
            if item.revocated == "False":
                ballots.append(ast.literal_eval(item.candidate))
    print("ballots\n",ballots)
    phai1 = Permutation()
    phai2 = Permutation()
    phai1.genPermutation(len(ballots))
    phai2.genPermutation(len(ballots))
    firstMixedBallots = phai1.doPermutation(ballots)
    print(firstMixedBallots)
    secondMixedBallots = phai2.doPermutation(firstMixedBallots)
    async with async_session() as session:
        async with session.begin():
            for item in secondMixedBallots:
                # print(type(item))
                ballot = ShuffleBallots(candidate=str(item))
                session.add(ballot)
    return {"mixResult": secondMixedBallots}