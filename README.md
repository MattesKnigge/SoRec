
# OPC UA Server with FastAPI

This project sets up a FastAPI server to interact with an OPC UA server. It provides endpoints to get and set machine speeds for `SpeedOfBelt`, `SpeedOfVibration`, and `SpeedOfDrum`.

## Prerequisites

Before you run the server, make sure you have the following installed on your machine:

1. **Python 3.8+**  
2. **pip** (Python package installer)

You will also need access to an **OPC UA server** (local or remote) to connect to for reading and writing machine speeds.

## Configuration

Make sure your OPC UA server is running and accessible via `opc.tcp://localhost:4840/freeopcua/server/`. 

You will also need to update the **node IDs** (in the `get_speed` and `set_speed` endpoints) to match your OPC UA server's configuration. These are the identifiers for the machine's speed values that you want to monitor or adjust. In the provided example:

- **SpeedOfBelt** is located at `ns=2;i=2`
- **SpeedOfVibration** is located at `ns=2;i=3`
- **SpeedOfDrum** is located at `ns=2;i=4`

Additionally, update the `machine_id` in the PATCH request to match the relevant machine ID in your external system.

## Running the Server

Once you have everything set up, you can start the server with the following command:

```bash
uvicorn main:app --reload
```

This will start the FastAPI server, and it will be accessible at `http://127.0.0.1:8000`.

## Available Endpoints

1. **GET `/speed`**  
   Retrieves the current speed of the belt. The server will read the speed from the OPC UA server and return it in the response.

   **Response**:
   ```json
   {
     "speedOfBelt": 3.0  # Example speed value
   }
   ```

2. **PATCH `/speed`**  
   Sets the speed of the belt, vibration, or drum by sending a JSON payload with the operation (path) and the new value.

   **Payload example**:
   ```json
   {
     "operations": [
       {
         "path": "/SpeedOfBelt",
         "value": 5.0
       }
     ]
   }
   ```

   **Response**:
   ```json
   {
     "message": "200 OK",
     "data": {
       "status": "Speed updated successfully"
     }
   }
   ```

   This will update the corresponding value on the machine and simulate sending an update to an external server.

## Shutting Down

The server will automatically disconnect from the OPC UA server when it shuts down. You can manually shut down the server by pressing `Ctrl+C` in the terminal.

---

### Troubleshooting

- **Error connecting to OPC UA server**:  
  Ensure that the OPC UA server is running and accessible at the specified URL (`opc.tcp://localhost:4840/freeopcua/server/`).
  
- **Invalid path error in PATCH request**:  
  Ensure that the `path` in the PATCH request matches one of the valid values: `/SpeedOfBelt`, `/SpeedOfVibration`, or `/SpeedOfDrum`.

---
