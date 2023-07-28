import mysql.connector

# MySQL Credentials
username = # Your RDS instance username
password = # Your RDS instance password
rds_endpoint = # Your RDS instance endpoint
port = '3306'  # Default MySQL port

# Create the database "dataRox" using the SQL file
with open('create_db_testRox.sql', 'r') as query:
    query = query.read()

conn = mysql.connector.connect(host=rds_endpoint, user=username, passwd=password)
cur = conn.cursor()
cur.execute(query)
conn.commit()
print('Database testRox created')

# Create the "Customer" table using the SQL file
with open('create_table_Customer.sql', 'r') as query:
    query = query.read()

conn = mysql.connector.connect(host=rds_endpoint, user=username, passwd=password)
cur = conn.cursor()
cur.execute(query)
conn.commit()
print('Table Customer created')

# Create the "Person" table using the SQL file
with open('create_table_Person.sql', 'r') as query:
    query = query.read()

conn = mysql.connector.connect(host=rds_endpoint, user=username, passwd=password)
cur = conn.cursor()
cur.execute(query)
conn.commit()
print('Table Person created')

# Create the "Product" table using the SQL file
with open('create_table_Product.sql', 'r') as query:
    query = query.read()

conn = mysql.connector.connect(host=rds_endpoint, user=username, passwd=password)
cur = conn.cursor()
cur.execute(query)
conn.commit()
print('Table Product created')

# Create the "SalesOrderDetail" table using the SQL file
with open('create_table_SalesOrderDetail.sql', 'r') as query:
    query = query.read()

conn = mysql.connector.connect(host=rds_endpoint, user=username, passwd=password)
cur = conn.cursor()
cur.execute(query)
conn.commit()
print('Table SalesOrderDetail created')

# Create the "SalesOrderHeader" table using the SQL file
with open('create_table_SalesOrderHeader.sql', 'r') as query:
    query = query.read()

conn = mysql.connector.connect(host=rds_endpoint, user=username, passwd=password)
cur = conn.cursor()
cur.execute(query)
conn.commit()
print('Table SalesOrderHeader created')

# Create the "SpecialOfferProduct" table using the SQL file
with open('create_table_SpecialOfferProduct.sql', 'r') as query:
    query = query.read()

conn = mysql.connector.connect(host=rds_endpoint, user=username, passwd=password)
cur = conn.cursor()
cur.execute(query)
conn.commit()
print('Table SpecialOfferProduct created')
