FROM eclipse-mosquitto

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]

COPY ./mqtt.sh /mqtt.sh
CMD [ "/mqtt.sh" ]

EXPOSE 1883
