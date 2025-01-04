from sqlalchemy import Table, Column, Integer, String
from ..core.database import metadata

people = Table(
    "people",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("Age", Integer),
    Column("Gender", String(1)),
)

electoral_roll = Table(
    "electraol_roll",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("Age", Integer),
    Column("Gender", String(1)),
    Column("PINcode", Integer),
)

candidate_list = Table(
    "candidate_list",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("party", String(50)),
    Column("district", String(50)),
)

bulletin_board = Table(
    "bulletin_board",
    metadata,
    Column("id",Integer, primary_key=True),
    Column("info",String(511)),
)
