import boto3

# Nome do bucket e suas credenciais AWS
bucket = # Nome do seu bucket
region_name = # Região em que ele está localizado
aws_access_key_id = # Sua access key
aws_secret_access_key = # Sua secret access key

# Conexão ao S3
s3 = boto3.resource('s3', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
print('Connected to S3')

# Criação do bucket (se ele não existe)
if s3.Bucket(bucket) in s3.buckets.all():
   s3.meta.client.create_bucket(Bucket=bucket)
   print(f'Bucket {bucket} created')
else:
   print(f'Bucket {bucket} is already created')


# Upload da layer Python
s3.meta.client.upload_file('python_layer.zip', bucket, 'lambda_layer/python_layer.zip')
print('Upload com sucesso do arquivo lambda_layer/python.zip')

# Upload do arquivo Person.Person.csv
s3.meta.client.upload_file('Person.Person.csv', bucket, 'Person.Person.csv')
print('Upload com sucesso do arquivo Person.Person.csv')

# Upload do arquivo Production.Product.csv
s3.meta.client.upload_file('Production.Product.csv', bucket, 'Production.Product.csv')
print('Upload com sucesso do arquivo Production.Product.csv')

# Upload do arquivo Sales.Customer.csv
s3.meta.client.upload_file('Sales.Customer.csv', bucket, 'Sales.Customer.csv')
print('Upload com sucesso do arquivo Sales.Customer.csv')

# Upload do arquivo Sales.SpecialOfferProduct.csv
s3.meta.client.upload_file('Sales.SpecialOfferProduct.csv', bucket, 'Sales.SpecialOfferProduct.csv')
print('Upload com sucesso do arquivo Sales.SpecialOfferProduct.csv')

# Upload do arquivo Sales.SalesOrderHeader.csv
s3.meta.client.upload_file('Sales.SalesOrderHeader.csv', bucket, 'Sales.SalesOrderHeader.csv')
print('Upload com sucesso do arquivo ales.SalesOrderHeader.csv')

# Upload do arquivo Sales.SalesOrderDetail.csv
s3.meta.client.upload_file('Sales.SalesOrderDetail.csv', bucket, 'Sales.SalesOrderDetail.csv')
print('Upload com sucesso do arquivo Sales.SalesOrderDetail.csv')
