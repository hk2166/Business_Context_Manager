+------------------------------------------------------+
| User / AI Agent |
| (Invoice Processing / Risk Check / Escalation) |
+------------------------------------------------------+
                           |
                           v
+------------------------------------------------------+
| Decision Context Engine |
| - Aggregation |
| - Trend Detection |
| - Conflict Resolution |
| - Context Summarization |
+------------------------------------------------------+
                            |
                            v
+------------------------------------------------------+
| Multi-Factor Ranking Layer |
| - Semantic Score |
| - Temporal Decay |
| - Severity Weight |
| - Graph Proximity Boost |
| - Trend Weight |
+------------------------------------------------------+
                            |
                            v
+------------------------------------------------------+
| Hybrid Retrieval Layer |
| ------------------ ------------------ |
| | Semantic Search | | Lexical Search | |
| | (pgvector KNN) | | (BM25) | |
| ------------------ ------------------ |
+------------------------------------------------------+
                            |
                            v
+------------------------------------------------------+
| Memory Storage Layer |
| |
| - Entity Table |
| - Memory Table (Episodic / Semantic / Pattern) |
| - Relation Graph |
| - Embedding Vectors |
+------------------------------------------------------+
                            |
                            v
+------------------------------------------------------+
| PostgreSQL + pgvector |
| (Indexed Embeddings + Metadata) |
+------------------------------------------------------+



