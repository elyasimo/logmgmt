#!/bin/bash

# Ensure correct permissions for rsyslog directories
chown -R root:root /var/log/rsyslog /var/spool/rsyslog
chmod -R 755 /var/log/rsyslog /var/spool/rsyslog

# Print rsyslog version
rsyslogd -version

# Check rsyslog configuration
rsyslogd -N1

# List loaded modules
rsyslogd -M

# Start rsyslog in the foreground
exec rsyslogd -n

