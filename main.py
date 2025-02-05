from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from opcua import Client
import requests
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()
client = None

# OPC-Adresse der Maschine
OPC_ADDRESS = "opc.tcp://192.168.0.1:4840"


class Operation(BaseModel):
    path: str
    value: float


class PatchRequest(BaseModel):
    operations: list[Operation]


@app.on_event("startup")
async def startup_event():
    global client
    logging.info("Starte OPC-UA Client und verbinde mich mit %s", OPC_ADDRESS)
    client = Client(OPC_ADDRESS)
    try:
        client.connect()
        logging.info("Erfolgreich mit OPC-UA Server verbunden: %s", OPC_ADDRESS)
    except Exception as e:
        logging.error("Fehler beim Verbinden mit OPC-UA Server: %s", e)


@app.on_event("shutdown")
async def shutdown_event():
    global client
    if client:
        client.disconnect()
        logging.info("Verbindung zum OPC-UA Server wurde getrennt.")


@app.get("/speed")
async def get_speed():
    """
    Lese den Wert für die Geschwindigkeit vom Förderband aus.
    Node-ID 'ns=2;i=2' muss ggf. an der Maschine angepasst werden.
    """
    logging.info("GET /speed wurde aufgerufen")
    try:
        node = client.get_node("ns=2;i=2")  # Beispiel-Node-ID, anpassen falls notwendig
        speed_of_belt = node.get_value()
        logging.info("Ausgelesene Geschwindigkeit vom Förderband: %s", speed_of_belt)
        return {"speedOfBelt": speed_of_belt}
    except Exception as e:
        logging.error("Fehler beim Auslesen der Geschwindigkeit: %s", e)
        raise HTTPException(status_code=500, detail=f"Error reading speed: {e}")


@app.patch("/speed")
async def set_speed(patch_request: PatchRequest):
    """
    Setze Geschwindigkeitswerte anhand der übergebenen Operationen.
    Unterstützte Pfade:
      - /SpeedOfBelt       -> Node-ID: ns=2;i=2
      - /SpeedOfVibration  -> Node-ID: ns=2;i=3
      - /SpeedOfDrum       -> Node-ID: ns=2;i=4
    """
    logging.info("PATCH /speed wurde mit Payload: %s", patch_request.json())
    try:
        for operation in patch_request.operations:
            if operation.path == "/SpeedOfBelt":
                node = client.get_node("ns=2;i=2")  # Beispiel-Node-ID, anpassen falls notwendig
                node.set_value(operation.value)
                logging.info("Setze SpeedOfBelt auf %s", operation.value)

            elif operation.path == "/SpeedOfVibration":
                node = client.get_node("ns=2;i=3")  # Beispiel-Node-ID, anpassen falls notwendig
                node.set_value(operation.value)
                logging.info("Setze SpeedOfVibration auf %s", operation.value)

            elif operation.path == "/SpeedOfDrum":
                node = client.get_node("ns=2;i=4")  # Beispiel-Node-ID, anpassen falls notwendig
                node.set_value(operation.value)
                logging.info("Setze SpeedOfDrum auf %s", operation.value)

            else:
                logging.warning("Ungültiger Pfad erhalten: %s", operation.path)
                raise HTTPException(status_code=400, detail=f"Invalid path: {operation.path}")

        machine_id = "da509dc5-743b-4fbe-c727-08dce93f67d2"
        url = f"https://dev-sorec-management-backend-aacgbja0evada2cm.northeurope-01.azurewebsites.net/api/machines/{machine_id}"
        data = {"status": "Speed updated successfully"}
        logging.info("Sende Update an externen Server: %s", url)
        try:
            ext_response = requests.patch(url, json=data)
            logging.info("Externer Server antwortete mit Statuscode: %s", ext_response.status_code)
        except Exception as http_err:
            logging.error("Fehler beim Senden der Daten an den externen Server: %s", http_err)

        logging.info("PATCH /speed erfolgreich abgeschlossen")
        return {"message": "200 OK", "data": data}

    except Exception as e:
        logging.error("Fehler beim Setzen der Geschwindigkeiten: %s", e)
        raise HTTPException(status_code=500, detail=f"Error setting speed: {e}")


# uvicorn main:app --reload
