FROM postgres:16.1

ADD . .
RUN chmod +x migrate_db.sh

CMD ["./migrate_db.sh"]