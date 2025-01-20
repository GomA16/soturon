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
    ballots = sharedResource.ballots
    revocationList = sharedResource.revocationList
    plainBallots = [item for item in ballots if item not in revocationList]
    phai1 = Permutation()
    phai2 = Permutation()
    phai1.genPermutation(len(plainBallots))
    phai2.genPermutation(len(plainBallots))
    firstMixedBallots = phai1.doPermutation(plainBallots)
    secondMixedBallots = phai2.doPermutation(firstMixedBallots)
    sharedResource.setMixedBallots(secondMixedBallots)
    return {"mixResult": secondMixedBallots}