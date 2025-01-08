import socket
import time
import datetime
import json

def send_log(message, host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.sendall(json.dumps(message).encode() + b'\n')
    sock.close()

def generate_log(vendor):
    timestamp = datetime.datetime.now().isoformat()
    log_message = f'{{"vendor": "{vendor}", "timestamp": "{timestamp}", "message": "Test log message from Python client"}}'
    return log_message

if __name__ == "__main__":
    rsyslog_host = "rsyslog"
    vendors = {
        "fortinet": 5014,
        "cisco": 5015,
        "paloalto": 5016,
        "f5": 5017,
        "checkpoint": 5017,
        "broadcom": 5017
    }

    while True:
        for vendor, port in vendors.items():
            log_message = generate_log(vendor)
            send_log(json.loads(log_message), rsyslog_host, port)
            print(f"Sent {vendor} log: {log_message}")
        time.sleep(5)

