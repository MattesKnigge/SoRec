from fastapi import HTTPException
from .opcua import check_opcua_connection

# Funktion zur Überprüfung der Verbindung und Auslösung von Fehlern
def check_connection_and_handle_error():
    try:
        check_opcua_connection()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
