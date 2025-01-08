FROM alpine:latest

# Install required packages
RUN apk add --no-cache \
    rsyslog \
    rsyslog-mysql \
    logrotate \
    python3 \
    supervisor \
    util-linux && \
    mkdir -p /var/spool/rsyslog \
             /var/log/rsyslog \
             /var/log/supervisor \
             /var/run \
             /dev \
             /var/lib/logrotate \
             /app/rsyslog/scripts && \
    chown -R root:adm /var/spool/rsyslog \
                      /var/log/rsyslog \
                      /var/log/supervisor \
                      /var/run \
                      /var/lib/logrotate \
                      /app/rsyslog/scripts && \
    chmod -R 755 /var/spool/rsyslog \
                 /var/log/rsyslog \
                 /var/log/supervisor \
                 /var/run \
                 /var/lib/logrotate \
                 /app/rsyslog/scripts && \
    touch /dev/log && \
    chmod 666 /dev/log

RUN rsyslogd -v

# Copy configuration files
COPY config/*.conf /etc/rsyslog.d/
COPY logrotate.conf /etc/logrotate.d/rsyslog
COPY scripts/*.py /app/rsyslog/scripts/

# Create supervisord configuration
COPY supervisord.conf /etc/supervisord.conf

# Add logrotate cron job
RUN echo "0 * * * * /usr/sbin/logrotate /etc/logrotate.d/rsyslog" >> /etc/crontabs/root

# Create log files and set permissions
RUN for file in all.log error.log fortinet.log cisco.log paloalto.log f5.log checkpoint.log broadcom.log debug.log rsyslog-debug.log; do \
        touch /var/log/rsyslog/$file && \
        chmod 644 /var/log/rsyslog/$file && \
        chown root:adm /var/log/rsyslog/$file; \
    done

# Expose ports for TCP inputs only
EXPOSE 5014/tcp 5015/tcp 5016/tcp 5017/tcp 5018/tcp 5019/tcp

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]

