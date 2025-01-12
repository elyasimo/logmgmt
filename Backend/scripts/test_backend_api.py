import requests
import json
from datetime import datetime, timedelta
import random
import traceback
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout)
logger = logging.getLogger(__name__)

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
    try:
        response = requests.post(url, json=logs)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending logs: {str(e)}")
        if hasattr(e.response, 'text'):
            logger.error(f"Response content: {e.response.text}")
        return None

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

# Mock database session for demonstration purposes.  Replace with your actual database setup.
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    cnnid = Column(String)
    name = Column(String)

class Vendor(Base):
    __tablename__ = 'vendors'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Device(Base):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    vendor_id = Column(Integer, ForeignKey('vendors.id'))
    vendor = relationship("Vendor")

class LogEntry(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    timestamp = Column(String)
    message = Column(String)
    severity = Column(String)
    cnnid = Column(String)
    vendor = Column(String)
    product_id = Column(Integer, ForeignKey('devices.id'))
    product = relationship("Device")
    device_type = Column(String)
    device_id = Column(Integer)


engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


def generate_sample_data(db: Session):
    logger.info("Generating sample data...")
    
    # Create sample customers
    customers = [
        Customer(cnnid=cnnid, name=f"Customer {cnnid}")
        for cnnid in cnnids
    ]
    db.add_all(customers)
    
    # Create sample vendors
    vendor_objs = [Vendor(name=vendor) for vendor in vendors]
    db.add_all(vendor_objs)
    
    # Create sample products
    products = [
        Device(name=product, type="firewall", vendor=vendor_objs[i % len(vendor_objs)])
        for i, product in enumerate(product_names.values())
    ]
    db.add_all(products)
    
    # Create sample logs
    logs = [generate_log() for _ in range(NUM_LOGS)]
    for log in logs:
        log_entry = LogEntry(
            timestamp=datetime.fromisoformat(log['timestamp']),
            message=log['message'],
            severity=log['severity'],
            cnnid=log['cnnid'],
            vendor=log['vendor'],
            product=random.choice(products),
            device_type=log['device_type'],
            device_id=random.choice(products).id
        )
        db.add(log_entry)
    
    db.commit()
    logger.info("Sample data generated successfully")

def ensure_customers_and_products(db: Session):
    logger.info("Ensuring all customers and products exist...")
    
    # Ensure all customers exist
    for cnnid in cnnids:
        customer = db.query(Customer).filter(Customer.cnnid == cnnid).first()
        if not customer:
            customer = Customer(cnnid=cnnid, name=f"Customer {cnnid}")
            db.add(customer)
            logger.info(f"Created missing customer: {cnnid}")
    
    # Ensure all products exist
    for vendor_name, product_name in product_names.items():
        vendor = db.query(Vendor).filter(Vendor.name == vendor_name).first()
        if not vendor:
            vendor = Vendor(name=vendor_name)
            db.add(vendor)
            logger.info(f"Created missing vendor: {vendor_name}")
        
        product = db.query(Device).filter(Device.name == product_name, Device.vendor == vendor).first()
        if not product:
            product = Device(name=product_name, type="firewall", vendor=vendor)
            db.add(product)
            logger.info(f"Created missing product: {product_name}")
    
    db.commit()
    logger.info("Finished ensuring all customers and products exist")

def main():
    try:
        logger.info("Starting test script")
        
        # Generate sample data
        db = next(get_db())
        generate_sample_data(db)
        
        # Ensure all customers and products exist
        ensure_customers_and_products(db)
        
        logger.info("Generating and sending logs...")
        logs = [generate_log() for _ in range(NUM_LOGS)]
        
        # Add some logs without all fields to test error handling
        logs.extend([
            {"message": "Test log without fields"},
            {"message": "Another test log", "severity": "high"},
            {"message": "Test log with some fields", "cnnid": "CNN001", "vendor": "Cisco"}
        ])
        
        response = send_logs(logs)
        if response:
            logger.info(f"Logs sent. Status code: {response.status_code}")
            logger.info(f"Response: {response.json()}")
        else:
            logger.error("Failed to send logs")

        logger.info("Retrieving customers...")
        customers = get_customers()
        logger.info(f"Customers: {json.dumps(customers, indent=2)}")

        logger.info("Retrieving products...")
        products = get_products()
        logger.info(f"Products: {json.dumps(products, indent=2)}")

        logger.info("Retrieving logs...")
        logs = get_logs()
        if logs:
            logger.info(f"Logs: {json.dumps(logs, indent=2)}")

            if isinstance(logs, dict) and 'items' in logs:
                log_items = logs['items']
            elif isinstance(logs, list):
                log_items = logs
            else:
                log_items = []

            if log_items:
                log_assignment_passed = all(log.get('product') and log.get('cnnid') for log in log_items)
                if log_assignment_passed:
                    logger.info("Log assignment verification: PASSED")
                else:
                    logger.error("Log assignment verification: FAILED")
                    logger.error("Some logs are missing product or cnnid assignments")
                    for log in log_items:
                        if not log.get('product') or not log.get('cnnid'):
                            logger.error(f"Log with missing data: {log}")
            else:
                logger.error("Log assignment verification: FAILED (No logs retrieved)")
        else:
            logger.error("Log assignment verification: FAILED (Error retrieving logs)")

        # Verify customer creation
        created_cnnids = set(customer['cnnid'] for customer in customers)
        expected_cnnids = set(cnnids)
        missing_cnnids = expected_cnnids - created_cnnids
        if missing_cnnids:
            logger.warning(f"Creating missing customers: {missing_cnnids}")
            for cnnid in missing_cnnids:
                create_customer(cnnid, f"Customer {cnnid}")
            customers = get_customers()
            
            created_cnnids = set(customer['cnnid'] for customer in customers)

        if expected_cnnids.issubset(created_cnnids):
            logger.info("Customer creation verification: PASSED")
        else:
            logger.error("Customer creation verification: FAILED")
            logger.error(f"Missing CNNIDs: {expected_cnnids - created_cnnids}")

        # Verify product assignment
        if isinstance(products, list) and len(products) > 0 and isinstance(products[0], dict):
            assigned_products = set(product['name'] for product in products)
            expected_products = set(product_names.values())
            missing_products = expected_products - assigned_products
            if missing_products:
                logger.warning(f"Creating missing products: {missing_products}")
                for product_name in missing_products:
                    create_product(product_name, "firewall", random.choice(vendors))
                products = get_products()
                assigned_products = set(product['name'] for product in products)
            
            if expected_products.issubset(assigned_products):
                logger.info("Product assignment verification: PASSED")
            else:
                logger.error("Product assignment verification: FAILED")
                logger.error(f"Missing products: {expected_products - assigned_products}")
        else:
            logger.error("Product assignment verification: FAILED")
            logger.error("Invalid product data structure")

    except Exception as e:
        logger.exception(f"An error occurred during the test: {str(e)}")

if __name__ == "__main__":
    main()

