import enum


class ItemCategory(enum.Enum):
    clothes = "Clothes"
    toys = "Toys"
    household = "Household"
    electronics = "Electronics"
    other = "Other"


class ItemStatus(enum.Enum):
    listed = "Listed"  # Нет получателя
    chosen = "Chosen"  # Выбран получатель (не показываем больше в списке)
    closed = "Closed"  # `Сделка прошла`


class ItemDelivery(enum.Enum):
    pickup = "Pickup"
    mail = "Mail"
    owner_delivery = "OwnerDelivery"
