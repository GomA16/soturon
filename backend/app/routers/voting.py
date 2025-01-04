from fastapi import APIRouter, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from databases import Database
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, insert, select
from pydantic import BaseModel
from ..models.election_tables import people, electoral_roll, candidate_list, bulletin_board
from ..core.database import database

router = APIRouter()

class VoterData(BaseModel):
    name: str
    Age: int
    Gender: str

@router.post("/")
async def votin_top(data: VoterData):
    # electoral_rollに基本情報を含むレコードがあるかを確認
    print("voting data", data)
    if (int(data.Age) > 0) & (data.Gender in {"F", "M"}): 
        query = select(electoral_roll).where(
                (electoral_roll.c.name == data.name) &
                (electoral_roll.c.Age ==  data.Age) &
                (electoral_roll.c.Gender == data.Gender)
            )
        condition = await database.fetch_one(query)

        if condition:
            return {"status": "success", "message": "success"}
        else:
            return {"status": "fail", "message": "fail"}
    else:
        return{"status": "fail", "message": "invalid input"}
    
@router.get("/candidates")
async def get_candidate():
    query = select(candidate_list)
    result = await database.fetch_all(query)
    response ={"candidates": [dict(row) for row in result]} 
    print(response)
    return response

class CandidateData(BaseModel):
    id: int
    name: str
    party: str
    district: str

class BallotData(BaseModel):
    name: str
    PINcode: int
    selectedCandidate: CandidateData

@router.post("/addballot")
async def add_ballot(data: BallotData):
    query = insert(bulletin_board).values(
            name=data.name,
            PINcode=data.PINcode,
            candidate_id=data.selectedCandidate.id,
            candidate_name=data.selectedCandidate.name,
            candidate_party=data.selectedCandidate.party,
            candidate_district=data.selectedCandidate.district,
        )
    await database.execute(query)

    return{"status": "success", "message": "ballot was added"}