from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pdf2docx import Converter
import os
import shutil

app = FastAPI()

# อนุญาตให้หน้าเว็บ (Frontend) ติดต่อกับ Backend ได้
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/convert")
async def convert_pdf_to_docx(file: UploadFile = File(...)):
    pdf_path = f"temp_{file.filename}"
    docx_path = pdf_path.replace(".pdf", ".docx")
    
    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # แปลงไฟล์
    cv = Converter(pdf_path)
    cv.convert(docx_path)
    cv.close()

    os.remove(pdf_path) # ลบ PDF ทิ้งหลังแปลงเสร็จ
    return FileResponse(docx_path, filename=f"converted_{docx_path}")
