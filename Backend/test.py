import asyncio
from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models import Entity

async def test():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Entity))
        print("Entities:", result.scalars().all())

asyncio.run(test())