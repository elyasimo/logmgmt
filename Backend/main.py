import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Backend.api.routes import logs, customers, products
import random
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],  # Allows all origins
  allow_credentials=True,
  allow_methods=["*"],  # Allows all methods
  allow_headers=["*"],  # Allows all headers
)

# Include the logs router
app.include_router(logs.router, prefix="/api/v1")
app.include_router(customers.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")

def generate_log():
    vendors = ["fortinet", "cisco", "paloalto", "f5", "checkpoint", "broadcom"]
    device_types = ["firewall", "router", "switch", "endpoint"]
    severities = ["low", "medium", "high", "critical"]
    products = {
        "fortinet": "FortiGate",
        "cisco": "ASA",
        "paloalto": "PA-Series",
        "f5": "BIG-IP",
        "checkpoint": "CheckPoint",
        "broadcom": "Symantec"
    }
    
    vendor = random.choice(vendors)
    device_type = random.choice(device_types)
    severity = random.choice(severities)
    cnnid = f"CNN{random.randint(1, 999):03d}"
    
    return {
        "vendor": vendor,
        "timestamp": datetime.now().isoformat(),
        "message": f"Test log message from {device_type}",
        "cnnid": cnnid,
        "device_type": device_type,
        "severity": severity,
        "product": products[vendor]
    }

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the Log Management API"}

if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=8000)

