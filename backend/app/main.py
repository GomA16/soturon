from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.database import database, metadata, engine
from .routers import registration, voting, test, mix, tally
from .models.election_tables import *
# from helios_crypto import *


app = FastAPI()

metadata.create_all(engine)

app.include_router(registration.router, prefix="/registration", tags=["registration"])
app.include_router(voting.router, prefix="/voting", tags=["voting"])
app.include_router(mix.router, prefix="/mix", tags=["mix"])
app.include_router(tally.router, prefix="/tally", tags=["tally"])
app.include_router(test.router, prefix="/test", tags=["test"])


# フロントエンドからのCORSを許可
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Reactのデフォルトポート
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
