from fastapi import APIRouter, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from databases import Database
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, insert, select
from pydantic import BaseModel
from ..models.election_tables import people, electoral_roll
from ..core.database import database
# from helios_crypto import *

router = APIRouter()

class PeopleData(BaseModel):
    name: str
    Age: int
    Gender: str

@router.post("/")
async def registraion(data: PeopleData):
    print("registration data", data)
    if (int(data.Age) > 0) & (data.Gender in {"F", "M"}): 
        query = select(people).where(
                (people.c.name == data.name) &
                (people.c.Age ==  data.Age) &
                (people.c.Gender == data.Gender)
            )
        condition = await database.fetch_one(query)

        if condition:
            return {"status": "success", "message": "success"}
        else:
            return {"status": "fail", "message": "fail"}
    else:
        return{"status": "fail", "message": "invalid input"}
    
class PINData(BaseModel):
    name: str
    Age: int
    Gender: str
    PINcode: int

@router.post("/regist_pin")
async def regist_pin(data: PINData):
    print("regist_pin data ",data)
        # 入力データのバリデーション
    if data.Age <= 0 or data.Gender not in {"M", "F"}:
        raise HTTPException(status_code=400, detail="Invalid input data")
    # レコードが既存するかチェック
    query = select(people).where(
        (electoral_roll.c.name == data.name) &
        (electoral_roll.c.Age == data.Age) &
        (electoral_roll.c.Gender == data.Gender)
    )
    existing_record = await database.fetch_one(query)

    if existing_record:
        # raise HTTPException(
        #     status_code=409, 
        #     detail="User with the same details already exists"
        # )
        return{"status": "fail", "message": "PINcode already exists"}

    # 新しいレコードを挿入
    insert_query = electoral_roll.insert().values(
        name=data.name,
        Age=data.Age,
        Gender=data.Gender,
        PINcode=data.PINcode  # PINcodeを新しい列として保存
    )
    await database.execute(insert_query)

    return {"status": "success", "message": "User registered successfully"}