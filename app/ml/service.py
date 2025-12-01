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

В описании укажи визуальные факты: цвет, состояние, дефекты.
Если бренд хорошо виден на фото (логотип, надпись), обязательно упомяни его.
Не выдумывай бренды и размеры, если их не видно на фото.

Если предмета не видно или ошибка, напиши:

ERROR|||Текст ошибки

Примеры:

Кружка|||Синяя керамическая кружка Luminarc со сколом.|||Быт

Конструктор|||Куча разноцветных деталей Lego, хорошее состояние.|||Игрушки

Куртка|||Зелёная куртка The North Face из полиэстера, отличное состояние.|||Одежда

ERROR|||Фото слишком темное.
"""


class MLService:

    def __init__(self):
        if not ml_config.OPENROUTER_API_KEY:
            raise ValueError("Нет API ключа для OpenRouter")
        
        self.client = AsyncOpenAI(
            base_url=ml_config.OPENROUTER_BASE_URL,
            api_key=ml_config.OPENROUTER_API_KEY
        )

    async def analyze_multiple_base64(self, base64_images: list[str]) -> AnalysisResponse:
        try:
            content = [{"type": "text", "text": PROMPT}]
            
            for base64_data in base64_images:
                content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_data}"}
                })
            
            response = await self.client.chat.completions.create(
                model=ml_config.MODEL_NAME,
                messages=[{"role": "user", "content": content}],
                temperature=0.3
            )
            
            text = response.choices[0].message.content.strip()
            logger.info(f"AI ответ: {text}")
            
            if text.startswith("ERROR"):
                error_msg = text.split("|||")[1] if "|||" in text else text
                raise Exception(error_msg.strip())
            
            parts = text.split("|||")
            if len(parts) < 3:
                raise Exception("Неверный формат ответа")
            
            return AnalysisResponse(
                name=parts[0].strip(),
                description=parts[1].strip(),
                category=parts[2].strip()
            )
        except Exception as e:
            logger.error(f"ML Error: {e}")
            raise


try:
    ml_service = MLService()
except ValueError:
    logger.warning("ML сервис не инициализирован")
    ml_service = None
