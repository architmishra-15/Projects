# from fastapi import FastAPI
# from typing import Dict
# import asyncio
# import requests
# import time
# import aiohttp
# import os


# import aiohttp
# import time
# import asyncio

# app = FastAPI(
#     title="Speed Test API",
#     description="API for measuring download and upload speed",
#     version="0.1.0"
# )

# async def measure_download_speed(test_duration: int = 5) -> float:
#     """
#     Measures download speed using a secure HTTPS connection.
    
#     We're using a 25MB test file from a fast CDN to ensure reliable measurements.
#     The function downloads data for a fixed duration to get an accurate speed reading.
    
#     Args:
#         test_duration: Number of seconds to run the test (default 5 seconds)
    
#     Returns:
#         float: Download speed in Mbps (Megabits per second)
#     """
#     # Using Cloudflare's CDN which is globally distributed and fast
#     url = "http://speedtest.tele2.net/10MB.zip"
    
#     total_bytes = 0
#     start_time = time.time()
    
#     # Configure timeout to prevent hanging
#     timeout = aiohttp.ClientTimeout(total=test_duration + 5)
    
#     async with aiohttp.ClientSession(timeout=timeout) as session:
#         try:
#             async with session.get(url) as response:
#                 # Make sure we got a successful response
#                 if response.status != 200:
#                     print(f"Error: Server returned status {response.status}")
#                     return 0.0
                
#                 # Read the response in chunks while keeping track of time
#                 async for chunk in response.content.iter_chunked(16384):  # Using larger chunks (16KB)
#                     total_bytes += len(chunk)
                    
#                     # Stop if we've reached our test duration
#                     if (time.time() - start_time) >= test_duration:
#                         break
            
#             duration = time.time() - start_time
            
#             # Avoid division by zero and ensure minimum test duration
#             if duration < 0.1:
#                 return 0.0
                
#             # Calculate speed in Mbps
#             speed_mbps = (total_bytes * 8) / (duration * 1_000_000)
#             return speed_mbps
            
#         except Exception as e:
#             print(f"Download test error: {str(e)}")
#             return 0.0


# async def measure_upload_speed(url: str = "https://speed.cloudflare.com/__up") -> float:
#     """
#     Measures upload speed by sending data and calculating transfer rate.
#     Returns speed in Mbps (Megabits per second).
#     """
#     # Create sample data for upload (10MB)
#     data_size = 10_000_000
#     data = os.urandom(data_size)
    
#     async with aiohttp.ClientSession() as session:
#         start_time = time.time()
        
#         async with session.post(url, data=data) as response:
#             await response.read()
            
#         duration = time.time() - start_time
        
#         # Convert bytes to bits and duration to seconds to get Mbps
#         speed_mbps = (data_size * 8) / (duration * 1_000_000)
#         return speed_mbps


# app = FastAPI(
#     title="Speed Test API",
#     description="API for measuring download and upload speed",
#     version="0.1.0"
# )

# @app.get("/speed-test")
# async def perform_speed_test() -> Dict:
#     """
#     Performs both download and upload speed tests and returns results.
#     """
#     # Perform multiple tests for more accurate results
#     download_speeds = []
#     upload_speeds = []
    
#     for _ in range(3):  # Run 3 tests for each
#         download_speed = await measure_download_speed()
#         download_speeds.append(download_speed)
        
#         # Brief pause between tests
#         await asyncio.sleep(1)
        
#         upload_speed = await measure_upload_speed()
#         upload_speeds.append(upload_speed)
    
#     return {
#         "download_speed": sum(download_speeds) / len(download_speeds),
#         "upload_speed": sum(upload_speeds) / len(upload_speeds),
#         "unit": "Mbps"
#     }

# @app.get("/speed-test/download")
# async def test_download_speed():
#     try:
#         speed = await measure_download_speed()
        
#         return {
#             "download_speed": round(speed, 2),  # Round to 2 decimal places for cleaner output
#             "unit": "Mbps",
#             "status": "success"
#         }
#     except Exception as e:
#         return {
#             "download_speed": 0,
#             "unit": "Mbps",
#             "status": "error",
#             "error": str(e)
#         }

# @app.get("/speed-test/upload")
# async def test_upload_speed():
#     try:
#         speed = await measure_upload_speed()
        
#         return {
#             "upload_speed": round(speed, 2),  # Round to 2 decimal places for cleaner output
#             "unit": "Mbps",
#             "status": "success"
#         }
#     except Exception as e:
#         return {
#             "upload_speed": 0,
#             "unit": "Mbps",
#             "status": "error",
#             "error": str(e)
#         }

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import aiohttp
import time
import json
from typing import List

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active WebSocket connections
active_connections: List[WebSocket] = []

@app.websocket("/ws/speedtest")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "start_test":
                # Trigger speed test when client requests it
                await measure_download_speed(websocket)
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
    finally:
        active_connections.remove(websocket)

async def measure_download_speed(websocket: WebSocket) -> float:
    """Measures download speed and sends real-time updates to the client"""
    url = "http://speedtest.tele2.net/10MB.zip"
    total_bytes = 0
    start_time = time.time()
    last_update = start_time
    
    timeout = aiohttp.ClientTimeout(total=30)  # 30 seconds timeout
    
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as response:
                if response.status != 200:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Failed to connect to speed test server"
                    })
                    return 0.0
                
                speeds = []
                async for chunk in response.content.iter_chunked(16384):
                    total_bytes += len(chunk)
                    current_time = time.time()
                    
                    # Send updates every 200ms
                    if current_time - last_update >= 0.2:
                        duration = current_time - start_time
                        current_speed = (total_bytes * 8) / (duration * 1_000_000)
                        speeds.append(current_speed)
                        
                        # Send real-time update to client
                        await websocket.send_json({
                            "type": "speed_update",
                            "speed": round(current_speed, 2)
                        })
                        
                        last_update = current_time
                    
                    # Stop after 10 seconds
                    if current_time - start_time >= 30:
                        break
            
            # Calculate and send final average speed
            average_speed = speeds[-1]
            await websocket.send_json({
                "type": "test_complete",
                "current_speed": round(average_speed, 2)
            })
            
            return average_speed
            
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "message": str(e)
        })
        return 0.0

# Regular HTTP endpoint (optional, as we're using WebSocket for real-time updates)
@app.get("/speed-test/download")
async def test_download_speed():
    return {"message": "Please use WebSocket connection for speed test"}