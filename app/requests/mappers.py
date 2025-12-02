import uuid

from app.items.enums import ItemStatus, ItemDelivery
from app.requests.models import RequestBase, RequestDeliveryTypeBase
from app.requests.schemas import Request
from app.requests.schemas import RequestResponse


# noinspection PyPep8Naming
def Requests_to_RequestBase(request: Request,
                            user_id: uuid.UUID,
                            request_id: uuid.UUID | None = None,
                            status: ItemStatus = ItemStatus.listed
                            ) -> RequestBase:
    return RequestBase(
        id=request_id,
        user_id=user_id,
        text=request.text,
        location=request.location,
        category=request.category,
        status=status,
    )


# noinspection PyPep8Naming
def RequestBase_to_RequestResponse(request_base: RequestBase, organization_name: str | None) -> RequestResponse:
    return RequestResponse(
        id=request_base.id,
        user_id=request_base.user_id,
        text=request_base.text,
        location=request_base.location,
        category=request_base.category,
        delivery_types=deliveries_bases_to_deliveries(request_base.delivery_bases),
        organization_name=organization_name
    )


# noinspection PyPep8Naming
def RequestDelivery_to_RequestDeliveryTypeBase(
        delivery: ItemDelivery,
        request_id: uuid.UUID,
        id: uuid.UUID | None = None,
) -> RequestDeliveryTypeBase:
    return RequestDeliveryTypeBase(
        id=id,
        request_id=request_id,
        delivery_type=delivery
    )


def deliveries_bases_to_deliveries(delivery_bases: list[RequestDeliveryTypeBase]) -> list[ItemDelivery]:
    return [request_base.delivery_type for request_base in delivery_bases]
