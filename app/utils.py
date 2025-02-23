# app/utils.py
import logging
from fastapi import HTTPException
from opcua import ua

def update_opc_node(client, node_identifier: str, speed: float):
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

async def monitor_speed_belt(client, previous_speed_belt_ref):
    import asyncio
    node_identifier = 'ns=3;s="OPC_Daten"."Istwert Magnertband"'
    try:
        while True:
            try:
                node = client.get_node(node_identifier)
                current_speed = node.get_value()
                logging.info("Scheduled reading - Conveyor belt speed: %s", current_speed)
                if previous_speed_belt_ref[0] is not None:
                    if abs(current_speed - previous_speed_belt_ref[0]) >= 0.1:
                        logging.info("ALERT: Speed changed from %s to %s", previous_speed_belt_ref[0], current_speed)
                previous_speed_belt_ref[0] = current_speed
            except Exception as e:
                logging.error("Error in scheduled speed monitor: %s", e)
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        logging.info("Monitor task received cancellation request.")
        raise
