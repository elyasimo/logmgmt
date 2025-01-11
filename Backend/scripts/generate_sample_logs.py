import requests
import json
from datetime import datetime, timedelta
import random
import time
import logging
from requests.exceptions import RequestException

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
API_ENDPOINT = "http://api:8000/api/v1/logs"
NUM_LOGS = 50
MAX_RETRIES = 30  # Increased from 5 to 30
RETRY_DELAY = 10  # Increased from 5 to 10 seconds

# Sample data
vendors = ["Cisco", "Juniper", "Palo Alto", "Fortinet", "Check Point", "F5", "Broadcom"]
severities = ["low", "medium", "high", "critical"]
device_types = ["firewall", "router", "switch", "endpoint", "load_balancer"]
cnnids = ["CNN001", "CNN002", "CNN003", "CNN004", "CNN005"]

def generate_logs():
    logs = []
    for _ in range(NUM_LOGS):
        timestamp = datetime.now() - timedelta(minutes=random.randint(0, 1440))  # Random time within last 24 hours
        log = {
            "timestamp": timestamp.isoformat(),
            "message": f"Sample log message for {random.choice(device_types)}",
            "severity": random.choice(severities),
            "vendor": random.choice(vendors),
            "cnnid": random.choice(cnnids),
            "device_type": random.choice(device_types)
        }
        logs.append(log)
    return logs

def send_logs_to_api(logs):
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(API_ENDPOINT, data="\n".join(json.dumps(log) for log in logs))
            if response.status_code == 200:
                logger.info(f"Successfully sent {NUM_LOGS} logs to the API.")
                logger.info(f"API Response: {response.json()}")
                return True
            else:
                logger.error(f"Failed to send logs. Status code: {response.status_code}")
                logger.error(f"Response: {response.text}")
        except RequestException as e:
            logger.error(f"Attempt {attempt + 1} failed: {e}")
        
        if attempt < MAX_RETRIES - 1:
            logger.info(f"Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)
        else:
            logger.error("Max retries reached. Failed to send logs.")
    return False

def main():
    logger.info("Waiting for API to become available...")
    while True:
        try:
            response = requests.get("http://api:8000/health")
            if response.status_code == 200:
                logger.info("API is available. Proceeding with log generation.")
                break
        except RequestException:
            logger.info("API not yet available. Retrying in 10 seconds...")
            time.sleep(10)

    logs = generate_logs()
    success = send_logs_to_api(logs)
    
    if success:
        logger.info("\nSample of sent logs:")
        for log in logs[:5]:
            logger.info(json.dumps(log, indent=2))
    else:
        logger.error("Failed to send logs to the API.")

if __name__ == "__main__":
    main()

