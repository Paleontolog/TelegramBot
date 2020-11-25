FROM golang AS builder
WORKDIR /go/src/github.com/alexellis/href-counter/
RUN go get -d -v  github.com/Syfaro/telegram-bot-api
RUN go get -d -v  github.com/lib/pq
COPY bot/main.go .
RUN env XDG_CACHE_HOME=/tmp/.cache env CGO_ENABLED=0 go build main.go


FROM alpine:latest
RUN apk add --no-cache --upgrade bash
RUN apk add --no-cache -X http://dl-cdn.alpinelinux.org/alpine/edge/testing hub
RUN apk --no-cache add ca-certificates
WORKDIR /root/
# RUN chmod u+x ./main
COPY --from=builder /go/src/github.com/alexellis/href-counter/main .
EXPOSE 80/tcp
CMD ["./main"]  
