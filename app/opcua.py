from opcua import Client, ua
import logging

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

# Funktion zur Überprüfung der OPC-UA-Verbindung
def check_opcua_connection():
    global client
    if client is None:
        logging.warning("OPC UA client is None, attempting to reconnect...")
        client = Client(OPC_ADDRESS)
        try:
            client.connect()
            logging.info("Reconnected to OPC-UA Server.")
        except Exception as e:
            raise Exception(f"Failed to connect to OPC UA server: {str(e)}")

    try:
        client.get_node(ua.ObjectIds.Server_ServerStatus).get_value()
    except Exception as e:
        logging.error("Error during OPC UA connection check: %s", e)
        raise Exception("OPC UA server not connected or connection lost.")

# Startup-Logik
def init_opcua_client():
    global client
    if client is None:
        logging.info("Initializing OPC-UA Client for address: %s", OPC_ADDRESS)
        client = Client(OPC_ADDRESS)
        try:
            client.connect()
            logging.info("Successfully connected to OPC-UA Server.")
        except Exception as e:
            logging.error("Connection to OPC-UA server failed: %s", e)
            client = None

# Shutdown-Logik
def shutdown_opcua_client():
    global client
    if client:
        try:
            client.disconnect()
            logging.info("Disconnected from OPC-UA Server.")
        except Exception as e:
            logging.exception("Error during OPC-UA Client disconnect: %s", e)
