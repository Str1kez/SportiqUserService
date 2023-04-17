FROM redis:7-alpine

RUN apk add --no-cache openssl
COPY ./misc/crontab.txt /crontab.txt
RUN crontab /crontab.txt

CMD ["sh", "-c", "crond -b; redis-server"]
