-- Embeddings table for RAG semantic search.
-- Each row stores the vector representation of a FOIA request's text content.
-- Dimension 1536 matches text-embedding-3-small and voyage-3-lite.
-- If model changes, backfill is required (model_id tracks which model generated each row).
CREATE TABLE ai_embeddings (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    foia_request_id UUID NOT NULL REFERENCES foia_requests(id) ON DELETE CASCADE,
    model_id        VARCHAR(100) NOT NULL,
    embedding       vector(1536) NOT NULL,
    content_hash    VARCHAR(64)  NOT NULL,
    created_at      TIMESTAMP    NOT NULL DEFAULT now(),
    CONSTRAINT uq_embedding_request_model UNIQUE (foia_request_id, model_id)
);

CREATE INDEX idx_ai_emb_foia_request_id ON ai_embeddings(foia_request_id);
CREATE INDEX idx_ai_emb_embedding_hnsw
    ON ai_embeddings
    USING hnsw (embedding vector_cosine_ops);