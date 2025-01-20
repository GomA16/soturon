import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, text

# データベースURL（適宜変更してください）
DATABASE_URL = "postgresql+asyncpg://postgres:601405@localhost:5433/postgres"

# 非同期エンジンとセッションのセットアップ
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# ベースクラス
Base = declarative_base()

# サンプルテーブル定義
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

# 非同期操作のサンプル関数
async def main():
    # テーブル作成
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # データベースにデータを挿入
    async with async_session() as session:
        async with session.begin():
            user1 = User(name="Alice", age=25)
            user2 = User(name="Bob", age=30)
            session.add_all([user1, user2])

    # データを読み取る
    async with async_session() as session:
        result = await session.execute(text("SELECT * FROM users"))
        rows = result.fetchall()
        for row in rows:
            print(row)

    # エンジンのクローズ
    await engine.dispose()

# メインループの実行
if __name__ == "__main__":
    asyncio.run(main())