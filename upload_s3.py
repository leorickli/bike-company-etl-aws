import boto3

# AWS Bucket name and credentials
bucket = # Enter the name of the bucket where the .csv files are stored
region_name = # Enter the AWS region of your project
aws_access_key_id = # Enter your AWS access key ID
aws_secret_access_key = # Enter your AWS secret access key

# Connect to S3
s3 = boto3.resource('s3', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
print('Connected to S3')

# Create the bucket (if it does not exist)
if s3.Bucket(bucket) not in s3.buckets.all():
    s3.meta.client.create_bucket(Bucket=bucket)
    print(f'Bucket {bucket} created')
else:
    print(f'Bucket {bucket} already exists')

# Upload the Customer.csv file
s3.meta.client.upload_file('Customer.csv', bucket, 'Customer.csv')
print('Successfully uploaded Customer.csv file')

# Upload the Person.csv file
s3.meta.client.upload_file('Person.csv', bucket, 'Person.csv')
print('Successfully uploaded Person.csv file')

# Upload the Product.csv file
s3.meta.client.upload_file('Product.csv', bucket, 'Product.csv')
print('Successfully uploaded Product.csv file')

# Upload the SalesOrderDetail.csv file
s3.meta.client.upload_file('SalesOrderDetail.csv', bucket, 'SalesOrderDetail.csv')
print('Successfully uploaded SalesOrderDetail.csv file')

# Upload the SalesOrderHeader.csv file
s3.meta.client.upload_file('SalesOrderHeader.csv', bucket, 'SalesOrderHeader.csv')
print('Successfully uploaded SalesOrderHeader.csv file')

# Upload the SpecialOfferProduct.csv file
s3.meta.client.upload_file('SpecialOfferProduct.csv', bucket, 'SpecialOfferProduct.csv')
print('Successfully uploaded SpecialOfferProduct.csv file')
