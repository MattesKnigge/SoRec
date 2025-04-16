from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from opcua import Client, ua
import logging

# ------------------------------------------------------------
# To run the FastAPI application, use the following command:
# uvicorn app.main:app --reload
# ------------------------------------------------------------

# Configure logging to display the timestamp, log level, and message.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize the FastAPI application.
app = FastAPI()

# Global OPC-UA client variable.
client = None

# OPC-UA server address for the machine.
# Machine IP: 139.174.27.2:4840
OPC_ADDRESS = "opc.tcp://139.174.27.2:4840"


# ------------------------------
# Data Models
# ------------------------------

class SpeedInput(BaseModel):
    """
    Data model for speed input from the user.

    Attributes:
        speed (float): The speed value to set (must be between 0 and 100).
    """
    speed: float

    @validator('speed')
    def validate_speed(cls, value):
        if value > 100:
            raise ValueError("Speeds above 100% are not allowed!")
        if value < 0:
            raise ValueError("Speeds below 0% are not allowed!")
        return value


# The following models are defined for potential future use with batch operations.
class Operation(BaseModel):
    """
    Data model for a single operation in a patch request.

    Attributes:
        path (str): The node path to modify.
        value (float): The value to be set.
    """
    path: str
    value: float


class PatchRequest(BaseModel):
    """
    Data model for a patch request containing multiple operations.

    Attributes:
        operations (list[Operation]): List of operations to perform.
    """
    operations: list[Operation]


# ------------------------------
# Helper Functions
# ------------------------------

def update_opc_node(node_identifier: str, speed: float):
    """
    Helper function to update an OPC-UA node with a new speed value.

    Parameters:
        node_identifier (str): The OPC-UA node identifier.
        speed (float): The new speed value to set.

    Returns:
        A dictionary with a confirmation message.

    Raises:
        HTTPException: If the client is not connected or if setting the value fails.
    """
    if not client:
        logging.error("OPC-UA client is not connected.")
        raise HTTPException(status_code=500, detail="OPC-UA client is not connected.")

    try:
        node = client.get_node(node_identifier)
        variant_value = ua.DataValue(ua.Variant(speed, ua.VariantType.Float))
        node.set_value(variant_value)
        logging.info("Set value for node %s to %s", node_identifier, variant_value)
        return {"message": f"Speed set to {speed}% for node {node_identifier}"}
    except Exception as e:
        logging.error("Error setting speed for node %s: %s", node_identifier, e)
        raise HTTPException(status_code=500, detail=f"Error setting speed: {e}")


# ------------------------------
# Application Lifecycle Events
# ------------------------------

@app.on_event("startup")
async def startup_event():
    """
    Startup event handler:
    - Initializes the OPC-UA client.
    - Attempts to connect to the OPC-UA server.
    """
    global client
    logging.info("Starting OPC-UA Client and connecting to %s", OPC_ADDRESS)
    client = Client(OPC_ADDRESS)
    try:
        client.connect()
        logging.info("Successfully connected to OPC-UA Server at: %s", OPC_ADDRESS)
    except Exception as e:
        logging.error("Error connecting to OPC-UA Server: %s", e)


@app.on_event("shutdown")
async def shutdown_event():
    """
    Shutdown event handler:
    - Disconnects from the OPC-UA server if the client is active.
    """
    global client
    if client:
        client.disconnect()
        logging.info("Disconnected from OPC-UA Server.")


# ------------------------------
# API Endpoints
# ------------------------------

@app.post("/machineOn")
async def machine_on():
    """
    POST endpoint to turn the machine on.

    TODO: Implement logic to power on the machine.
    """
    logging.info("POST /machineOn endpoint called")
    # TODO: Add code to turn the machine on.
    return {"message": "Machine on endpoint - TODO: implement logic"}


@app.post("/machineOff")
async def machine_off():
    """
    POST endpoint to turn the machine off.

    TODO: Implement logic to power off the machine.
    """
    logging.info("POST /machineOff endpoint called")
    # TODO: Add code to turn the machine off.
    return {"message": "Machine off endpoint - TODO: implement logic"}


@app.get("/speedOfBelt")
async def get_speed_belt():
    """
    GET endpoint to retrieve the current speed of the conveyor belt.
    The speed value is expected to be a percentage (%).

    Returns:
        A JSON object containing the key "speedOfBelt" with its current value.
    """
    logging.info("GET /speedOfBelt endpoint called")
    try:
        node = client.get_node('ns=3;s="OPC_Daten"."Istwert Magnertband"')
        speed_of_belt = node.get_value()
        logging.info("Retrieved conveyor belt speed: %s", speed_of_belt)
        return {"speedOfBelt": speed_of_belt}
    except Exception as e:
        logging.error("Error reading conveyor belt speed: %s", e)
        raise HTTPException(status_code=500, detail=f"Error reading speed: {e}")


