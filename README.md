# SoRec - OPC-UA FastAPI Integration

SoRec is a FastAPI application designed for industrial machine control. It integrates with an OPC-UA server to monitor and control machine speeds. The application provides a comprehensive REST API to manage various machine components (such as a magnetic drum, conveyor belt, and feeder) and includes asynchronous background tasks for real-time monitoring.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture & Code Structure](#architecture--code-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Logging & Monitoring](#logging--monitoring)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

SoRec enables you to:
- Connect to an OPC-UA server to read and write machine parameters.
- Monitor the speed of a conveyor belt via a background task.
- Control machine operations (e.g., start, stop, and adjust speeds) using a RESTful API.
- Easily extend or modify the code thanks to its modular architecture.

This project is ideal for environments where machine performance and safety require real-time monitoring and control.

---

## Features

- **OPC-UA Integration:** Communicate with an OPC-UA server to control machine speeds.
- **Asynchronous Monitoring:** Continuously monitors the conveyor belt speed and logs significant changes.
- **RESTful API:** Provides endpoints for machine control and speed management.
- **Modular Design:** Clean separation between models, routes, utilities, and configuration.
- **Robust Error Handling:** Returns appropriate HTTP status codes and error messages when issues occur.

---

## Architecture & Code Structure

```
SoRec/
├── app/
│   ├── __init__.py         # Package initialization.
│   ├── main.py             # FastAPI app initialization, lifecycle events, and OPC-UA client setup.
│   ├── models.py           # Pydantic models for request validation.
│   ├── routes.py           # API endpoint definitions.
│   └── utils.py            # Helper functions for OPC-UA node updates and background monitoring.
├── requirements.txt        # Python dependencies.
└── README.md               # Project documentation.
```

- **`app/main.py`:** Initializes the FastAPI application, sets up the OPC-UA client, and configures startup/shutdown events.
- **`app/models.py`:** Contains data models (e.g., `SpeedInput`) used for validating API requests.
- **`app/routes.py`:** Defines all API endpoints for controlling machine operations and monitoring speeds.
- **`app/utils.py`:** Implements helper functions like `update_opc_node` and `monitor_speed_belt` that interact with the OPC-UA server.

---

## Installation

### Prerequisites

- Python 3.8 or higher.
- Access to an OPC-UA server (update the server address as needed).

### Steps

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/SoRec.git
   cd SoRec
   ```

2. **Create a Virtual Environment:**

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment:**

   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

The OPC-UA server address and other configurations are defined in `app/main.py`:

```python
OPC_ADDRESS = "opc.tcp://139.174.27.2:4840"
```

Update this address as necessary for your environment. Logging settings and other configurations are also managed in this file.

---

## Running the Application

To run the application with automatic reloading during development, execute:

```bash
uvicorn app.main:app --reload
```

The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## API Endpoints

### Belt Speed Monitoring

- **PATCH /startBeltSpeedMonitor**  
  **Tags:** Belt Speed Monitoring  
  **Summary:** Start Belt Speed Monitor  
  **Description:** Starts monitoring the speed of the conveyor belt by initiating a background task.  
  **Response:**  
  - `{ "message": "Monitor started" }` if started successfully, or  
  - `{ "message": "Monitor is already running" }` if already active.

- **PATCH /stopBeltSpeedMonitor**  
  **Tags:** Belt Speed Monitoring  
  **Summary:** Stop Belt Speed Monitor  
  **Description:** Stops the background task that monitors the conveyor belt speed.  
  **Response:**  
  - `{ "message": "Monitor stopped" }` if stopped successfully, or  
  - `{ "message": "Monitor is not running" }` if no task was active.

### Machine Control

- **PATCH /machineOn**  
  **Tags:** Machine Control  
  **Summary:** Turn Machine On  
  **Description:** Turns the machine on. *(Placeholder – logic needs to be implemented.)*  
  **Response:** `{ "message": "Machine on endpoint - TODO: implement logic" }`

- **PATCH /machineOff**  
  **Tags:** Machine Control  
  **Summary:** Turn Machine Off  
  **Description:** Turns the machine off. *(Placeholder – logic needs to be implemented.)*  
  **Response:** `{ "message": "Machine off endpoint - TODO: implement logic" }`

- **PATCH /stop**  
  **Tags:** Machine Control  
  **Summary:** Stop All Machine Components  
  **Description:** Stops all machine components by setting the speeds of the drum, belt, and feeder to 0.  
  **Response:** Returns detailed results for each component (drum, belt, feeder), indicating success or errors during the stop sequence.

### Speed Monitoring

- **GET /speedOfBelt**  
  **Tags:** Speed Monitoring  
  **Summary:** Get Belt Speed  
  **Description:** Retrieves the current speed of the conveyor belt (in %).  
  **Response:** `{ "speedOfBelt": <value> }`

- **GET /speedOfDrum**  
  **Tags:** Speed Monitoring  
  **Summary:** Get Drum Speed  
  **Description:** Retrieves the current speed of the magnetic drum (in %).  
  **Response:** `{ "speedOfDrum": <value> }`

- **GET /speedOfFeeder**  
  **Tags:** Speed Monitoring  
  **Summary:** Get Feeder Speed  
  **Description:** Retrieves the current speed of the feeder (in %).  
  **Response:** `{ "speedOfFeeder": <value> }`

### Speed Control

- **PATCH /speedOfDrum**  
  **Tags:** Speed Control  
  **Summary:** Set Drum Speed  
  **Description:** Sets the speed of the magnetic drum.  
  **Request Body:** JSON payload with the new speed (validated by `SpeedInput` model).  
  **Response:** Confirmation of the updated speed.

- **PATCH /speedOfBelt**  
  **Tags:** Speed Control  
  **Summary:** Set Belt Speed  
  **Description:** Sets the speed of the conveyor belt.  
  **Request Body:** JSON payload with the new speed (validated by `SpeedInput` model).  
  **Response:** Confirmation of the updated speed.

- **PATCH /speedOfFeeder**  
  **Tags:** Speed Control  
  **Summary:** Set Feeder Speed  
  **Description:** Sets the speed of the feeder.  
  **Request Body:** JSON payload with the new speed (validated by `SpeedInput` model).  
  **Response:** Confirmation of the updated speed.

---

## Logging & Monitoring

- **Logging:** The application logs all major events, including API calls, OPC-UA client interactions, and errors. Logs include timestamps and log levels to aid in debugging.
- **Background Task:** A dedicated asynchronous task continuously polls the OPC-UA server to monitor the conveyor belt speed. Significant changes trigger log entries, which can be used for further analysis or alerting.

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (e.g., `feature/YourFeature`).
3. Commit your changes and push to your fork.
4. Open a pull request with a detailed description of your changes.

Please ensure that your contributions follow the coding style and include appropriate tests and documentation.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

This README provides all necessary information to understand, set up, run, and extend the SoRec project. For any additional questions, please refer to the inline code comments or contact the project maintainers.
