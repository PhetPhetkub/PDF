from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pdf2docx import Converter
import os
import shutil

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

# ... (บรรทัด app = FastAPI() ของคุณจะอยู่ตรงนี้) ...

# ก๊อปปี้ก้อนนี้ไปวางต่อท้ายเลยครับ
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
