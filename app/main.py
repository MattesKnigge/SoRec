# app/main.py
import logging, asyncio
from fastapi import FastAPI
from opcua import Client
from app.routes import router as api_router

# start with: uvicorn app.main:app --reload

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()

# Global variables
OPC_ADDRESS = "opc.tcp://139.174.27.2:4840"
opc_client = Client(OPC_ADDRESS)

# Initialize global state for routes (this is a simple example; consider better state management for production)
routes_client = opc_client  # Assign the initialized client to your routes

@app.on_event("startup")
async def startup_event():
    logging.info("Starting OPC-UA Client and connecting to %s", OPC_ADDRESS)
    try:
        opc_client.connect()
        logging.info("Successfully connected to OPC-UA Server at: %s", OPC_ADDRESS)
    except Exception as e:
        logging.error("Error connecting to OPC-UA Server: %s", e)

@app.on_event("shutdown")
async def shutdown_event():
    logging.info("Shutting down and disconnecting from OPC-UA Server.")
    try:
        opc_client.disconnect()
        logging.info("Disconnected from OPC-UA Server.")
    except Exception as e:
        logging.error("Error disconnecting from OPC-UA Server: %s", e)

# Include the API routes
app.include_router(api_router)
