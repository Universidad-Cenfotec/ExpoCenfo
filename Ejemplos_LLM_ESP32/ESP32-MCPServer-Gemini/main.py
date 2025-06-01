from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

API_KEY = "TU_API_KEY_DE_GEMINI"
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

TEMPLATE = """
Temperatura: {temperature}°C
Humedad relativa: {humidity}%

Genera una melodía breve en formato "nota,duración,nota,duración,...", usando notas musicales estándar (C3 a C6 y R para silencios). Ideal para expresar el estado ambiental de una planta.
"""

class ContextData(BaseModel):
    location: str
    plant_type: str
    soil_moisture: float
    temperature: float
    humidity: float

@app.post("/consulta")
def consulta(data: ContextData):
    prompt = TEMPLATE.format(**data.dict())
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 100}
    }
    headers = {"Content-Type": "application/json"}
    r = requests.post(ENDPOINT, headers=headers, json=payload)

    if r.status_code == 200:
        text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
        return {"respuesta": text}
    else:
        return {"error": r.text}
