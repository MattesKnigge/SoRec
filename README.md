
# OPC-UA FastAPI Server

This project provides an OPC-UA server client interface using FastAPI, allowing for the interaction with machines via the OPC-UA protocol. It offers endpoints to read and set the speed of various components (e.g., belts, drums, feeders) via the OPC-UA server.

## Project Structure

The project is structured as follows:

```
/app
    /main.py         # Main application, initialization, and routing
    /opcua.py        # OPC-UA client and connection handling
    /models.py       # Pydantic models (e.g., for SpeedUpdate)
    /utils.py        # Utility functions like connection checks
```

- **`main.py`**: Contains the FastAPI app with all the API endpoints.
- **`opcua.py`**: Contains all the OPC-UA client logic, including connecting and disconnecting to the server.
- **`models.py`**: Contains Pydantic models for data validation, e.g., `SpeedUpdate`.
- **`utils.py`**: Includes utility functions, such as connection checks for the OPC-UA server.

## Prerequisites

To run this project, you need to have Python 3.8+ installed. The following dependencies are required:

- `fastapi`: The web framework for building the API.
- `uvicorn`: The ASGI server to run the FastAPI application.
- `opcua`: The Python library for interacting with OPC-UA servers.
- `pydantic`: For data validation using Pydantic models.

To install the dependencies, use `pip`:

```bash
pip install fastapi uvicorn opcua pydantic
```

## Running the Application

To run the FastAPI server, use the following command:

```bash
uvicorn app.main:app --reload
```

This will start the server on `http://127.0.0.1:8000`, and you can access the OpenAPI documentation at `http://127.0.0.1:8000/docs`.

## API Endpoints

### Health Check

**GET /health**

Check the status of the OPC-UA connection. Returns a status of the server and the current time.

```bash
GET /health
```

Response:
```json
{
    "status": "ok",
    "server_time": "2025-05-03 12:00:00"
}
```

### Get Current Speed

**GET /get_speed_belt**

Retrieve the current speed of the belt.

```bash
GET /get_speed_belt
```

Response:
```json
{
    "speed": 15.0
}
```

### Set Speed for Belt

**PATCH /set_speed_belt**

Set a new speed for the belt. The speed is passed in the request body.

```bash
PATCH /set_speed_belt
```

Request body:
```json
{
    "speed": 20.5
}
```

Response:
```json
{
    "message": "Speed updated successfully"
}
```

### Get Current Drum Speed

**GET /get_speed_drum**

Retrieve the current speed of the drum.

```bash
GET /get_speed_drum
```

Response:
```json
{
    "speed": 10.0
}
```

### Set Speed for Drum

**PATCH /set_speed_drum**

Set a new speed for the drum.

```bash
PATCH /set_speed_drum
```

Request body:
```json
{
    "speed": 15.0
}
```

Response:
```json
{
    "message": "Speed updated successfully"
}
```

### Get Current Feeder Speed

**GET /get_speed_feeder**

Retrieve the current speed of the feeder.

```bash
GET /get_speed_feeder
```

Response:
```json
{
    "speed": 5.0
}
```

### Set Speed for Feeder

**PATCH /set_speed_feeder**

Set a new speed for the feeder.

```bash
PATCH /set_speed_feeder
```

Request body:
```json
{
    "speed": 8.0
}
```

Response:
```json
{
    "message": "Speed updated successfully"
}
```

## Configuration

The OPC-UA server address is configured in the `opcua.py` file. By default, the address is set to:

```python
OPC_ADDRESS = "opc.tcp://127.0.0.1:4840"
```

If your OPC-UA server is running on a different address, update the `OPC_ADDRESS` accordingly.

## Exception Handling

- If the OPC-UA server is not connected or the client cannot communicate with it, an error message is returned for any request that requires the OPC-UA connection.
- All endpoints that interact with the server include error handling to ensure that the server's status is checked before performing any operations.

## Shutting Down the Application

The application automatically disconnects from the OPC-UA server upon shutdown. You can initiate the shutdown process by stopping the FastAPI server.

```bash
CTRL+C  # Stop the server
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.