#!/bin/bash

# ... (keep existing content)

# Add the following at the end of the file:

# Test client logic
while true; do
    echo "<34>$(date): Test log message from Alpine client" | nc -w 1 rsyslog 5014
    sleep 5
done