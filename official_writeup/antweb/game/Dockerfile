FROM openjdk:8u342-jre
ENV LANG C.UTF-8
VOLUME /tmp
COPY PKU_GeekGame_Ant_Web-1.0.0-SNAPSHOT.jar web.jar
COPY PKU_GeekGame_Ant_Backend-1.0.0-SNAPSHOT.jar backend.jar
COPY PKU_GeekGame_Ant_Bonus-1.0.0-SNAPSHOT.jar bonus.jar
COPY flag1.txt /root/flag1.txt
COPY flag2.txt /root/flag2.txt
COPY flag3.txt /root/flag3.txt

RUN echo \
"#!/bin/sh\n"\
"nohup java -jar /backend.jar --server.port=8079 &\n"\
"nohup java -jar /bonus.jar --server.port=8080 &"\
>> /start.sh

RUN chmod +x /start.sh

CMD nohup sh -c "/start.sh && java -jar /web.jar --server.port=80"
EXPOSE 80