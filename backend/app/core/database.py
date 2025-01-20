import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, text

DATABASE_URL = "postgresql+asyncpg://postgres:601405@localhost:5433/postgres"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
                    bind=engine, 
                    class_=AsyncSession, 
                    expire_on_commit=False
                )

Base = declarative_base()