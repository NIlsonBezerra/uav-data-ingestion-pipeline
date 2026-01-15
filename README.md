# UAV Data Ingestion Pipeline (Capstone CS-414)

**Role:** Systems Integration Lead  
**Context:** Senior Capstone Project (Modular UAV Sensor Payload)  
**Hardware Target:** Raspberry Pi 5 (Central Hub)

## Project Overview
This repository contains the Python-based data ingestion logic designed to synchronize asynchronous data streams from a modular UAV sensor payload. The system manages a **split-bus topology**:
* **High-Bandwidth:** Ethernet/RTSP video stream from a SIYI A2 Mini gimbal camera.
* **Low-Bandwidth:** $I^2C$ telemetry from environmental sensors (LiDAR, GNSS, IMU).

## Architecture
The system uses a multi-threaded architecture to decouple sensor polling from data processing, ensuring that heavy video I/O does not block critical flight telemetry.

### Key Modules
* **`ingest_video_stream`**: Handles blocking RTSP frame capture.
* **`ingest_sensor_telemetry`**: Polls the $I^2C$ bus at 10Hz for spatial data.
* **`synchronize_streams`**: Correlates video frames with the nearest valid telemetry timestamp to enable downstream LAS/DEM generation.

## How to Run (Simulation Mode)
The `ingestion_pipeline.py` script includes a mock hardware layer to simulate sensor inputs for testing without physical drone hardware.

```bash
python3 ingestion_pipeline.py
