from fastapi import APIRouter

router = APIRouter()

@router.get("")
async def list_funds():
    return [
        {"id": "fund1", "name": "Второе дыхание", "city": "Москва"},
        {"id": "fund2", "name": "Шанс", "city": "СПб"},
    ]

@router.get("/{fund_id}/locations")
async def get_fund_locations(fund_id: str):
    return [
        {
            "id": "loc1",
            "address": "ул. Красная, д. 1",
            "city": "Москва",
            "working_hours": "9:00 - 18:00",
        }
    ]

@router.post("/{fund_id}/qr-confirm")
async def confirm_transfer(fund_id: str):
    return {"status": "confirmed", "badge": "Волонтер"}