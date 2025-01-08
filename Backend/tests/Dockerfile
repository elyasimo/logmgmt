FROM alpine:latest

RUN apk add --no-cache netcat-openbsd

COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]