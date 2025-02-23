# app/routes.py
import logging, asyncio
from fastapi import APIRouter, HTTPException
from app.models import SpeedInput
from app.utils import update_opc_node, monitor_speed_belt

router = APIRouter()

monitor_task = None

# You might also consider using dependency injection to pass the OPC-UA client.
client = None  # This should be initialized in main.py and passed to your route functions.
previous_speed_belt = [None]  # Using a list to hold mutable state

@router.post("/startBeltSpeedMonitor")
async def start_monitor():
    global monitor_task
    if monitor_task is None or monitor_task.cancelled():
        monitor_task = asyncio.create_task(monitor_speed_belt(client, previous_speed_belt))
        logging.info("Monitor task started.")
        return {"message": "Monitor started"}
    else:
        return {"message": "Monitor is already running"}

@router.post("/stopBeltSpeedMonitor")
async def stop_monitor():
    global monitor_task
    if monitor_task is not None:
        monitor_task.cancel()
        try:
            await monitor_task
        except asyncio.CancelledError:
            logging.info("Monitor task cancelled via endpoint.")
        monitor_task = None
        return {"message": "Monitor stopped"}
    else:
        return {"message": "Monitor is not running"}

@router.post("/machineOn")
async def machine_on():
    logging.info("POST /machineOn endpoint called")
    return {"message": "Machine on endpoint - TODO: implement logic"}

@router.post("/machineOff")
async def machine_off():
    logging.info("POST /machineOff endpoint called")
    return {"message": "Machine off endpoint - TODO: implement logic"}

@router.post("/stop")
async def stop_all():
    logging.info("POST /stop endpoint called. Setting all speeds to 0.")
    drum_response = update_opc_node(client, 'ns=3;s="OPC_Daten"."Sollwert Magnettrommel"', 0)
    belt_response = update_opc_node(client, 'ns=3;s="OPC_Daten"."Sollwert Magnetband"', 0)
    feeder_response = update_opc_node(client, 'ns=3;s="OPC_Daten"."Sollwert Zuführband"', 0)
    return {
        "message": "All machine speeds have been set to 0.",
        "details": {
            "drum": drum_response,
            "belt": belt_response,
            "feeder": feeder_response
        }
    }

@router.get("/speedOfBelt")
async def get_speed_belt():
    logging.info("GET /speedOfBelt endpoint called")
    try:
        node = client.get_node('ns=3;s="OPC_Daten"."Istwert Magnertband"')
        speed_of_belt = node.get_value()
        logging.info("Retrieved conveyor belt speed: %s", speed_of_belt)
        return {"speedOfBelt": speed_of_belt}
    except Exception as e:
        logging.error("Error reading conveyor belt speed: %s", e)
        raise HTTPException(status_code=500, detail=f"Error reading speed: {e}")

@router.get("/speedOfDrum")
async def get_speed_drum():
    logging.info("GET /speedOfDrum endpoint called")
    try:
        node = client.get_node('ns=3;s="OPC_Daten"."Istwert Magnettrommel"')
        speed_of_drum = node.get_value()
        logging.info("Retrieved magnetic drum speed: %s", speed_of_drum)
        return {"speedOfDrum": speed_of_drum}
    except Exception as e:
        logging.error("Error reading magnetic drum speed: %s", e)
        raise HTTPException(status_code=500, detail=f"Error reading speed: {e}")

@router.get("/speedOfFeeder")
async def get_speed_feeder():
    logging.info("GET /speedOfFeeder endpoint called")
    try:
        node = client.get_node('ns=3;s="OPC_Daten"."Istwert Zuführband"')
        speed_of_feeder = node.get_value()
        logging.info("Retrieved feeder speed: %s", speed_of_feeder)
        return {"speedOfFeeder": speed_of_feeder}
    except Exception as e:
        logging.error("Error reading feeder speed: %s", e)
        raise HTTPException(status_code=500, detail=f"Error reading speed: {e}")

@router.patch("/speedOfDrum")
async def set_speed_drum(speed_input: SpeedInput):
    logging.info("PATCH /speedOfDrum endpoint called with payload: %s", speed_input)
    return update_opc_node(client, 'ns=3;s="OPC_Daten"."Sollwert Magnettrommel"', speed_input.speed)

@router.patch("/speedOfBelt")
async def set_speed_belt(speed_input: SpeedInput):
    logging.info("PATCH /speedOfBelt endpoint called with payload: %s", speed_input)
    return update_opc_node(client, 'ns=3;s="OPC_Daten"."Sollwert Magnetband"', speed_input.speed)

@router.patch("/speedOfFeeder")
async def set_speed_feeder(speed_input: SpeedInput):
    logging.info("PATCH /speedOfFeeder endpoint called with payload: %s", speed_input)
    return update_opc_node(client, 'ns=3;s="OPC_Daten"."Sollwert Zuführband"', speed_input.speed)
