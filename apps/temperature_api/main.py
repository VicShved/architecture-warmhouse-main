import random
import datetime as dt
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Temperature API",
    description="Эмулятор удалённого датчика температуры",
    version="0.0.1",
)

# Дефолтный маппинг location <-> sensor_id (как в задании)
LOCATION_TO_SENSOR_ID = {
    "living room": "1",
    "bedroom": "2",
    "kitchen": "3",
}
SENSOR_ID_TO_LOCATION = {v: k for k, v in LOCATION_TO_SENSOR_ID.items()}


class TemperatureResponse(BaseModel):
    value: float
    unit: str = "°C"
    timestamp: dt.datetime
    location: str
    status: str = "ok"
    sensor_id: str
    sensor_type: str = "temperature"
    description: str


def random_temperature() -> float:
    return round(random.uniform(10.0, 30.0), 1)


def build_response(location: str, sensor_id: str) -> TemperatureResponse:
    return TemperatureResponse(
        value=random_temperature(),
        timestamp=dt.datetime.now(dt.timezone.utc),
        location=location,
        sensor_id=sensor_id,
        description=f"Температура в локации {location}",
    )


@app.get("/temperature", response_model=TemperatureResponse)
def get_temperature(
    location: Optional[str] = None,
    sensorId: Optional[str] = None,
) -> TemperatureResponse:
    norm = (location or "").strip().lower()

    # Если location нет — берём по sensorId
    if location is None or location == "":
        if sensorId is None or sensorId == "":
            location = "Unknown"
        else:
            location = SENSOR_ID_TO_LOCATION.get(sensorId, "Unknown")
    else:
        # Если sensorId нет — подставляем по location
        if sensorId is None or sensorId == "":
            sensorId = LOCATION_TO_SENSOR_ID.get(norm, "0")

    return build_response(location, sensorId or "0")


@app.get("/temperature/{sensor_id}", response_model=TemperatureResponse)
def get_temperature_by_id(sensor_id: str) -> TemperatureResponse:
    location = SENSOR_ID_TO_LOCATION.get(sensor_id, "Unknown")
    return build_response(location, sensor_id)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
