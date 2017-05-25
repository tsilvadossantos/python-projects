#!/bin/bash
set -e

mysqld >/dev/null 2>&1 &

while ! nc -z mysql-node01 3306; do sleep 3; done
#Dumping mysql mb_prod_schema
mysql -u root --password=abc123 -h mysql-node01 < /usr/local/bin/database.sql | tee /usr/local/bin/schema.out
