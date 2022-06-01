FROM eclipse-mosquitto

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]

COPY ./receiver.sh /receiver.sh
CMD [ "/receiver.sh" ]
