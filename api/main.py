from contextlib import asynccontextmanager
import os
from fastapi.responses import RedirectResponse
from fastapi_offline import FastAPIOffline

from data.mqtt import connect, disconnect
from routers import gun, module, system


mqtt_server = os.getenv("MQTT_SERVER")
MQTT_SERVER = mqtt_server if mqtt_server else "localhost"


@asynccontextmanager
async def lifespan(_):
    connect(MQTT_SERVER)
    yield
    disconnect()


app = FastAPIOffline(
    lifespan=lifespan,
    swagger_ui_parameters={"tryItOutEnabled": True}
)
app.title = "Colat laser game API"
app.version = "0.42.2"
app.include_router(system.router)
app.include_router(module.router)
app.include_router(gun.router)


@app.get("/", include_in_schema=False)
def redirect_docs():
    return RedirectResponse("/docs")
