from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.database import get_db
from app.models import Entity, Memory

router = APIRouter()


class MemoryCreate(BaseModel):
    entity_name: str
    entity_type: str
    content: str
    memory_type: str
    severity: Optional[float] = 0.0


@router.post("/memories")
async def create_memory(payload: MemoryCreate, db: AsyncSession = Depends(get_db)):

    # 1️⃣ Find or create entity
    result = await db.execute(
        select(Entity).where(
            Entity.name == payload.entity_name,
            Entity.entity_type == payload.entity_type
        )
    )
    entity = result.scalar_one_or_none()

    if not entity:
        entity = Entity(
            name=payload.entity_name,
            entity_type=payload.entity_type
        )
        db.add(entity)
        await db.flush()

    # 2️⃣ Create memory
    memory = Memory(
        entity_id=entity.id,
        content=payload.content,
        memory_type=payload.memory_type,
        severity=payload.severity,
        created_at=datetime.utcnow()
    )

    db.add(memory)
    await db.commit()

    return {"message": "Memory stored successfully"}