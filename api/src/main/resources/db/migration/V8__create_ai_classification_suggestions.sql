-- AI classification suggestions table.
-- Every suggestion is a candidate; humans approve or reject via the review workflow.
-- No suggestion directly mutates foia_requests without human action.
CREATE TABLE ai_classification_suggestions (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    foia_request_id     UUID NOT NULL REFERENCES foia_requests(id) ON DELETE CASCADE,
    suggested_category  VARCHAR(100) NOT NULL,
    suggested_priority  VARCHAR(20)  NOT NULL,
    confidence_score    NUMERIC(5,4) NOT NULL CHECK (confidence_score BETWEEN 0 AND 1),
    model_id            VARCHAR(100) NOT NULL,
    raw_response        TEXT,
    status              VARCHAR(20)  NOT NULL DEFAULT 'PENDING'
                            CHECK (status IN ('PENDING', 'APPROVED', 'REJECTED', 'OVERRIDDEN')),
    reviewer_id         BIGINT REFERENCES users(id) ON DELETE SET NULL,
    reviewer_note       TEXT,
    reviewed_at         TIMESTAMP,
    created_at          TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX idx_ai_cls_foia_request_id ON ai_classification_suggestions(foia_request_id);
CREATE INDEX idx_ai_cls_status          ON ai_classification_suggestions(status);