import math

from app.utils.embedding import get_embedding
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from sqlalchemy import select

from app.database import get_db
from app.models import Entity, Memory

router = APIRouter()


class MemoryCreate(BaseModel):
    entity_name: str
    entity_type: str
    content: str
    memory_type: str
    severity: Optional[float] = 0.0


class MemoryQuery(BaseModel):
    query: str
    top_k: int = 5
    entity_name: Optional[str] = None
    entity_type: Optional[str] = None


@router.post("/memories")
async def create_memory(payload: MemoryCreate, db: AsyncSession = Depends(get_db)):

    
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


    embedding_vector = await get_embedding(payload.content)

    memory = Memory(
        entity_id=entity.id,
        content=payload.content,
        memory_type=payload.memory_type,
        severity=payload.severity,
        created_at=datetime.utcnow(),
        embedding=embedding_vector
)
    
    

    db.add(memory)
    await db.commit()

    return {"message": "Memory stored successfully"}

# --------------------------------------------------------------------------------------------------------------------

@router.post("/search")
async def search_memory(payload: MemoryQuery, db: AsyncSession = Depends(get_db)):

    query_embedding = await get_embedding(payload.query)

    stmt = (
        select(
            Memory.id,
            Memory.content,
            Memory.severity,
            Memory.created_at,
            Memory.entity_id,
            (1 - Memory.embedding.cosine_distance(query_embedding)).label("semantic_similarity")
        )
        .where(Memory.embedding.is_not(None))
    )

    # 🔹 Entity filter (if provided)
    if payload.entity_name and payload.entity_type:
        entity_result = await db.execute(
            select(Entity).where(
                Entity.name == payload.entity_name,
                Entity.entity_type == payload.entity_type
            )
        )
        entity = entity_result.scalar_one_or_none()

        if entity:
            stmt = stmt.where(Memory.entity_id == entity.id)

    stmt = stmt.order_by(Memory.embedding.cosine_distance(query_embedding)).limit(payload.top_k)

    result = await db.execute(stmt)
    rows = result.all()

    final_results = []
    now = datetime.utcnow()

    for row in rows:

        age_days = (now - row.created_at).days
        half_life = 90
        temporal_weight = math.exp(-math.log(2) * age_days / half_life)

        severity_weight = 1 + (row.severity / 10)

        final_score = row.semantic_similarity * temporal_weight * severity_weight

        final_results.append({
            "id": row.id,
            "content": row.content,
            "semantic_similarity": float(row.semantic_similarity),
            "temporal_weight": temporal_weight,
            "severity_weight": severity_weight,
            "final_score": final_score
        })

    final_results.sort(key=lambda x: x["final_score"], reverse=True)

    return final_results