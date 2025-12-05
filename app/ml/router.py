from fastapi import APIRouter, HTTPException, UploadFile, File

from app.ml.schemas import AnalysisResponse
from app.ml.service import ml_service
from app.utils.decorators.handle_errors import handle_errors

router = APIRouter(prefix="/ml", tags=["ML"])


@router.post("/analyze-images", response_model=AnalysisResponse)
@handle_errors()
async def analyze_images(images: list[UploadFile] = File(...)) -> AnalysisResponse:
    return await ml_service.analyze(images)


@router.get("/health")
async def health():
    """Проверка статуса ML сервиса"""
    if not ml_service:
        raise HTTPException(status_code=503, detail="ML сервис недоступен")
    return {"status": "ok"}
