import uuid
from datetime import datetime, timedelta

items = {}
requests_to_items = {}

def create_item(data: dict, donor_id: str) -> dict:
    item_id = str(uuid.uuid4())
    item = data.copy()
    item.update({
        "id": item_id,
        "donor_id": donor_id,
        "status": "available",
        "created_at": datetime.utcnow().isoformat(),
        "requests": [],
    })
    items[item_id] = item
    return item

def get_item(item_id: str):
    return items.get(item_id)

def list_items(category: str = None):
    result = list(items.values())
    if category:
        result = [i for i in result if i.get("category") == category]
    return result

def create_request_for_item(item_id: str, requester_name: str, requester_telegram: str):
    if item_id not in items:
        return None
    
    request_id = str(uuid.uuid4())
    request_record = {
        "id": request_id,
        "item_id": item_id,
        "requester_name": requester_name,
        "requester_telegram": requester_telegram,
        "created_at": datetime.utcnow().isoformat(),
        "status": "pending"
    }
    
    requests_to_items[request_id] = request_record
    items[item_id]["requests"].append(request_record)
    return request_record

def get_item_requests(item_id: str):
    if item_id not in items:
        return None
    return items[item_id]["requests"]

def approve_request(item_id: str, request_id: str):
    if item_id not in items:
        return None
    if request_id not in requests_to_items:
        return None
    
    item = items[item_id]
    request_record = requests_to_items[request_id]
    
    item["status"] = "given"
    request_record["status"] = "accepted"
    
    for req in item["requests"]:
        if req["id"] != request_id and req["status"] == "pending":
            req["status"] = "rejected"
    
    return request_record

def count_items_this_month(items_list: list) -> int:
    now = datetime.utcnow()
    month_ago = now - timedelta(days=30)
    
    count = 0
    for date_str in items_list:
        try:
            date = datetime.fromisoformat(date_str)
            if date >= month_ago:
                count += 1
        except:
            pass
    return count