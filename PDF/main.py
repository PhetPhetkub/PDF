from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pdf2docx import Converter
import os
import uuid

app = FastAPI()

# 1. ระบบจัดการความปลอดภัย (CORS) - แก้ปัญหาที่หน้าเว็บฟ้อง Error สีส้ม
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. ฟังก์ชันหลักสำหรับแปลงไฟล์ PDF เป็น Word
@app.post("/convert")
async function convert_pdf_to_docx(file: UploadFile = File(...)):
    # ตรวจสอบว่าเป็นไฟล์ PDF หรือไม่
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="ขอเป็นไฟล์ PDF เท่านั้นครับ")

    # สร้างชื่อไฟล์สุ่มเพื่อไม่ให้ชื่อซ้ำกัน
    file_id = str(uuid.uuid4())
    pdf_path = f"{file_id}.pdf"
    docx_path = f"{file_id}.docx"

    try:
        # บันทึกไฟล์ PDF ที่รับมาลงเครื่องชั่วคราว
        with open(pdf_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # เริ่มต้นการแปลงไฟล์ด้วย pdf2docx
        cv = Converter(pdf_path)
        cv.convert(docx_path)
        cv.close()

        # ส่งไฟล์ Word กลับไปให้ผู้ใช้ดาวน์โหลด
        return FileResponse(
            path=docx_path, 
            filename=file.filename.replace(".pdf", ".docx"),
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    # หมายเหตุ: ในระบบฟรี ไฟล์ชั่วคราวจะถูกลบเมื่อมีการเริ่ม Deploy ใหม่
