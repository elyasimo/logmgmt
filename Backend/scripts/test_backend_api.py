import requests
import json
from datetime import datetime, timedelta
import random
import traceback

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"
NUM_LOGS = 50

# Sample data
vendors = ["Fortinet", "Cisco", "Palo Alto", "Juniper"]
severities = ["low", "medium", "high", "critical"]
device_types = ["firewall", "router", "switch", "endpoint"]
cnnids = ["CNN001", "CNN002", "CNN003", "CNN004", "CNN005"]
product_names = {"Fortinet": "FortiGate", "Cisco": "ASA", "Palo Alto": "PA-Series", "Juniper": "SRX"}

def generate_hostname(cnnid, country, devid):
    return f"{cnnid}-{country}-{devid}"

def generate_log():
    cnnid = random.choice(cnnids)
    vendor = random.choice(vendors)
    country = random.choice(["US", "UK", "DE", "FR", "JP"])
    devid = f"FG100D3G16{random.randint(10000000, 99999999)}"
    hostname = generate_hostname(cnnid, country, devid)
    
    return {
        "timestamp": (datetime.now() - timedelta(minutes=random.randint(0, 1440))).isoformat(),
        "message": f"Test log message from {hostname}",
        "severity": random.choice(severities),
        "vendor": vendor,
        "cnnid": cnnid,
        "device_type": random.choice(device_types),
        "product": product_names[vendor],
        "hostname": hostname,
        "devid": devid,
        "country": country
    }

def send_logs(logs):
    url = f"{API_BASE_URL}/logs"
    response = requests.post(url, json=logs)
    return response

def get_customers():
    url = f"{API_BASE_URL}/customers"
    response = requests.get(url)
    return response.json()

def create_customer(cnnid, name):
    url = f"{API_BASE_URL}/customers"
    response = requests.post(url, params={"cnnid": cnnid, "name": name})
    return response.json()

def get_products():
    url = f"{API_BASE_URL}/products"
    response = requests.get(url)
    return response.json()

def create_product(name, type, vendor_name):
    url = f"{API_BASE_URL}/products"
    response = requests.post(url, params={"name": name, "type": type, "vendor_name": vendor_name})
    return response.json()

def get_logs():
    url = f"{API_BASE_URL}/logs"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving logs: {str(e)}")
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text}")
        return None

def main():
    try:
        print("Generating and sending logs...")
        logs = [generate_log() for _ in range(NUM_LOGS)]
        response = send_logs(logs)
        print(f"Logs sent. Status code: {response.status_code}")
        print(f"Response: {response.json()}")

        print("\nRetrieving customers...")
        customers = get_customers()
        print(f"Customers: {json.dumps(customers, indent=2)}")

        print("\nRetrieving products...")
        products = get_products()
        print(f"Products: {json.dumps(products, indent=2)}")

        print("\nRetrieving logs...")
        logs = get_logs()
        if logs:
            print(f"Logs: {json.dumps(logs, indent=2)}")

            if isinstance(logs, dict) and 'items' in logs:
                log_items = logs['items']
            elif isinstance(logs, list):
                log_items = logs
            else:
                log_items = []

            if log_items:
                log_assignment_passed = all(log.get('product') and log.get('cnnid') for log in log_items)
                if log_assignment_passed:
                    print("Log assignment verification: PASSED")
                else:
                    print("Log assignment verification: FAILED")
                    print("Some logs are missing product or cnnid assignments")
                    for log in log_items:
                        if not log.get('product') or not log.get('cnnid'):
                            print(f"Log with missing data: {log}")
            else:
                print("Log assignment verification: FAILED (No logs retrieved)")
        else:
            print("Log assignment verification: FAILED (Error retrieving logs)")

        # Verify customer creation
        created_cnnids = set(customer['cnnid'] for customer in customers)
        expected_cnnids = set(cnnids)
        missing_cnnids = expected_cnnids - created_cnnids
        if missing_cnnids:
            print(f"\nCreating missing customers: {missing_cnnids}")
            for cnnid in missing_cnnids:
                create_customer(cnnid, f"Customer {cnnid}")
            customers = get_customers()
            
            created_cnnids = set(customer['cnnid'] for customer in customers)

        if expected_cnnids.issubset(created_cnnids):
            print("\nCustomer creation verification: PASSED")
        else:
            print("\nCustomer creation verification: FAILED")
            print(f"Missing CNNIDs: {expected_cnnids - created_cnnids}")

        # Verify product assignment
        if isinstance(products, list) and len(products) > 0 and isinstance(products[0], dict):
            assigned_products = set(product['name'] for product in products)
            expected_products = set(product_names.values())
            missing_products = expected_products - assigned_products
            if missing_products:
                print(f"\nCreating missing products: {missing_products}")
                for product_name in missing_products:
                    create_product(product_name, "firewall", random.choice(vendors))
                products = get_products()
                assigned_products = set(product['name'] for product in products)
            
            if expected_products.issubset(assigned_products):
                print("Product assignment verification: PASSED")
            else:
                print("Product assignment verification: FAILED")
                print(f"Missing products: {expected_products - assigned_products}")
        else:
            print("Product assignment verification: FAILED")
            print("Invalid product data structure")

    except Exception as e:
        print(f"An error occurred during the test: {str(e)}")
        print(traceback.format_exc())

if __name__ == "__main__":
    main()

