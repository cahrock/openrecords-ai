import anthropic
from uuid import UUID
from app.config import settings
from app.models.classification import ClassificationRequest, ClassificationResponse

SYSTEM_PROMPT = """You are an expert FOIA request classifier for a federal agency.
Given a FOIA request, classify it into a category and priority level.

Categories (choose exactly one):
- PERSONNEL_RECORDS
- FINANCIAL_RECORDS
- ENVIRONMENTAL_DATA
- LAW_ENFORCEMENT
- CONTRACTS_PROCUREMENT
- POLICY_DOCUMENTS
- COMMUNICATIONS
- OTHER

Priority levels (choose exactly one):
- LOW: routine request, no urgency indicators
- MEDIUM: moderate complexity or public interest
- HIGH: time-sensitive, involves public safety, or significant public interest

Respond in this exact format, nothing else:
CATEGORY: <category>
PRIORITY: <priority>
CONFIDENCE: <0.0 to 1.0>
REASONING: <one sentence explanation>"""


def _build_user_prompt(req: ClassificationRequest) -> str:
    return f"""Subject: {req.subject}

Description: {req.description}

Records Requested: {req.records_requested}"""


def _parse_response(text: str, foia_request_id: UUID, model_id: str) -> ClassificationResponse:
    lines = {
        line.split(":")[0].strip(): ":".join(line.split(":")[1:]).strip()
        for line in text.strip().splitlines()
        if ":" in line
    }

    category = lines.get("CATEGORY", "OTHER").strip()
    priority = lines.get("PRIORITY", "MEDIUM").strip()
    confidence = float(lines.get("CONFIDENCE", "0.5"))
    confidence = max(0.0, min(1.0, confidence))

    return ClassificationResponse(
        foia_request_id=foia_request_id,
        suggested_category=category,
        suggested_priority=priority,
        confidence_score=confidence,
        model_id=model_id,
        raw_response=text,
    )


async def classify_request(req: ClassificationRequest) -> ClassificationResponse:
    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    message = client.messages.create(
        model=settings.anthropic_model,
        max_tokens=256,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": _build_user_prompt(req)}],
    )

    raw_text = message.content[0].text
    return _parse_response(raw_text, req.foia_request_id, settings.anthropic_model)