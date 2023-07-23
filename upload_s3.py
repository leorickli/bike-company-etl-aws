import boto3


# Nome do bucket e suas credenciais AWS
bucket = # Bucket onde estão os arquivos .csv
region_name = # Região do projeto
aws_access_key_id = # Access key da sua conta AWS
aws_secret_access_key = # Secret acess key da sua conta AWS

# Conexão ao S3
s3 = boto3.resource('s3', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
print('Connected to S3')

# Criação do bucket (se ele não existe)
if s3.Bucket(bucket) in s3.buckets.all():
   s3.meta.client.create_bucket(Bucket=bucket)
   print(f'Bucket {bucket} criada')
else:
   print(f'Bucket {bucket} já foi criada anteriormente')

# Upload do arquivo Customer.csv
s3.meta.client.upload_file('Customer.csv', bucket, 'Customer.csv')
print('Upload com sucesso do arquivo Customer.csv')

# Upload do arquivo Person.csv
s3.meta.client.upload_file('Person.csv', bucket, 'Person.csv')
print('Upload com sucesso do arquivo Person.csv')

# Upload do arquivo Product.csv
s3.meta.client.upload_file('Product.csv', bucket, 'Product.csv')
print('Upload com sucesso do arquivo Product.csv')

# Upload do arquivo SalesOrderDetail.csv
s3.meta.client.upload_file('SalesOrderDetail.csv', bucket, 'SalesOrderDetail.csv')
print('Upload com sucesso do arquivo SalesOrderDetail.csv')

# Upload do arquivo SalesOrderHeader.csv
s3.meta.client.upload_file('SalesOrderHeader.csv', bucket, 'SalesOrderHeader.csv')
print('Upload com sucesso do arquivo SalesOrderHeader.csv')

# Upload do arquivo SpecialOfferProduct.csv
s3.meta.client.upload_file('SpecialOfferProduct.csv', bucket, 'SpecialOfferProduct.csv')
print('Upload com sucesso do arquivo SpecialOfferProduct.csv')
