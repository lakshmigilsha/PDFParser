from fastapi import APIRouter,UploadFile,File
from typing import Annotated
 
router=APIRouter()

@router.post("/pdf/")
async def upload_pdf(file: list[UploadFile]=File(...)):
    if file.content_type == "application/pdf":
        return {"file":file.file}
    return{"message":"Upload file in pdf format"}
