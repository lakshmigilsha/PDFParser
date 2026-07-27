from fastapi import APIRouter,UploadFile,File,BackgroundTasks
from typing import Annotated
from parser.statementparser import StatementParser
from services.services import StatementService
from pathlib import Path
import tempfile
import shutil
from schemas.pydanticschema import (
    pdfResponse,
    TransactionResponse,
)
from uuid import UUID
 
router=APIRouter()

def save_to_temp_pdf(file: UploadFile) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        shutil.copyfileobj(file.file, temp_pdf)
        return temp_pdf.name
    
def load_extracted_data(temp_path,original_name):
    try:
        #print("Background task started")
        parser = StatementParser(temp_path)
        parsed_result = parser.parse()
        #print("Parsing completed")

        service = StatementService()
        service.save_statement(parsed_result,original_name)
        #print("SAved to database")
    finally:
        Path(temp_path).unlink(missing_ok=True)


@router.post("/pdf/")
async def upload_pdf(
    file: UploadFile,
    background_tasks: BackgroundTasks
):
    if file.content_type != "application/pdf":
        return {"message": "Only PDF files are allowed"}

    temp_path = save_to_temp_pdf(file)

    background_tasks.add_task(
        load_extracted_data,
        temp_path,
        file.filename,
        )

    return {"message": "File uploaded successfully"}

@router.get("/uploaded_pdf_list/",response_model=list[pdfResponse])
async def uploaded_pdf() -> list[pdfResponse]:
    service = StatementService()
    list_pdfs = service.list_uploaded_pdf()
    return list_pdfs

@router.get("/uploaded_pdf_list/{file_id}/transactions/",
            response_model=list[TransactionResponse],
            )
async def uploaded_pdf_transaction(file_id:UUID) -> list[TransactionResponse]:
    service = StatementService()
    list_transactions = service.selected_pdf_transaction(file_id)
    return list_transactions
