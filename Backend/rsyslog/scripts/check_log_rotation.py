import os
import datetime

def check_log_rotation(log_file):
    if not os.path.exists(log_file):
        print(f"Log file {log_file} does not exist.")
        return

    current_size = os.path.getsize(log_file)
    last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(log_file))
    
    print(f"Log file: {log_file}")
    print(f"Current size: {current_size} bytes")
    print(f"Last modified: {last_modified}")

if __name__ == "__main__":
    check_log_rotation("/var/log/syslog")
    check_log_rotation("/var/log/fortinet.log")

