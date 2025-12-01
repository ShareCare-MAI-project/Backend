from fastapi import APIRouter, HTTPException, UploadFile, File

from app.ml.schemas import AnalysisResponse
from app.ml.service import ml_service

router = APIRouter(prefix="/ml", tags=["ML"])


@router.post("/analyze-images", response_model=AnalysisResponse)
async def analyze_images(images: list[UploadFile] = File(...)) -> AnalysisResponse:
    if not ml_service:
        raise HTTPException(status_code=503, detail="ML сервис недоступен")
    
    import base64
    
    base64_images = []
    for image in images:
        contents = await image.read()
        base64_data = base64.b64encode(contents).decode("utf-8")
        base64_images.append(base64_data)
    
    try:
        result = await ml_service.analyze_multiple_base64(base64_images)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/health")
async def health():
    """Проверка статуса ML сервиса"""
    if not ml_service:
        raise HTTPException(status_code=503, detail="ML сервис недоступен")
    return {"status": "ok"}
