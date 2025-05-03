from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .opcua import init_opcua_client, shutdown_opcua_client, NODES, client
from .models import SpeedUpdate
from .utils import check_connection_and_handle_error
import logging

# FastAPI-Setup
app = FastAPI()

# CORS-Konfiguration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Startup
@app.on_event("startup")
async def startup_event():
    init_opcua_client()

# API Shutdown
@app.on_event("shutdown")
async def shutdown_event():
    shutdown_opcua_client()

# Healthcheck-Endpoint
@app.get("/health")
async def health_check():
    check_connection_and_handle_error()

    # Serverzeit abrufen
    try:
        server_time = client.get_node("ns=0;i=2258").get_value()
        return {"status": "ok", "server_time": str(server_time)}
    except Exception as e:
        logging.warning("Health check failed: %s", e)
        return {"status": "error", "opcua": "connection_failed", "detail": "Connection failed during health check."}

# GET und PATCH Endpoints für die Geschwindigkeit

# GET current belt speed
@app.get("/get_speed_belt")
async def get_speed_belt():
    check_connection_and_handle_error()
    try:
        node = client.get_node(NODES["belt_actual"])
        return {"speed": node.get_value()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# PATCH belt speed
@app.patch("/set_speed_belt")
async def set_speed_belt(data: SpeedUpdate):
    check_connection_and_handle_error()
    try:
        node = client.get_node(NODES["belt_target"])
        node.set_value(data.speed)
        return {"message": "Speed updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# GET current drum speed
@app.get("/get_speed_drum")
async def get_speed_drum():
    check_connection_and_handle_error()
    try:
        node = client.get_node(NODES["drum_actual"])
        return {"speed": node.get_value()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# PATCH drum speed
@app.patch("/set_speed_drum")
async def set_speed_drum(data: SpeedUpdate):
    check_connection_and_handle_error()
    try:
        node = client.get_node(NODES["drum_target"])
        node.set_value(data.speed)
        return {"message": "Speed updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# GET current feeder speed
@app.get("/get_speed_feeder")
async def get_speed_feeder():
    check_connection_and_handle_error()
    try:
        node = client.get_node(NODES["feeder_actual"])
        return {"speed": node.get_value()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# PATCH feeder speed
@app.patch("/set_speed_feeder")
async def set_speed_feeder(data: SpeedUpdate):
    check_connection_and_handle_error()
    try:
        node = client.get_node(NODES["feeder_target"])
        node.set_value(data.speed)
        return {"message": "Speed updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# GET current drum speed
@app.get("/get_speed_drum")
async def get_speed_drum():
    check_connection_and_handle_error()
    try:
        node = client.get_node(NODES["drum_actual"])
        return {"speed": node.get_value()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# PATCH drum speed
@app.patch("/set_speed_drum")
async def set_speed_drum(data: SpeedUpdate):
    check_connection_and_handle_error()
    try:
        node = client.get_node(NODES["drum_target"])
        node.set_value(data.speed)
        return {"message": "Speed updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
