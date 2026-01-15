import time
import json
import random
import threading
from datetime import datetime

# Simulated Hardware Constants (RTSP Stream & Sensor Bus)
RTSP_FRAME_RATE = 30  # fps
SENSOR_POLL_RATE = 10  # Hz (I2C)


class DataIngestionPipeline:
    def __init__(self):
        self.running = True
        self.latest_frame = None
        self.telemetry_buffer = []
        self.lock = threading.Lock()

    def timestamp(self):
        """High-precision timestamp for synchronization."""
        return datetime.now().isoformat()

    def ingest_video_stream(self):
        """Simulates high-bandwidth RTSP video ingestion (SIYI A2 Mini)."""
        print("[SYSTEM] Starting RTSP Video Ingestion Thread...")
        while self.running:
            # Simulate frame capture (Blocking I/O)
            time.sleep(1 / RTSP_FRAME_RATE)

            with self.lock:
                self.latest_frame = {
                    "source": "SIYI_A2_MINI",
                    "timestamp": self.timestamp(),
                    "frame_id": random.randint(1000, 9999),
                    "size_bytes": 1024 * 500  # Approx 500KB frame
                }

    def ingest_sensor_telemetry(self):
        """Simulates low-bandwidth I2C sensor polling (LiDAR/GNSS)."""
        print("[SYSTEM] Starting I2C Sensor Bus Polling...")
        while self.running:
            time.sleep(1 / SENSOR_POLL_RATE)

            # Simulate sensor read
            telemetry = {
                "gnss": {"lat": 42.500 + random.uniform(-0.001, 0.001), "lon": -71.200},
                "imu": {"pitch": random.uniform(-5, 5), "roll": random.uniform(-2, 2)},
                "lidar_distance_m": random.uniform(20.0, 100.0),
                "timestamp": self.timestamp()
            }

            with self.lock:
                self.telemetry_buffer.append(telemetry)
                # Keep buffer small (real-time constraint)
                if len(self.telemetry_buffer) > 50:
                    self.telemetry_buffer.pop(0)

    def synchronize_streams(self):
        """Correlates Video Frames with nearest Spatial Telemetry."""
        print("[SYSTEM] Starting Data Synchronization Service...")
        while self.running:
            time.sleep(0.1)  # Sync every 100ms

            with self.lock:
                if self.latest_frame and self.telemetry_buffer:
                    # Fetch latest frame and most recent telemetry
                    frame = self.latest_frame
                    sensor_data = self.telemetry_buffer[-1]

                    # Log the sync event (simulating LAS/DEM generation prep)
                    print(
                        f"[SYNC] Frame {frame['frame_id']} <-> LiDAR {sensor_data['lidar_distance_m']:.2f}m | Lag: 12ms")

    def start(self):
        # Multi-threaded architecture for asynchronous I/O
        t1 = threading.Thread(target=self.ingest_video_stream)
        t2 = threading.Thread(target=self.ingest_sensor_telemetry)
        t3 = threading.Thread(target=self.synchronize_streams)

        t1.start()
        t2.start()
        t3.start()

        try:
            while True: time.sleep(1)
        except KeyboardInterrupt:
            print("[SYSTEM] Shutting down pipeline...")
            self.running = False


if __name__ == "__main__":
    pipeline = DataIngestionPipeline()
    pipeline.start()