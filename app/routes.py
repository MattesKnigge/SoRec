import logging, asyncio
from fastapi import APIRouter, HTTPException
from app.models import SpeedInput
from app.utils import update_opc_node, monitor_speed_belt

router = APIRouter()

monitor_task = None
client = None
previous_speed_belt = [None]

@router.patch("/startBeltSpeedMonitor", tags=["Belt Speed Monitoring"], summary="Start Belt Speed Monitor", description="Starts monitoring the speed of the conveyor belt.")
async def start_monitor():
    global monitor_task
    if not client:
        logging.error("OPC-UA client is not connected.")
        raise HTTPException(status_code=503, detail="OPC-UA client is not connected.")
    if monitor_task is None or monitor_task.cancelled():
        monitor_task = asyncio.create_task(monitor_speed_belt(client, previous_speed_belt))
        logging.info("Monitor task started.")
        return {"message": "Monitor started"}
    else:
        logging.info("Monitor is already running.")
        return {"message": "Monitor is already running"}

@router.patch("/stopBeltSpeedMonitor", tags=["Belt Speed Monitoring"], summary="Stop Belt Speed Monitor", description="Stops the conveyor belt speed monitoring task.")
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

@router.patch("/machineOn", tags=["Machine Control"], summary="Turn Machine On", description="Turns the machine on. (Placeholder – logic needs to be implemented.)")
async def machine_on():
    logging.info("patch /machineOn endpoint called")
    return {"message": "Machine on endpoint - TODO: implement logic"}

@router.patch("/machineOff", tags=["Machine Control"], summary="Turn Machine Off", description="Turns the machine off. (Placeholder – logic needs to be implemented.)")
async def machine_off():
    logging.info("patch /machineOff endpoint called")
    return {"message": "Machine off endpoint - TODO: implement logic"}

@router.patch("/stop", tags=["Machine Control"], summary="Stop All Machine Components", description="Stops all machine components by setting the speed of the drum, belt, and feeder to 0.")
async def stop_all():
    logging.info("PATCH /stop endpoint called. Initiating stop sequence for all machine components.")

    results = {}

    try:
        logging.info("Attempting to set drum speed to 0.")
        drum_response = update_opc_node(client, 'ns=3;s="OPC_Daten"."Sollwert Magnettrommel"', 0)
        results["drum"] = drum_response
        logging.info("Drum speed successfully set to 0. Response: %s", drum_response)
    except Exception as e:
        error_msg = f"Error: {e}"
        results["drum"] = error_msg
        logging.error(error_msg)
    try:
        logging.info("Attempting to set belt speed to 0.")
        belt_response = update_opc_node(client, 'ns=3;s="OPC_Daten"."Sollwert Magnetband"', 0)
        results["belt"] = belt_response
        logging.info("Belt speed successfully set to 0. Response: %s", belt_response)
    except Exception as e:
        error_msg = f"Error: {e}"
        results["belt"] = error_msg
        logging.error(error_msg)
    try:
        logging.info("Attempting to set feeder speed to 0.")
        feeder_response = update_opc_node(client, 'ns=3;s="OPC_Daten"."Sollwert Zuführband"', 0)
        results["feeder"] = feeder_response
        logging.info("Feeder speed successfully set to 0. Response: %s", feeder_response)
    except Exception as e:
        error_msg = f"Error: {e}"
        results["feeder"] = error_msg
        logging.error(error_msg)

    logging.info("Stop sequence completed. Final results: %s", results)
    return {
        "message": "Stop sequence completed. Check details for each machine component.",
        "details": results
    }

@router.get("/speedOfBelt", tags=["Speed Monitoring"], summary="Get Belt Speed", description="Retrieves the current speed of the conveyor belt in %.")
async def get_speed_belt():
    logging.info("GET /speedOfBelt endpoint called")
    if not client:
        logging.error("OPC-UA client is not connected.")
        raise HTTPException(status_code=503, detail="OPC-UA client is not connected.")
    try:
        node = client.get_node('ns=3;s="OPC_Daten"."Istwert Magnertband"')
        speed_of_belt = node.get_value()
        logging.info("Retrieved conveyor belt speed: %s", speed_of_belt)
        return {"speedOfBelt": speed_of_belt}
    except Exception as e:
        logging.error("Error reading conveyor belt speed: %s", e)
        raise HTTPException(status_code=500, detail=f"Error reading speed: {e}")

@router.get("/speedOfDrum", tags=["Speed Monitoring"], summary="Get Drum Speed", description="Retrieves the current speed of the magnetic drum in %.")
async def get_speed_drum():
    logging.info("GET /speedOfDrum endpoint called")
    if not client:
        logging.error("OPC-UA client is not connected.")
        raise HTTPException(status_code=503, detail="OPC-UA client is not connected.")
    try:
        node = client.get_node('ns=3;s="OPC_Daten"."Istwert Magnettrommel"')
        speed_of_drum = node.get_value()
        logging.info("Retrieved magnetic drum speed: %s", speed_of_drum)
        return {"speedOfDrum": speed_of_drum}
    except Exception as e:
        logging.error("Error reading magnetic drum speed: %s", e)
        raise HTTPException(status_code=500, detail=f"Error reading speed: {e}")

@router.get("/speedOfFeeder", tags=["Speed Monitoring"], summary="Get Feeder Speed", description="Retrieves the current speed of the feeder in %.")
async def get_speed_feeder():
    logging.info("GET /speedOfFeeder endpoint called")
    if not client:
        logging.error("OPC-UA client is not connected.")
        raise HTTPException(status_code=503, detail="OPC-UA client is not connected.")
    try:
        node = client.get_node('ns=3;s="OPC_Daten"."Istwert Zuführband"')
        speed_of_feeder = node.get_value()
        logging.info("Retrieved feeder speed: %s", speed_of_feeder)
        return {"speedOfFeeder": speed_of_feeder}
    except Exception as e:
        logging.error("Error reading feeder speed: %s", e)
        raise HTTPException(status_code=500, detail=f"Error reading speed: {e}")

@router.patch("/speedOfDrum", tags=["Speed Control"], summary="Set Drum Speed", description="Sets the speed of the magnetic drum.")
async def set_speed_drum(speed_input: SpeedInput):
    logging.info("PATCH /speedOfDrum endpoint called with payload: %s", speed_input)
    return update_opc_node(client, 'ns=3;s="OPC_Daten"."Sollwert Magnettrommel"', speed_input.speed)

@router.patch("/speedOfBelt", tags=["Speed Control"], summary="Set Belt Speed", description="Sets the speed of the conveyor belt.")
async def set_speed_belt(speed_input: SpeedInput):
    logging.info("PATCH /speedOfBelt endpoint called with payload: %s", speed_input)
    return update_opc_node(client, 'ns=3;s="OPC_Daten"."Sollwert Magnetband"', speed_input.speed)

@router.patch("/speedOfFeeder", tags=["Speed Control"], summary="Set Feeder Speed", description="Sets the speed of the feeder.")
async def set_speed_feeder(speed_input: SpeedInput):
    logging.info("PATCH /speedOfFeeder endpoint called with payload: %s", speed_input)
    return update_opc_node(client, 'ns=3;s="OPC_Daten"."Sollwert Zuführband"', speed_input.speed)
