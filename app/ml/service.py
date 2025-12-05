import base64
import logging

from fastapi import HTTPException, UploadFile
from openai import AsyncOpenAI
from starlette.status import HTTP_503_SERVICE_UNAVAILABLE, HTTP_500_INTERNAL_SERVER_ERROR

from app.ml.config import ml_config
from app.ml.schemas import AnalysisResponse
from app.items.enums import ItemCategory

logger = logging.getLogger(__name__)

PROMPT = f"""
Ты — помощник в приложении обмена вещами. По фото составь описание товара.

Ответ должен состоять СТРОГО из одной строки с тремя частями, разделенными "|||".

Формат:

НАЗВАНИЕ|||ОПИСАНИЕ|||КАТЕГОРИЯ

Категории: {[i.capitalize() for i in ItemCategory.__members__.keys() ]}.

В описании укажи визуальные факты: цвет, состояние, дефекты.
Если бренд хорошо виден на фото (логотип, надпись), обязательно упомяни его.
Не выдумывай бренды и размеры, если их не видно на фото.

Если предмета не видно или ошибка, напиши:

ERROR|||Текст ошибки

Примеры:

Кружка|||Синяя керамическая кружка Luminarc со сколом.|||{ItemCategory.household.value}

Конструктор|||Куча разноцветных деталей Lego, хорошее состояние.|||{ItemCategory.toys.value}

Куртка|||Зелёная куртка The North Face из полиэстера, отличное состояние.|||{ItemCategory.clothes.value}

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

    async def analyze(self, images: list[UploadFile]) -> AnalysisResponse:
        try:
            if not ml_service:
                raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail="ML сервис недоступен")

            base64_images = []
            for image in images:
                contents = await image.read()
                base64_data = base64.b64encode(contents).decode()
                base64_images.append(base64_data)
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
                raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=error_msg.strip())

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
