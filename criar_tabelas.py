import mysql.connector


# Credenciais MySQL
username = # Inserir o username da sua instância RDS
password = # Inserir a senha da sua instância RDS
rds_endpoint = # Inserir o endpoint da sua instância RDS
port='3306'


# Criar a base de dados "Person" através do arquivo SQL
with open('criar_db_person.sql', 'r') as query:
   query = query.read()

conn = mysql.connector.connect(host=rds_endpoint, user=username, passwd=password)
cur = conn.cursor()
cur.execute(query)
conn.commit()

print('Database Person criada')


# Criar a base de dados "Production" através do arquivo SQL
with open('criar_db_production.sql', 'r') as query:
   query = query.read()

conn = mysql.connector.connect(host=rds_endpoint, user=username, passwd=password)
cur = conn.cursor()
cur.execute(query)
conn.commit()

print('Database Production criada')


# Criar a base de dados "Sales" através do arquivo SQL
with open('criar_db_sales.sql', 'r') as query:
   query = query.read()

conn = mysql.connector.connect(host=rds_endpoint, user=username, passwd=password)
cur = conn.cursor()
cur.execute(query)
conn.commit()

print('Database Sales criada')


# Criar a tabela "Product" através do arquivo SQL
with open('criar_tabela_product.sql', 'r') as query:
   query = query.read()

conn = mysql.connector.connect(host=rds_endpoint, user=username, passwd=password)
cur = conn.cursor()
cur.execute(query)
conn.commit()

print('Tabela Product criada')


# Criar a tabela "Person" através do arquivo SQL
with open('criar_tabela_person.sql', 'r') as query:
   query = query.read()

conn = mysql.connector.connect(host=rds_endpoint, user=username, passwd=password)
cur = conn.cursor()
cur.execute(query)
conn.commit()

print('Tabela Person criada')


# Criar a tabela "Customer" através do arquivo SQL
with open('criar_tabela_customer.sql', 'r') as query:
   query = query.read()

conn = mysql.connector.connect(host=rds_endpoint, user=username, passwd=password)
cur = conn.cursor()
cur.execute(query)
conn.commit()

print('Tabela Customer criada')


# Criar a tabela "Sales Order Header" através do arquivo SQL
with open('criar_tabela_salesOrderHeader.sql', 'r') as query:
   query = query.read()

conn = mysql.connector.connect(host=rds_endpoint, user=username, passwd=password)
cur = conn.cursor()
cur.execute(query)
conn.commit()

print('Tabela SalesOrderHeader criada')


# Criar a tabela "Sales Offer Product" através do arquivo SQL
with open('criar_tabela_specialOfferProduct.sql', 'r') as query:
   query = query.read()

conn = mysql.connector.connect(host=rds_endpoint, user=username, passwd=password)
cur = conn.cursor()
cur.execute(query)
conn.commit()

print('Tabela SpecialOfferProduct criada')


# Criar a tabela "Sales Order Detail" através do arquivo SQL
with open('criar_tabela_salesOrderDetail.sql', 'r') as query:
   query = query.read()

conn = mysql.connector.connect(host=rds_endpoint, user=username, passwd=password)
cur = conn.cursor()
cur.execute(query)
conn.commit()

print('Tabela Sales.SalesOrderDetail criada')
