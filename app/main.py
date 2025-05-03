from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from opcua import Client, ua
import logging
from datetime import datetime
import random

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OPC-UA configuration
OPC_ADDRESS = "opc.tcp://127.0.0.1:4840"
client = None

# Node Identifiers
NODES = {
    "belt_actual": 'ns=3;s="OPC_Daten"."Istwert Magnertband"',
    "belt_target": 'ns=3;s="OPC_Daten"."Sollwert Magnetband"',
    "drum_actual": 'ns=3;s="OPC_Daten"."Istwert Magnettrommel"',
    "drum_target": 'ns=3;s="OPC_Daten"."Sollwert Magnettrommel"',
    "feeder_actual": 'ns=3;s="OPC_Daten"."Istwert Zuführband"',
    "feeder_target": 'ns=3;s="OPC_Daten"."Sollwert Zuführband"',
}

# PATCH model for speed update
class SpeedUpdate(BaseModel):
    speed: float

def check_opcua_connection():
    global client
    if client is None:
        logging.warning("OPC UA client is None, attempting to reconnect...")
        client = Client(OPC_ADDRESS)
        try:
            client.connect()
            logging.info("Reconnected to OPC-UA Server.")
        except Exception as e:
            # Wenn die Verbindung fehlschlägt, geben wir eine detaillierte Fehlermeldung zurück
            raise HTTPException(status_code=503, detail=f"Failed to connect to OPC UA server: {str(e)}")

    try:
        # Überprüfe, ob der Client eine gültige Verbindung hat, indem wir auf den Serverstatus zugreifen
        client.get_node(ua.ObjectIds.Server_ServerStatus).get_value()
    except Exception as e:
        logging.error("Error during OPC UA connection check: %s", e)
        raise HTTPException(status_code=503, detail="OPC UA server not connected or connection lost.")

# API Startup
@app.on_event("startup")
async def startup_event():
    global client
    logging.info("Initializing OPC-UA Client for address: %s", OPC_ADDRESS)
    client = Client(OPC_ADDRESS)
    try:
        client.connect()
        logging.info("Successfully connected to OPC-UA Server.")
    except Exception as e:
        # Log detailed error for debugging purposes
        logging.error("Connection to OPC-UA server failed: %s", e)
        client = None  # Set client to None if connection fails

# API shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    global client
    if client:
        try:
            client.disconnect()
            logging.info("Disconnected from OPC-UA Server.")
        except Exception as e:
            logging.exception("Error during OPC-UA Client disconnect: %s", e)

# Healthcheck-Endpoint
@app.get("/health")
async def health_check():
    check_opcua_connection()  # Check if the connection is valid
    try:
        # Check if the server's current time can be fetched (just as a simple connectivity check)
        server_time = client.get_node(ua.ObjectIds.Server_ServerStatus_CurrentTime).get_value()
        return {
            "status": "ok",
            "opcua": "connected",
            "server_time": str(server_time)
        }
    except Exception as e:
        logging.warning("Health check failed: %s", e)
        return {"status": "error", "opcua": "connection_failed", "detail": str(e)}

# GET current belt speed
@app.get("/get_speed_belt")
async def get_speed_belt():
    check_opcua_connection()
    try:
        node = client.get_node(NODES["belt_actual"])
        return {"speed": node.get_value()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# PATCH belt speed
@app.patch("/set_speed_belt")
async def set_speed_belt(data: SpeedUpdate):
    check_opcua_connection()
    try:
        node = client.get_node(NODES["belt_target"])
        node.set_value(ua.Variant(data.speed, ua.VariantType.Float))
        return {"message": "Speed updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# GET current drum speed
@app.get("/get_speed_drum")
async def get_speed_drum():
    check_opcua_connection()
    try:
        node = client.get_node(NODES["drum_actual"])
        return {"speed": node.get_value()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# PATCH drum speed
@app.patch("/set_speed_drum")
async def set_speed_drum(data: SpeedUpdate):
    check_opcua_connection()
    try:
        node = client.get_node(NODES["drum_target"])
        node.set_value(ua.Variant(data.speed, ua.VariantType.Float))
        return {"message": "Speed updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# GET current feeder speed
@app.get("/get_speed_feeder")
async def get_speed_feeder():
    check_opcua_connection()
    try:
        node = client.get_node(NODES["feeder_actual"])
        return {"speed": node.get_value()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# PATCH feeder speed
@app.patch("/set_speed_feeder")
async def set_speed_feeder(data: SpeedUpdate):
    check_opcua_connection()
    try:
        node = client.get_node(NODES["feeder_target"])
        node.set_value(ua.Variant(data.speed, ua.VariantType.Float))
        return {"message": "Speed updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
