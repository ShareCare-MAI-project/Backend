from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.ml.schemas import AnalysisRequest, AnalysisResponse
from app.ml.service import ml_service
from app.core.database import get_async_db
from app.items.schemas import Item

router = APIRouter(prefix="/ml", tags=["ML"])


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_item(request: AnalysisRequest) -> AnalysisResponse:
    
    if not ml_service:
        raise HTTPException(
            status_code=503,
            detail="ml не работает"
        )
    
    result = await ml_service.analyze(request.image_url)
    return result


@router.post("/analyze-item/{item_id}", response_model=AnalysisResponse)
async def analyze_and_fill_item(
    item_id: str,
    request: AnalysisRequest,
    db: Session = Depends(get_async_db)
) -> AnalysisResponse:
    
    if not ml_service:
        raise HTTPException(status_code=503, detail="ML сервис недоступен")
    
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail=f"Товар с ID {item_id} не найден")
    
    result = await ml_service.analyze(request.image_url)
    
    if result.error:
        raise HTTPException(status_code=400, detail=f"Ошибка анализа: {result.error}")
    
    if not item.name or item.name.strip() == "":
        item.name = result.name
    
    if not item.description or item.description.strip() == "":
        item.description = result.description
    
    if not item.category or item.category.strip() == "":
        item.category = result.category
    
    db.commit()
    db.refresh(item)
    
    return AnalysisResponse(
        name=result.name,
        description=result.description,
        category=result.category,
        error=None
    )


@router.post("/analyze-item-force/{item_id}", response_model=AnalysisResponse)
async def analyze_and_overwrite_item(
    item_id: str,
    request: AnalysisRequest,
    db: Session = Depends(get_async_db)
) -> AnalysisResponse:
    if not ml_service:
        raise HTTPException(status_code=503, detail="ML сервис недоступен")
    
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail=f"Товар с ID {item_id} не найден")
    
    result = await ml_service.analyze(request.image_url)
    
    if result.error:
        raise HTTPException(status_code=400, detail=f"Ошибка анализа: {result.error}")
    
    item.name = result.name
    item.description = result.description
    item.category = result.category
    
    db.commit()
    db.refresh(item)
    
    return AnalysisResponse(
        name=result.name,
        description=result.description,
        category=result.category,
        error=None
    )


@router.get("/health")
async def health():
    """проверка, работает ли ml"""
    if not ml_service:
        raise HTTPException(status_code=503)
    
    return {"status": "ok", "model": "prime-intellect/intellect-3"}
