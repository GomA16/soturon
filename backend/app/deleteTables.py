from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.database import engine, async_session
from .routers import registration, voting, test, mix, tally
from .models.election_tables import *
# from helios_crypto import *
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, text

async def main():
    async with async_session() as session:
        # stmt = delete(TestTable).where(TestTable.tag == "test")
        async with session.begin():
            await session.execute(text("DROP TABLE IF EXISTS bulletin_board"))
            await session.execute(text("DROP TABLE IF EXISTS electoral_roll"))
            await session.execute(text("DROP TABLE IF EXISTS all_ballots CASCADE"))
            await session.execute(text("DROP TABLE IF EXISTS shuffled_ballots"))
            await session.execute(text("DROP TABLE IF EXISTS revocation"))

if __name__ == "__main__":
    asyncio.run(main())