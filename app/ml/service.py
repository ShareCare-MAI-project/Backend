import json
import logging
from openai import OpenAI
from app.ml.config import ml_config
from app.ml.schemas import AnalysisResponse

logger = logging.getLogger(__name__)


class MLService:
    
    def __init__(self):
        if not ml_config.OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY не установлен в .env")
        
        self.client = OpenAI(
            base_url=ml_config.OPENROUTER_BASE_URL,
            api_key=ml_config.OPENROUTER_API_KEY
        )
    
    async def analyze(self, image_url: str) -> AnalysisResponse:
        
        try:
            # Отправляем запрос к модели с фото
            response = self.client.chat.completions.create(
                model=ml_config.MODEL_NAME,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """Ты — AI-ассистент для приложения шеринга вещей "ShareCare". Твоя задача — проанализировать фотографию вещи, которую пользователь хочет отдать, и сформировать JSON с описанием для объявления.

Правила:
1. Язык ответа: Русский.
2. Формат ответа: Только валидный JSON, без markdown-разметки (``````).
3. Назови объект (object) кратко в одно-два слова что за предмет на фото (футболка, кружка и тп).
3. Категории (category) могут быть только одни из списка: \"Одежда\", \"Игрушки\", \"Быт\", \"Электроника\", \"Другое\".
4. Если на фото несколько вещей, описывай самую крупную или ту, что в центре.
5. Описание (description) должно быть полезным: укажи цвет, материал(если уверен), состояние (если видно), бренд (если читается) и тип предмета.Описание должно быть похоже на объявление реального человека.
6. Если фото не содержит предметов (черный экран, размыто, запрещенный контент) — верни поле "error": \"Не удалось распознать предмет\".
Структура JSON(порядок обязателен):
{
  "object": "Что за предмет на фото (футболка шкаф и тп )",
  "description": "Подробное описание (2-3 предложения). Укажи цвет, состояние, особенности.",
  "category": "Одежда" | "Игрушки" | "Быт" | "Электроника" | "Другое",
}"""
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": image_url}
                            }
                        ]
                    }
                ],
                temperature=0.7,
                max_tokens=300
            )
            content = response.choices[0].message.content 
            
            data = self._parse_json(content)
            
            valid_categories = ["Одежда", "Игрушки", "Быт", "Электроника", "Другое"]
            if data.get("category") not in valid_categories:
                data["category"] = "Другое"
            
            return AnalysisResponse(
                name=data.get("object", "Товар"),
                description=data.get("description", ""),
                category=data.get("category", "Другое")
            )
        
        except Exception as e:
            logger.error(f"Ошибка при анализе: {str(e)}")
            return AnalysisResponse(
                name="",
                description="",
                category="Другое",
                error=f"Ошибка: {str(e)}"
            )
    
    def _parse_json(self, content: str) -> dict:
        content = content.strip()
        
        if content.startswith("```"):
            content = content.split("```")
            if content.startswith("json"):
                content = content[4:]
        
        content = content.strip()
        return json.loads(content)


try:
    ml_service = MLService()
except ValueError as e:
    logger.warning(f"ml не работает: {e}")
    ml_service = None
