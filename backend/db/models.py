from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Customer(BaseModel):
    id: str  
    name: str
    email: str
    purchased_product: str
    date_of_purchase: str  # ISO format YYYY-MM-DD
    phone: Optional[str] = None
    address: Optional[str] = None


class Ticket(BaseModel):
    ticket_id: str
    email: str
    product: str
    issue: str
    status: str = "open"
    priority: str = "normal"
    created_at: datetime

class TicketRequest(BaseModel):
    customer_id: str
    issue: str
    priority: Optional[str] = "normal"
