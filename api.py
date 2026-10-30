import shutil
import tempfile
from fastapi import FastAPI, File, UploadFile
from analyzer import analyze_video  # імпортуємо твою функцію з analyzer.py

app = FastAPI(title="OctarCore AI Service")


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    # Зберігаємо завантажене відео у тимчасовий файл
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=".mp4"
    ) as temp_video:
        shutil.copyfileobj(file.file, temp_video)
        temp_path = temp_video.name

    # Проганяємо відео через твій аналізатор
    result_data = analyze_video(temp_path)

    # Повертаємо готовий JSON
    return result_data