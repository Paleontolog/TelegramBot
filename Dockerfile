FROM alpine:latest

COPY /target/main .


RUN apk add --no-cache --upgrade bash
RUN apk add --no-cache -X http://dl-cdn.alpinelinux.org/alpine/edge/testing hub

RUN chmod u+x ./main

EXPOSE 80/tcp
CMD ./main
