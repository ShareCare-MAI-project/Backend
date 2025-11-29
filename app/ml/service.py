import logging
from openai import AsyncOpenAI
from app.ml.config import ml_config
from app.ml.schemas import AnalysisResponse

logger = logging.getLogger(__name__)

PROMPT = """
Ты — помощник в приложении обмена вещами. По фото составь описание товара.
Ответ должен состоять СТРОГО из одной строки с тремя частями, разделенными "|||".

Формат:
НАЗВАНИЕ|||ОПИСАНИЕ|||КАТЕГОРИЯ

Категории: "Одежда", "Игрушки", "Быт", "Электроника", "Другое".

В описании укажи визуальные факты: цвет, состояние, дефекты. Не выдумывай бренды и размеры.

Если предмета не видно или ошибка, напиши:
ERROR|||Текст ошибки

Примеры:
Кружка|||Синяя керамическая кружка со сколом.|||Быт
Конструктор|||Куча разноцветных деталей Lego.|||Игрушки
ERROR|||Фото слишком темное.
"""
class MLService:
        
    def __init__(self):
        if not ml_config.OPENROUTER_API_KEY:
            raise ValueError("Нет API ключа")
        
        self.client = AsyncOpenAI(
            base_url=ml_config.OPENROUTER_BASE_URL,
            api_key=ml_config.OPENROUTER_API_KEY
        )
    
    async def analyze(self, image_url: str) -> AnalysisResponse:
        try:
            response = await self.client.chat.completions.create(
                model=ml_config.MODEL_NAME,
                messages=[
                    {"role": "system", "content": PROMPT},
                    {"role": "user", "content": [{"type": "image_url", "image_url": {"url": image_url}}]}
                ],
                temperature=0.3
            )
            text = response.choices[0].message.content.strip()
            logger.info(f"ответ ml {text}")

            if text.startswith("ERROR"):
                error_msg = text.split("|||")[1] if "|||" in text else text
                return AnalysisResponse(name="", description="", category="", error=error_msg)

            parts = text.split("|||")
            
            if len(parts) < 3:
                return AnalysisResponse(name="", description="", category="", error="Неверный формат ответа")

            return AnalysisResponse(
                name=parts[0].strip(),
                description=parts[1].strip(),
                category=parts[2].strip()
            )

        except Exception as e:
            logger.error(f"ML Error: {e}")
            return AnalysisResponse(name="",description="", category="", error=str(e))

try:
    ml_service = MLService()
except ValueError:
    ml_service = None
