from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

API_KEY_3PL = os.getenv("API_KEY_3PL")
URL_3PL_CREATE_SHIPMENT = os.getenv("URL_3PL_CREATE_SHIPMENT")
URL_3PL_UPDATE_SHIPMENT = os.getenv("URL_3PL_UPDATE_SHIPMENT")
URL_3PL_RATING = os.getenv("URL_3PL_RATING")
DAT_API_URL = os.getenv("DAT_API_URL")

HEADERS_3PL = {
    "Authorization": f"Bearer {API_KEY_3PL}",
    "Content-Type": "application/json"
}

class ShipmentInfo(BaseModel):
    someKey: Optional[str] = None

class WebhookRequest(BaseModel):
    lane: str = Field(..., example="NYC-LAX")
    shipmentInfo: Optional[ShipmentInfo] = None

class RatingRequest(BaseModel):
    lane: str = Field(..., example="NYC-LAX")
    weight: Optional[float] = Field(None, example=100.5)

def call_dat_api_simulated(lane: str) -> str:
    print(f"Simulando llamada a DAT API para lane: {lane}")
    return "test-rate-12345"

def create_shipment_3pl(rate_quote_id: str, lane: str) -> str:
    print(f"Simulando creación de shipment con rateQuoteID={rate_quote_id} y lane={lane}")
    return "mock-shipmentId-67890"

def update_shipment_3pl(shipment_id: str, details: Optional[Dict[str, Any]]):
    print(f"Simulando actualización de shipment {shipment_id} con detalles: {details}")

def get_rating_3pl(rating_data: Dict[str, Any]) -> Dict[str, Any]:
    print(f"Simulando consulta de rating 3PL con datos: {rating_data}")
    return {
        "rate": 1500.0,
        "currency": "USD",
        "estimatedDeliveryDays": 3,
        "notes": "Tarifa simulada para pruebas"
    }

@app.post("/webhook-3pl")
async def webhook_3pl(body: WebhookRequest):
    lane = body.lane
    shipment_info = body.shipmentInfo.dict() if body.shipmentInfo else {}

    try:
        rate_quote_id = call_dat_api_simulated(lane)
        print(f"rate_quote_id obtenido: {rate_quote_id}")
    except Exception as e:
        return {"error": f"Error llamando DAT API: {str(e)}"}

    try:
        shipment_id = create_shipment_3pl(rate_quote_id, lane)
        print(f"shipment_id creado: {shipment_id}")
    except Exception as e:
        return {"error": f"Error creando shipment en 3PL: {str(e)}"}

    try:
        update_shipment_3pl(shipment_id, shipment_info)
        print(f"shipment_id actualizado: {shipment_id}")
    except Exception as e:
        return {"error": f"Error actualizando shipment en 3PL: {str(e)}"}

    return {"message": "Envío creado y actualizado correctamente (simulado)", "shipmentId": shipment_id}

@app.post("/rating-3pl")
async def rating_3pl(body: RatingRequest):
    rating_data = body.dict()
    try:
        rating_response = get_rating_3pl(rating_data)
        print(f"rating_response obtenido: {rating_response}")
    except Exception as e:
        return {"error": f"Error consultando rating en 3PL: {str(e)}"}

    return rating_response

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Connection 3PL</title>
        <style>
            body {
                margin: 0;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #1e3c72, #2a5298);
                color: white;
                height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
                padding: 0 20px;
            }
            header {
                position: absolute;
                top: 20px;
                width: 100%;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            header img {
                height: 70px;
                object-fit: contain;
                filter: drop-shadow(0 0 5px rgba(255, 255, 255, 0.8));
            }
            h1 {
                font-size: 3.5rem;
                margin-bottom: 0.5rem;
                font-weight: 900;
                letter-spacing: 2px;
                text-shadow: 0 0 15px rgba(255, 255, 255, 0.6);
            }
            p.subtitle {
                font-size: 1.4rem;
                margin-top: 0;
                margin-bottom: 3rem;
                font-weight: 600;
                color: #d0e7ffcc;
            }
            section {
                background: rgba(255, 255, 255, 0.15);
                border-radius: 15px;
                padding: 20px 30px;
                max-width: 450px;
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
                backdrop-filter: blur(8px);
            }
            button {
                background: #4a90e2;
                color: white;
                border: none;
                padding: 14px 36px;
                font-size: 1.2rem;
                border-radius: 10px;
                cursor: pointer;
                box-shadow: 0 6px 15px rgba(74,144,226,0.5);
                transition: background-color 0.3s ease, transform 0.2s ease;
                font-weight: 700;
                user-select: none;
            }
            button:hover {
                background-color: #357ABD;
                transform: scale(1.05);
            }
            footer {
                margin-top: 40px;
                font-size: 0.9rem;
                color: #b0c4de;
            }
        </style>
    </head>
    <body>
        <header>
            <img src="https://directtrafficsolutions.com/wp-content/uploads/2023/03/Logo-white-font-01-012-6.png" alt="DTS Logo" />
        </header>

        <h1>Bienvenido a API - Connection3PL</h1>
        <p class="subtitle">Esta es una prueba de Integración simple y efectiva Senvíos y tarifas</p>
        <section>
            <h3>Prueba</h3>
            <button onclick="window.open('http://127.0.0.1:8000/docs#/default/webhook_3pl_webhook_3pl_post', '_blank')">Simular</button>
        </section>
        <footer>
            &copy; 2025 Santiago Vélez
        </footer>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
