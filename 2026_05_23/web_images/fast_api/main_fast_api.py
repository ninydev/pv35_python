import random
import asyncio
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

# Инициализируем наше приложение.
# Эти данные пойдут в красивую авто-документацию
app = FastAPI(
    title="AI Water Meters API",
    description="Микросервис для распознавания показаний счетчиков воды",
    version="1.0.0"
)


# Симуляция работы нейросети (асинхронная)
async def mock_recognize(file_size: int):
    print(f"[LOG] Анализируем файл размером {file_size} байт...")

    # Имитация задержки обработки моделью YOLO (не блокирует сервер!)
    await asyncio.sleep(random.uniform(0.5, 1.5))

    # 20% шанс, что фотка смазана
    if random.random() < 0.2:
        return {"status": "error", "message": "Зображення занадто розмите для розпізнавання."}

    # 80% успех
    return {
        "status": "success",
        "reading": f"{random.randint(10000, 99999)}",
        "confidence": round(random.uniform(0.70, 0.99), 2),
        "message": "Показання успішно розпізнано"
    }


# Наш роут (эндпоинт), который ждет POST-запрос с файлом
@app.post("/api/v1/recognize", tags=["Recognition"])
async def recognize_meter(image: UploadFile = File(..., description="Фотография счетчика")):
    # Проверка, что нам прислали именно картинку (базовая защита)
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Файл должен быть изображением!")

    # Читаем байты файла
    file_bytes = await image.read()

    # Отправляем в нашу функцию "нейросети"
    result = await mock_recognize(len(file_bytes))

    # Возвращаем красивый JSON (FastAPI сделает это автоматически)
    return JSONResponse(content=result)