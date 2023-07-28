import mysql.connector


# Credenciais MySQL
username = # Username da sua instância RDS
password = # Senha da sua instância RDS
rds_endpoint = # Endpoint da sua instância RDS
port='3306' # Porta padrão MySQL


# Criar a base de dados "dataRox" através do arquivo SQL
with open('criar_db_testeRox.sql', 'r') as query:
   query = query.read()

conn = mysql.connector.connect(host=rds_endpoint, user=username, passwd=password)
cur = conn.cursor()
cur.execute(query)
conn.commit()
print('Database testeRox criada')


# Criar a tabela "Customer" através do arquivo SQL
with open('criar_tabela_Customer.sql', 'r') as query:
   query = query.read()

conn = mysql.connector.connect(host=rds_endpoint, user=username, passwd=password)
cur = conn.cursor()
cur.execute(query)
conn.commit()
print('Tabela Customer criada')


# Criar a tabela "Person" através do arquivo SQL
with open('criar_tabela_Person.sql', 'r') as query:
   query = query.read()

conn = mysql.connector.connect(host=rds_endpoint, user=username, passwd=password)
cur = conn.cursor()
cur.execute(query)
conn.commit()
print('Tabela Person criada')


# Criar a tabela "Product" através do arquivo SQL
with open('criar_tabela_Product.sql', 'r') as query:
   query = query.read()

conn = mysql.connector.connect(host=rds_endpoint, user=username, passwd=password)
cur = conn.cursor()
cur.execute(query)
conn.commit()
print('Tabela Product criada')


# Criar a tabela "SalesOrderDetail" através do arquivo SQL
with open('criar_tabela_SalesOrderDetail.sql', 'r') as query:
   query = query.read()

conn = mysql.connector.connect(host=rds_endpoint, user=username, passwd=password)
cur = conn.cursor()
cur.execute(query)
conn.commit()
print('Tabela SalesOrderDetail criada')


# Criar a tabela "SalesOrderHeader" através do arquivo SQL
with open('criar_tabela_SalesOrderHeader.sql', 'r') as query:
   query = query.read()

conn = mysql.connector.connect(host=rds_endpoint, user=username, passwd=password)
cur = conn.cursor()
cur.execute(query)
conn.commit()
print('Tabela SalesOrderHeader criada')


# Criar a tabela "SpecialOfferProduct" através do arquivo SQL
with open('criar_tabela_SpecialOfferProduct.sql', 'r') as query:
   query = query.read()

conn = mysql.connector.connect(host=rds_endpoint, user=username, passwd=password)
cur = conn.cursor()
cur.execute(query)
conn.commit()
print('Tabela SpecialOfferProduct criada')
