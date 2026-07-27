from pydantic import BaseModel
from datetime import datetime
import uuid

class pdfResponse(BaseModel):
    file_id: uuid.UUID
    cust_id: int
    original_name: str
    status: str
    uploaded_at: datetime