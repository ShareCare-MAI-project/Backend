import uuid
from pathlib import Path
from uuid import UUID

import uuid_utils
from fastapi import UploadFile, HTTPException
from sqlalchemy import or_, and_, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from app.items.cruds.item_crud import ItemCrud
from app.items.cruds.item_delivery_crud import ItemDeliveryCrud
from app.items.cruds.item_image_crud import ItemImageCrud
from app.items.enums import ItemStatus
from app.items.mappers import ItemBase_to_ItemResponse, ItemRequest_to_ItemBase, ItemDelivery_to_ItemDeliveryTypeBase
from app.items.mappers import ItemBase_to_TransactionResponse
from app.items.models import ItemImageBase, ItemBase
from app.items.schemas import ItemCreateRequest
from app.items.schemas import ItemQuickInfoResponse
from app.items.schemas import ItemResponse, Item
from app.items.schemas import TransactionResponse
from app.requests.cruds.request_crud import RequestCrud
from app.utils.consts import SUCCESS_RESPONSE
from app.user.user_base import UserBase


class ItemsService:
    acceptance = dict()

    @staticmethod
    async def get_item_quick_info(db: AsyncSession, item_id: uuid.UUID, user_id: uuid.UUID) -> ItemQuickInfoResponse:
        item = await ItemCrud.get_item(db, item_id)

        if not item:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Товар не найден")

        item: ItemBase = item
        show_owner = item.status == ItemStatus.listed or item.owner_id != user_id

        to_show_id = item.owner_id if show_owner else item.recipient_id

        # noinspection PyTypeChecker
        user = await UserBase.get_by_id(to_show_id, db)

        opponent_donated = db.scalar(
            select(func.count(ItemBase.id)).where(and_(
                ItemBase.owner_id == user.id,
                ItemBase.status == ItemStatus.closed
            ))
        )

        opponent_received = db.scalar(
            select(func.count(ItemBase.id)).where(and_(
                ItemBase.recipient_id == user.id,
                ItemBase.status == ItemStatus.closed
            ))
        )
        # noinspection PyTypeChecker
        return ItemQuickInfoResponse(
            status=item.status,
            opponent_id=user.id,
            opponent_name=user.name,
            opponent_is_verified=user.is_verified,
            opponent_organization_name=user.organization_name,
            opponent_donated=(await opponent_donated) or 0,
            opponent_received=(await opponent_received) or 0
        )

    @staticmethod
    async def accept_item(db: AsyncSession, item_id: uuid.UUID, user_id: uuid.UUID):
        item = await ItemCrud.get_item(db, item_id)

        if user_id not in [item.recipient_id, item.owner_id]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Вы не можете принять")

        if item.status != ItemStatus.chosen:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Невозможно принять")

        acceptance = ItemsService.acceptance.setdefault(item_id, set())
        acceptance.add(user_id)
        if len(ItemsService.acceptance[item_id]) > 1:
            request_base = (await RequestCrud.get_request(db, item.request_id)) if item.request_id else None

            if request_base:
                request_base.status = ItemStatus.closed
            item.status = ItemStatus.closed

            await ItemCrud.update_item(db, new_item=item)

            await db.commit()

            if request_base:
                await db.refresh(request_base)

            await db.flush(item)
            ItemsService.acceptance.pop(item_id)

        return SUCCESS_RESPONSE

    @staticmethod
    async def deny_item(db: AsyncSession, item_id: uuid.UUID, user_id: uuid.UUID):
        item = await ItemCrud.get_item(db, item_id)

        if user_id not in [item.recipient_id, item.owner_id]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Вы не можете отменить")

        if item.status != ItemStatus.chosen:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Невозможно отменить")

        request_base = (await RequestCrud.get_request(db, item.request_id)) if item.request_id else None

        if request_base:
            request_base.status = ItemStatus.listed
        item.status = ItemStatus.listed
        item.recipient_id = None
        item.request_id = None

        await ItemCrud.update_item(db, new_item=item)

        await db.commit()

        if request_base:
            await db.refresh(request_base)

        await db.flush(item)
        return SUCCESS_RESPONSE

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
    async def create_item(db: AsyncSession, item: ItemCreateRequest, images: list[UploadFile], owner_id: uuid.UUID):
        request_base = await RequestCrud.get_request(db, item.request_id) if item.request_id is not None else None

        if request_base and request_base.status != ItemStatus.listed:
            raise HTTPException(status_code=HTTP_409_CONFLICT, detail="На заявку уже откликнулись!")

        recipient_id = request_base.user_id if request_base is not None else None

        item_status = ItemStatus.chosen if recipient_id else ItemStatus.listed

        item_base = ItemRequest_to_ItemBase(item=item, owner_id=owner_id, recipient_id=recipient_id, status=item_status)

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

        if request_base:
            request_base.status = ItemStatus.chosen

        await db.commit()
        await db.refresh(item_base)

        if request_base:
            await db.refresh(request_base)

        return SUCCESS_RESPONSE

    @staticmethod
    async def delete_item(db: AsyncSession, item_id: uuid.UUID, user_id: uuid.UUID):

        item_base = await ItemCrud.get_item(db, item_id=item_id)

        if user_id != item_base.owner_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет прав")

        await db.delete(item_base)
        await ItemDeliveryCrud.delete(db, item_id=item_id)
        await ItemImageCrud.delete(db, item_id=item_id)
        jobs = []
        for image_base in item_base.image_bases:
            jobs.append(ItemsService.delete_image(Path(image_base.image)))

        for i in jobs:
            await i

        await db.commit()

    @staticmethod
    async def edit_item(db: AsyncSession, item: Item, item_id: uuid.UUID, user_id: uuid.UUID):
        item_base = await ItemCrud.get_item(db, item_id=item_id)

        if user_id != item_base.owner_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет прав")

        # is there better way?
        item_base.title = item.title
        item_base.description = item.description
        item_base.category = item.category
        item_base.location = item.location

        await db.merge(item_base)

        await ItemDeliveryCrud.delete(db, item_id=item_id)
        await db.flush()

        to_await = []
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
    async def fetch_transactions(db: AsyncSession, user_id: uuid.UUID) -> list[TransactionResponse]:
        items = await ItemCrud.get_filtered_items(db,
                                                  and_(
                                                      or_(ItemBase.owner_id == user_id,
                                                          ItemBase.recipient_id == user_id),
                                                      ItemBase.status == ItemStatus.closed
                                                  )
                                                  )
        return [ItemBase_to_TransactionResponse(item, user_id) for item in items]

    @staticmethod
    async def delete_image(image: Path):
        print(image.exists())  # TODO

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
            await image.seek(0)

        return image_id, str(file_path)
