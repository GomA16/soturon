from sqlalchemy import Table, Column, Integer, String
from ..core.database import metadata

people = Table(
    "people",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("Age", Integer),
    Column("Gender", String(1)),
)

electoral_roll = Table(
    "electraol_roll",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("Age", Integer),
    Column("Gender", String(1)),
    Column("PINcode", Integer),
)

candidate_list = Table(
    "candidate_list",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("party", String),
    Column("district", String),
)

bulletin_board = Table(
    "bulletin_board",
    metadata,
    Column("id",Integer, primary_key=True),
    Column("tag", String),
    Column("info",String),
)
