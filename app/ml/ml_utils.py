from ml_processor import ItemProcessor
from app.models import Item
from typing import Optional

processor = ItemProcessor()

def enrich_item_data(item_data: dict, photos: Optional[list] = None) -> dict:
    """Обогащает данные вещи через ML"""
    
    title = item_data.get("title", "Unknown")
    
    result = processor.process_item_with_ml(title, photos or [])
    
    # Объединяем оригинальные данные с ML анализом
    enriched = item_data.copy()
    
    if result["enriched_data"]:
        # Если ML предложил категорию и её нет - добавляем
        if not enriched.get("category") and result["enriched_data"].get("auto_category"):
            enriched["suggested_category"] = result["enriched_data"]["auto_category"]
        
        # Если ML оценил состояние и его нет - добавляем
        if not enriched.get("condition") and result["enriched_data"].get("auto_condition"):
            enriched["suggested_condition"] = result["enriched_data"]["auto_condition"]
        
        # Дополняем описание ML анализом
        if result["enriched_data"].get("auto_description"):
            enriched["ml_description"] = result["enriched_data"]["auto_description"]
    
    enriched["ml_processed"] = result["ml_analysis"] is not None
    
    return enriched

def auto_detect_item_info(photos: list) -> dict:
    """Автоматически определяет информацию о вещи по фото"""
    
    if not photos:
        return {
            "category": None,
            "condition": None,
            "description": None
        }
    
    category = processor.suggest_category(photos[0])
    condition = processor.estimate_condition(photos[0])
    
    return {
        "category": category,
        "condition": condition,
        "description": f"Автоанализ: {category}, состояние {condition}"
    }