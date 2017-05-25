# Microservice based Application/Service(s)

This project was developed to meet the following criteria:
Create a Shopping Cart application using python flask, mysql and docker.

##Requirements:
1. Python Flask				
2. Mysql
3. Docker
4. Docker-compose

##Usage:
###Running application with docker-compose:
1. start docker stack: `cd app && docker-compose up -d` or `cd app && docker-compose up` to run the application in foreground
2. stop/remove docker stack: `cd app && docker-compose down`

###Running application as server (legacy style) :
1. Populate database: `cd src/core/mysql && mysql -u root -p < database.sql`
2. Point the application to the target database `app.config['MYSQL_DATABASE_HOST'] = DATABASE`
3. Running the application: `cd src/core/ && python app.py`

##Functionalities:
1. Register user
2. Login user
3. Shopping Cart
4. PayPal Integration
