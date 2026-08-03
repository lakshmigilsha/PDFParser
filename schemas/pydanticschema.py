from pydantic import BaseModel
from datetime import datetime, date
from decimal import Decimal
import uuid

class pdfResponse(BaseModel):
    file_id: uuid.UUID
    original_name: str
    status: str
    uploaded_at: datetime
    error_message: str|None=None

class TransactionResponse(BaseModel):
    date: date
    particulars:str
    balance:Decimal
    mode: str|None=None
    deposits:Decimal|None=None
    withdrawals:Decimal|None=None

class CustomerResponse(BaseModel):
    name:str
    address:str
    cust_id:int
    date:date
    account_number:int

class AccountResponse(BaseModel):
    account_type:str
    ac_balance:Decimal
    fixed_deposits_linked_balance:Decimal
    total_balance:Decimal
    nomination:str

class PointsResponse(BaseModel):
    savings_acc_number:int
    linked_payback_number:int
    savings_reward:int
    debit_card:int
    points_balance:int

class OtherResponse(BaseModel):
    account_type:str
    account_number:int
    micr_code:int
    ifsc_code:str
    nominee:str  