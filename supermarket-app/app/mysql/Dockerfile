FROM mysql:latest

RUN apt-get update && apt-get install -y netcat

COPY create_mysql_db.sh /usr/local/bin
COPY database.sql /usr/local/bin