@app.get("/speedOfDrum")
async def get_speed_drum():
    """
    GET endpoint to retrieve the current speed of the magnetic drum.
    The speed value is expected to be a percentage (%).

    Returns:
        A JSON object containing the key "speedOfDrum" with its current value.
    """
    logging.info("GET /speedOfDrum endpoint called")
    try:
        node = client.get_node('ns=3;s="OPC_Daten"."Istwert Magnettrommel"')
        speed_of_drum = node.get_value()
        logging.info("Retrieved magnetic drum speed: %s", speed_of_drum)
        return {"speedOfDrum": speed_of_drum}
    except Exception as e:
        logging.error("Error reading magnetic drum speed: %s", e)
        raise HTTPException(status_code=500, detail=f"Error reading speed: {e}")


@app.get("/speedOfFeeder")
async def get_speed_feeder():
    """
    GET endpoint to retrieve the current speed of the feeder.
    The speed value is expected to be a percentage (%).

    Returns:
        A JSON object containing the key "speedOfFeeder" with its current value.
    """
    logging.info("GET /speedOfFeeder endpoint called")
    try:
        node = client.get_node('ns=3;s="OPC_Daten"."Istwert Zuführband"')
        speed_of_feeder = node.get_value()
        logging.info("Retrieved feeder speed: %s", speed_of_feeder)
        return {"speedOfFeeder": speed_of_feeder}
    except Exception as e:
        logging.error("Error reading feeder speed: %s", e)
        raise HTTPException(status_code=500, detail=f"Error reading speed: {e}")


@app.patch("/speedOfDrum")
async def set_speed_drum(speed_input: SpeedInput):
    """
    PATCH endpoint to set the speed for the magnetic drum.

    Request Body Example:
        {
            "speed": 75.0  # The desired speed value (between 0 and 100)
        }

    Returns:
        A confirmation message with the new speed value.
    """
    logging.info("PATCH /speedOfDrum endpoint called with payload: %s", speed_input)
    return update_opc_node('ns=3;s="OPC_Daten"."Sollwert Magnettrommel"', speed_input.speed)


@app.patch("/speedOfBelt")
async def set_speed_belt(speed_input: SpeedInput):
    """
    PATCH endpoint to set the speed for the conveyor belt.

    Request Body Example:
        {
            "speed": 75.0  # The desired speed value (between 0 and 100)
        }

    Supported path:
      - /speedOfBelt  -> Node-ID: 'ns=3;s="OPC_Daten"."Sollwert Magnetband"'

    Returns:
        A confirmation message with the new speed value.
    """
    logging.info("PATCH /speedOfBelt endpoint called with payload: %s", speed_input)
    return update_opc_node('ns=3;s="OPC_Daten"."Sollwert Magnetband"', speed_input.speed)


@app.patch("/speedOfFeeder")
async def set_speed_feeder(speed_input: SpeedInput):
    """
    PATCH endpoint to set the speed for the feeder.

    Request Body Example:
        {
            "speed": 75.0  # The desired speed value (between 0 and 100)
        }

    Supported path:
      - /speedOfFeeder  -> Node-ID: 'ns=3;s="OPC_Daten"."Sollwert Zuführband"'

    Returns:
        A confirmation message with the new speed value.
    """
    logging.info("PATCH /speedOfFeeder endpoint called with payload: %s", speed_input)
    return update_opc_node('ns=3;s="OPC_Daten"."Sollwert Zuführband"', speed_input.speed)


@app.post("/stop")
async def stop_all():
    """
    POST endpoint to stop all machines by setting their speeds to 0.

    This endpoint sets the speed for:
      - Magnetic Drum
      - Conveyor Belt
      - Feeder

    Returns:
        A confirmation message indicating that all speeds have been set to 0.
    """
    logging.info("POST /stop endpoint called. Setting all speeds to 0.")
    drum_response = update_opc_node('ns=3;s="OPC_Daten"."Sollwert Magnettrommel"', 0)
    belt_response = update_opc_node('ns=3;s="OPC_Daten"."Sollwert Magnetband"', 0)
    feeder_response = update_opc_node('ns=3;s="OPC_Daten"."Sollwert Zuführband"', 0)

    return {
        "message": "All machine speeds have been set to 0.",
        "details": {
            "drum": drum_response,
            "belt": belt_response,
            "feeder": feeder_response
        }
    }