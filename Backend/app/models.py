from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base
from pgvector.sqlalchemy import Vector
from datetime import datetime

Base = declarative_base()


class Entity(Base):
    __tablename__ = "entities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    entity_type = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True, index=True)

    entity_id = Column(Integer, ForeignKey("entities.id", ondelete="CASCADE"))

    content = Column(Text, nullable=False)

    memory_type = Column(Text, nullable=False)

    severity = Column(Float, default=0.0)

    created_at = Column(DateTime, default=datetime.utcnow)

    is_stale = Column(Boolean, default=False)

    embedding = Column(Vector(1536))


class Relation(Base):
    __tablename__ = "relations"

    id = Column(Integer, primary_key=True, index=True)

    from_entity = Column(Integer, ForeignKey("entities.id", ondelete="CASCADE"))

    to_entity = Column(Integer, ForeignKey("entities.id", ondelete="CASCADE"))

    relation_type = Column(Text)