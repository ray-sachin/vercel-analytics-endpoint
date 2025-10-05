from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# Enable CORS for POST requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Embedded telemetry data
TELEMETRY_DATA = [
  {"region": "apac", "service": "support", "latency_ms": 206.32, "uptime_pct": 97.878, "timestamp": 20250301},
  {"region": "apac", "service": "payments", "latency_ms": 153.42, "uptime_pct": 97.371, "timestamp": 20250302},
  {"region": "apac", "service": "checkout", "latency_ms": 203.74, "uptime_pct": 99.344, "timestamp": 20250303},
  {"region": "apac", "service": "analytics", "latency_ms": 221.07, "uptime_pct": 99.322, "timestamp": 20250304},
  {"region": "apac", "service": "analytics", "latency_ms": 160.37, "uptime_pct": 97.234, "timestamp": 20250305},
  {"region": "apac", "service": "recommendations", "latency_ms": 128.26, "uptime_pct": 99.075, "timestamp": 20250306},
  {"region": "apac", "service": "checkout", "latency_ms": 195.68, "uptime_pct": 98.616, "timestamp": 20250307},
  {"region": "apac", "service": "support", "latency_ms": 179.06, "uptime_pct": 97.466, "timestamp": 20250308},
  {"region": "apac", "service": "catalog", "latency_ms": 138.74, "uptime_pct": 98.541, "timestamp": 20250309},
  {"region": "apac", "service": "support", "latency_ms": 133.25, "uptime_pct": 99.21, "timestamp": 20250310},
  {"region": "apac", "service": "recommendations", "latency_ms": 147.3, "uptime_pct": 98.215, "timestamp": 20250311},
  {"region": "apac", "service": "analytics", "latency_ms": 102, "uptime_pct": 97.325, "timestamp": 20250312},
  {"region": "emea", "service": "checkout", "latency_ms": 184.47, "uptime_pct": 99.218, "timestamp": 20250301},
  {"region": "emea", "service": "support", "latency_ms": 105.09, "uptime_pct": 98.248, "timestamp": 20250302},
  {"region": "emea", "service": "support", "latency_ms": 137.32, "uptime_pct": 98.967, "timestamp": 20250303},
  {"region": "emea", "service": "catalog", "latency_ms": 238.61, "uptime_pct": 98.777, "timestamp": 20250304},
  {"region": "emea", "service": "catalog", "latency_ms": 135.76, "uptime_pct": 97.589, "timestamp": 20250305},
  {"region": "emea", "service": "recommendations", "latency_ms": 186.44, "uptime_pct": 99.026, "timestamp": 20250306},
  {"region": "emea", "service": "support", "latency_ms": 151.63, "uptime_pct": 99.325, "timestamp": 20250307},
  {"region": "emea", "service": "catalog", "latency_ms": 217.21, "uptime_pct": 99.311, "timestamp": 20250308},
  {"region": "emea", "service": "support", "latency_ms": 197.95, "uptime_pct": 97.734, "timestamp": 20250309},
  {"region": "emea", "service": "analytics", "latency_ms": 210.64, "uptime_pct": 97.804, "timestamp": 20250310},
  {"region": "emea", "service": "support", "latency_ms": 164.35, "uptime_pct": 98.373, "timestamp": 20250311},
  {"region": "emea", "service": "support", "latency_ms": 128.17, "uptime_pct": 99.217, "timestamp": 20250312},
  {"region": "amer", "service": "catalog", "latency_ms": 161.79, "uptime_pct": 98.315, "timestamp": 20250301},
  {"region": "amer", "service": "recommendations", "latency_ms": 150.97, "uptime_pct": 97.577, "timestamp": 20250302},
  {"region": "amer", "service": "checkout", "latency_ms": 140.64, "uptime_pct": 97.608, "timestamp": 20250303},
  {"region": "amer", "service": "recommendations", "latency_ms": 150.71, "uptime_pct": 99.389, "timestamp": 20250304},
  {"region": "amer", "service": "checkout", "latency_ms": 135.63, "uptime_pct": 98.521, "timestamp": 20250305},
  {"region": "amer", "service": "recommendations", "latency_ms": 163.01, "uptime_pct": 98.439, "timestamp": 20250306},
  {"region": "amer", "service": "checkout", "latency_ms": 197.04, "uptime_pct": 99.474, "timestamp": 20250307},
  {"region": "amer", "service": "checkout", "latency_ms": 208.34, "uptime_pct": 97.775, "timestamp": 20250308},
  {"region": "amer", "service": "support", "latency_ms": 217.78, "uptime_pct": 98.924, "timestamp": 20250309},
  {"region": "amer", "service": "analytics", "latency_ms": 216.68, "uptime_pct": 99.188, "timestamp": 20250310},
  {"region": "amer", "service": "checkout", "latency_ms": 124.76, "uptime_pct": 98.121, "timestamp": 20250311},
  {"region": "amer", "service": "analytics", "latency_ms": 198.13, "uptime_pct": 98.497, "timestamp": 20250312}
]

@app.post("/analytics")
async def analytics(request: Request):
    data = await request.json()
    regions = data.get("regions", [])
    threshold_ms = data.get("threshold_ms", 180)
    
    result = {}
    
    for region in regions:
        # Filter data for this region
        region_data = [d for d in TELEMETRY_DATA if d["region"] == region]
        
        if not region_data:
            continue
            
        # Calculate metrics
        latencies = [d["latency_ms"] for d in region_data]
        uptimes = [d["uptime_pct"] for d in region_data]
        
        # Average latency
        avg_latency = sum(latencies) / len(latencies)
        
        # 95th percentile latency
        sorted_latencies = sorted(latencies)
        p95_index = int(len(sorted_latencies) * 0.95)
        p95_latency = sorted_latencies[p95_index]
        
        # Average uptime
        avg_uptime = sum(uptimes) / len(uptimes)
        
        # Breaches (count of records above threshold)
        breaches = sum(1 for lat in latencies if lat > threshold_ms)
        
        result[region] = {
            "avg_latency": round(avg_latency, 2),
            "p95_latency": round(p95_latency, 2),
            "avg_uptime": round(avg_uptime, 2),
            "breaches": breaches
        }
    
    return result

@app.get("/")
def read_root():
    return {"message": "Analytics API is running. POST to /analytics with regions and threshold_ms"}
