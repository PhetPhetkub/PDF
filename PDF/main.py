from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pdf2docx import Converter
import os
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# กลับมาใช้ชื่อเส้นทาง /convert เหมือนเดิม
@app.post("/convert")
async def convert_pdf(file: UploadFile = File(...)):
    pdf_path = f"{uuid.uuid4()}.pdf"
    docx_path = f"{uuid.uuid4()}.docx"
    
    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    try:
        # แปลงไฟล์ PDF เป็น Word อย่างไว
        cv = Converter(pdf_path)
        cv.convert(docx_path)
        cv.close()

        return FileResponse(
            docx_path, 
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document', 
            filename="Converted_Document.docx"
        )
    finally:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
