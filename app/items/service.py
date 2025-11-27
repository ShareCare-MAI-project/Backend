import uuid
from pathlib import Path
from uuid import UUID

import uuid_utils
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from app.items.cruds.item_crud import ItemCrud
from app.items.mappers import ItemBase_to_ItemResponse, Item_to_ItemBase, deliveries_bases_to_deliveries, \
    image_bases_to_images_links, ItemDelivery_to_ItemDeliveryTypeBase
from app.items.schemas import ItemResponse, Item
from app.utils.consts import SUCCESS_RESPONSE
from app.items.cruds.item_image_crud import ItemImageCrud
from app.items.models import ItemImageBase
from app.items.cruds.item_delivery_crud import ItemDeliveryCrud


class ItemsService:
    @staticmethod
    async def get_item(db: AsyncSession, item_id: UUID) -> ItemResponse:
        item = await ItemCrud.get_item(db, item_id)

        if not item:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Товар не найден")

        return ItemBase_to_ItemResponse(item)

    @staticmethod
    async def get_items(db: AsyncSession) -> list[ItemResponse]:
        items = await ItemCrud.get_items(db)
        return list(map(
            ItemBase_to_ItemResponse,
            items
        ))

    @staticmethod
    async def create_item(db: AsyncSession, item: Item, images: list[UploadFile], owner_id: uuid.UUID):
        item_base = Item_to_ItemBase(item=item, owner_id=owner_id)

        images_links = [await i for i in [ItemsService.save_image(images) for images in images]]

        await ItemCrud.create_item(db, item_base)
        await db.flush()
        item_id = item_base.id

        to_await = []
        for image_id, image_link in images_links:
            job = ItemImageCrud.create(db, ItemImageBase(id=image_id, item_id=item_id, image=image_link))
            to_await.append(job)

        for delivery_type in item.delivery_types:
            job = ItemDeliveryCrud.create(db, ItemDelivery_to_ItemDeliveryTypeBase(item_delivery=delivery_type,
                                                                                   item_id=item_id))
            to_await.append(job)

        for i in to_await:
            await i

        await db.commit()
        await db.refresh(item_base)

        return SUCCESS_RESPONSE

    @staticmethod
    async def save_image(image: UploadFile) -> tuple[UUID, str] | None:
        if not image.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail="File must be an image"
            )

        image_id = uuid_utils.uuid7()
        filename = f"{image_id}.jpg"

        upload_dir = Path("uploads/images")
        upload_dir.mkdir(parents=True, exist_ok=True)
        file_path = upload_dir / filename

        try:
            contents = await image.read()
            with open(file_path, 'wb') as f:
                f.write(contents)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Could not save image: {str(e)}"
            )
        finally:
            await image.seek(0)  # Сбрасываем позицию чтения файла

        return image_id, str(file_path)
