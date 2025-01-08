import json
import sys

def validate_json_log(log_file):
    with open(log_file, 'r') as f:
        for line in f:
            try:
                json.loads(line)
            except json.JSONDecodeError:
                print(f"Invalid JSON: {line}")
                return False
    print("All logs are valid JSON")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_json_log.py <log_file>")
        sys.exit(1)
    
    log_file = sys.argv[1]
    validate_json_log(log_file)

