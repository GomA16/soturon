from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.database import engine, async_session
from .routers import registration, voting, test, mix, tally
from .models.election_tables import *
# from helios_crypto import *
import asyncio
from sqlalchemy import text

async def main():
    async with async_session() as session:
        # stmt = delete(TestTable).where(TestTable.tag == "test")
        async with session.begin():
            await session.execute(text("DELETE FROM all_ballots CASCADE"))
            await session.execute(text("DELETE FROM shuffled_ballots"))
            await session.execute(text("DELETE FROM revocation"))

if __name__ == "__main__":
    asyncio.run(main())