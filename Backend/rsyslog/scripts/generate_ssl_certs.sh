#!/bin/bash

# Generate CA key and certificate
openssl genrsa -out /etc/ssl/private/ca-key.pem 2048
openssl req -x509 -new -nodes -key /etc/ssl/private/ca-key.pem -sha256 -days 1024 -out /etc/ssl/certs/ca.pem -subj "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=CA"

# Generate rsyslog key and certificate signing request
openssl genrsa -out /etc/ssl/private/rsyslog-key.pem 2048
openssl req -new -key /etc/ssl/private/rsyslog-key.pem -out /tmp/rsyslog.csr -subj "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=rsyslog"

# Sign the rsyslog certificate with the CA
openssl x509 -req -in /tmp/rsyslog.csr -CA /etc/ssl/certs/ca.pem -CAkey /etc/ssl/private/ca-key.pem -CAcreateserial -out /etc/ssl/certs/rsyslog-cert.pem -days 365 -sha256

# Clean up
rm /tmp/rsyslog.csr

echo "SSL certificates generated successfully."

