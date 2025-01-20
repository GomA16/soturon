# from fastapi import FastAPI
from ..core.database import engine, async_session
# from .routers import registration, voting, test, mix, tally
from ..models.election_tables import *
# from helios_crypto import *
import asyncio
from sqlalchemy import text

async def main():

    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    
    async with async_session() as session:
        result = await session.execute(text("SELECT * FROM electoral_roll"))
        print("\nresult\n",result.fetchall())
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())