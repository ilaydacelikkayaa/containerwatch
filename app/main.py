from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import redis

app = FastAPI()
instrumentator = Instrumentator()
instrumentator.instrument(app)  # ölçüm yap.

redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True,  # redis'ten gelen verileri Python'da okunabilir str biçimine dönüştür
)


@app.get("/")
def root():
    return {"message": "ContainerWatch API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/visit")
def visit():
    new_count = redis_client.incr("visit_count")
    return {"visits": new_count}


instrumentator.expose(app)  # Ölçümleri /metrics adresinde sun.
