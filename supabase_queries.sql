CREATE TABLE IF NOT EXISTS entities (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS memories (
    id SERIAL PRIMARY KEY,
    entity_id INTEGER REFERENCES entities(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    memory_type TEXT NOT NULL,
    severity FLOAT DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT NOW(),
    is_stale BOOLEAN DEFAULT FALSE,
    embedding VECTOR(1536)
);

CREATE TABLE IF NOT EXISTS relations (
    id SERIAL PRIMARY KEY,
    from_entity INTEGER REFERENCES entities(id) ON DELETE CASCADE,
    to_entity INTEGER REFERENCES entities(id) ON DELETE CASCADE,
    relation_type TEXT
);