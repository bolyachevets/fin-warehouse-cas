FROM alpine:latest

RUN apk add --no-cache openssh

USER root

RUN apk --update add python3

# Create working directory
RUN mkdir /opt/app-root && chmod 755 /opt/app-root
WORKDIR /opt/app-root

COPY . .

EXPOSE 8080

CMD [ "/bin/sh", "run.sh" ]
