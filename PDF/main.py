from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pdf2docx import Converter
import os
import uuid

app = FastAPI()

# 1. ส่วนควบคุมความปลอดภัย (CORS) - อนุญาตให้หน้าเว็บในคอมส่งไฟล์มาได้
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. ฟังก์ชันสำหรับรับไฟล์ PDF และสั่งแปลงเป็น Word
@app.post("/convert")
async def convert_pdf_to_docx(file: UploadFile = File(...)):
    # ตรวจสอบว่าเป็นไฟล์ PDF หรือไม่
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="กรุณาอัปโหลดไฟล์ PDF เท่านั้น")

    # สร้างชื่อไฟล์แบบสุ่มเพื่อป้องกันไฟล์ซ้ำ
    file_id = str(uuid.uuid4())
    pdf_path = f"{file_id}.pdf"
    docx_path = f"{file_id}.docx"

    try:
        # บันทึกไฟล์ PDF ลงในเครื่องชั่วคราว
        with open(pdf_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # สั่งแปลงไฟล์ PDF เป็น Word
        cv = Converter(pdf_path)
        cv.convert(docx_path)
        cv.close()

        # ส่งไฟล์ Word กลับไปให้หน้าเว็บดาวน์โหลด
        return FileResponse(
            path=docx_path, 
            filename=file.filename.replace(".pdf", ".docx"),
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )

    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # ลบไฟล์ PDF ต้นฉบับทิ้งหลังใช้งานเสร็จ (เพื่อประหยัดพื้นที่)
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
