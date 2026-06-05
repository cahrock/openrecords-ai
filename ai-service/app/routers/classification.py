from fastapi import APIRouter, HTTPException
from app.models.classification import ClassificationRequest, ClassificationResponse
from app.services.classification_service import classify_request
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/classify", response_model=ClassificationResponse)
async def classify(req: ClassificationRequest):
    if not req.subject or not req.description:
        raise HTTPException(status_code=422, detail="subject and description are required")
    try:
        return await classify_request(req)
    except Exception as e:
        logger.error("Classification failed for request %s: %s", req.foia_request_id, e)
        raise HTTPException(status_code=502, detail="AI service classification failed")