from ml_analyzer import ImageAnalyzer
from typing import Optional

class ItemProcessor:
    """Обработчик вещей с ML"""
    
    def __init__(self):
        self.analyzer = ImageAnalyzer()
    
    def process_item_with_ml(self, title: str, photos: list) -> dict:
        """Обогащает информацию о вещи через ML"""
        
        results = {
            "title": title,
            "ml_analysis": None,
            "enriched_data": {}
        }
        
        if photos and len(photos) > 0:
            # Анализируем первое фото
            first_photo = photos[0]
            
            # Если это URL - обрабатываем как строку
            if isinstance(first_photo, str):
                results["ml_analysis"] = {
                    "status": "photo_is_url",
                    "message": f"Анализ доступен для загруженных файлов"
                }
            else:
                # Если это bytes
                analysis = self.analyzer.analyze_image(first_photo)
                results["ml_analysis"] = analysis
                
                if analysis["success"]:
                    results["enriched_data"] = {
                        "auto_category": analysis["category"],
                        "auto_condition": analysis["condition"],
                        "auto_description": analysis["description"]
                    }
        
        return results
    
    def suggest_category(self, image_bytes: Optional[bytes]) -> Optional[str]:
        """Предлагает категорию на основе фото"""
        if not image_bytes:
            return None
        
        analysis = self.analyzer.analyze_image(image_bytes)
        
        if analysis["success"]:
            return analysis["category"]
        
        return None
    
    def estimate_condition(self, image_bytes: Optional[bytes]) -> Optional[str]:
        """Оценивает состояние вещи по фото"""
        if not image_bytes:
            return None
        
        analysis = self.analyzer.analyze_image(image_bytes)
        
        if analysis["success"]:
            return analysis["condition"]
        
        return None