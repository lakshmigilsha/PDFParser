from fastapi import APIRouter,UploadFile,File,BackgroundTasks
from typing import Annotated
from parser import statementparser 
 
router=APIRouter()

def load_extracted_data(file):
    parser = statementparser.StatementParser(file)

    result = parser.parse()


@router.post("/pdf/")
async def upload_pdf(file: UploadFile,background_tasks: BackgroundTasks):
    if file.content_type == "application/pdf":
        background_tasks.add_task(load_extracted_data,file)
    return{"message":"Upload file in pdf format"}
