FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive

COPY flag1 /
COPY flag2 /
COPY flag3 /
COPY sweeper /
COPY index.html /
RUN chmod 755 /sweeper
EXPOSE 8080

CMD [ "/sweeper" ]