from pydantic import BaseModel
from datetime import datetime, date
from decimal import Decimal
import uuid

class pdfResponse(BaseModel):
    file_id: uuid.UUID
    cust_id: int
    original_name: str
    status: str
    uploaded_at: datetime

class TransactionResponse(BaseModel):
    date: date
    particulars:str
    balance:Decimal
    mode: str|None=None
    deposits:Decimal|None=None
    withdrawals:Decimal|None=None