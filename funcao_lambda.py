import boto3
import os
import csv
import mysql.connector
s3_client = boto3.client('s3')

def lambda_handler(event):
    # Credenciais MySQL RDS
    host = os.environ.get('host')
    user = os.environ.get('user')
    password = os.environ.get('password')
    database = os.environ.get('database')
    
    for record in event['Records']:
        # Extract information about the S3 object
        bucket = record['s3']['bucket']['name']
        csv_file = record['s3']['object']['key']
        
        # Check if the file is a CSV file
        if csv_file.lower().endswith('.csv'):
            # Read the CSV file from S3
            csv_file_obj = s3_client.get_object(Bucket=bucket, Key=csv_file)
            lines = csv_file_obj['Body'].read().decode('utf-8').splitlines()
            
            # Get the table name from the CSV file name
            table_name = csv_file[:-4]  # Remove the '.csv' extension
            
            # Process the CSV data and prepare it for insertion
            results = []
            for row in csv.DictReader(lines):
                results.append(list(row.values()))
            
            # Establish a connection to the MySQL RDS database
            mydb = mysql.connector.connect(host=host, user=user, password=password, database=database)
            
            # Create the INSERT query based on the table name
            mysql_insert_query = f"INSERT INTO {table_name} ({', '.join(row.keys())}) VALUES ({', '.join(['%s']*len(row))})"
            
            # Execute the INSERT query for the current CSV file's data
            cursor = mydb.cursor()
            cursor.executemany(mysql_insert_query, results)
            mydb.commit()
            print(f"{cursor.rowcount} records inserted successfully into {table_name} table")
            
            # Close the cursor and database connection
            cursor.close()
            mydb.close()
