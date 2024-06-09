# pip install mysql
# pip install mysql-connector-python
# pip install mysql-connector

import mysql.connector

dataBase = mysql.connector.connect(
    host= 'localhost',
    user= 'root',
    passwd= 'password123'
    )


# Prepare a cursor object
cursorObject = dataBase.cursor()

# Create a database
cursorObject.execute("CREATE DATABASE mybase")

print('Database created!!')
