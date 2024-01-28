# rox-test

<img width="1013" alt="Screenshot 2023-07-24 at 09 54 02" src="https://github.com/leorickli/teste-rox/assets/106999054/939b7226-5b37-4c87-b82f-39973cfdd023">

This is a test from Rox Partner that asks for a cloud infrastructure for engineering/data analysis from a fictitious company that makes bicycles. There is a [brazilian portuguese](https://github.com/leorickli/rox-test/tree/main/portuguese_version) version for this test if you want to read this repository in another language. The test asks for Data Engineering skills to optimize the process. The following items are requested:

1. Do conceptual modeling of the data.
2. Creation of the necessary infrastructure.
3. Creation of all the necessary artifacts to upload the files to the created database.
4. SCRIPT development for data analysis.
5. (optional) Create a report in any data visualization tool.

The AWS platform was used to create the necessary infrastructure because I believe it offers the best solution for the promoted activity. In addition, I do already have experience and the Solutions Architect certification on the platform. The following AWS tools and others were used:

- **RDS:** An RDBMS (Relational Database Management System) tool will be used as it best meets the proposal. The chosen database was MySQL 8.0.33, Single-AZ, db.t3.micro with 20GB of General Purpose SSD storage (gp3), automatic backup, and access with public IP, maintaining the free-tier architecture. The data presented does not have a considerable size so we do not need a robust database in processing to meet the required situation.
- **S3:** It will be created a bucket for the [cleaned files](https://github.com/leorickli/rox-test/tree/main/cleaned_files) that were created based on the raw files provided.
- **Lambda:** We will use Lambda to execute triggers for the PUT commands in S3.
- **IAM:** It will be used to give roles to the Lambda function so that we have access to the S3, CloudWatch, and RDS tools.
- **CloudWatch:** It will be used to check our Lambda function's logs, to check its progress. It is here that we will verify if the triggers are really working after the testing phase inside the Lambda itself.
- **QuickSight:** Used for viewing data through a connection made to the RDS database.
- **Excel:** Used for preliminary data analysis only.
- **Pandas:** It will be used for data cleaning and EDA (Exploratory Data Analysis) of the files provided in the test.
- **DBeaver:** Used to create the on-premises database for testing, create the ERD (Entity Relationship Diagram) for Data Modeling and verify the ingestion of files in RDS.
- **Lucidchart:** Used for the architecture diagram provided in this test.

### Data Cleaning and EDA

An on-premises test environment was created where the data was ingested into a MySQL database to check whether it would accept the data presented in its raw format. A lot of [data cleaning and EDA](https://github.com/leorickli/rox-test/tree/main/cleaning_eda_notebooks) was made to overcome the constraints imposed by the rigid schema of the database created. These files are in .ipynb format so we can see the progress of exploration and data cleaning. Some details about cleaning:

- Files with ";" separators were changed to the traditional "," separators.
- Columns with date and time were properly allocated to the DATETIME format.
- "null" texts (in any variation of uppercase or lowercase) have been removed.
- It was found that there are large lines of text in some columns of the "Person" table, allocating the column to the LONGTEXT format.
- There were cases of repeated values in the primary key for the "SpecialOfferProduct" table, these lines were removed.

### Data Modeling

This is the preliminary diagram that was sent along with the test:

<img width="836" alt="Screenshot 2023-07-28 at 15 28 45" src="https://github.com/leorickli/rox-test/assets/106999054/b13f9b46-7103-4f9c-b7c8-ea7927b95c5c">

According to the diagram, the database will have these tables:

- testeRox
   - Customer
   - Person
   - Product
   - SalesOrderDetail
   - SalesOrderHeader
   - SpecialOfferProduct

By analyzing the .csv files we find the columns and the primary and foreign keys of the tables. A [Python script](https://github.com/leorickli/rox-test/blob/main/create_tables.py) was made for the connection to the MySQL database within RDS so we can execute these [SQL queries](https://github.com/leorickli/rox-test/tree/main/sql_files). These queries are used to create the schema in the MySQL database. It is important to note that, for the Python script to run locally on your machine, it is necessary to update the inbound rules of the security group allocated for the RDS instance by selecting port 3306 (MySQL) and inserting your machine's IP. It is not good practice to use the "0.0.0.0/0" IP as it is too generic, reducing security in your instance. It will also be necessary to create a public IP when creating the instance.

The ERD below shows the relationship between the entities (tables):

<img width="892" alt="Screenshot 2023-07-22 at 10 04 32" src="https://github.com/leorickli/teste-rox/assets/106999054/67ffc189-f23e-414f-b8d1-8766214e370c">

Special attention was needed to the datatypes of certain columns, especially in the columns with dates. A special case is in the Person table, where we find the columns "AdditionalContactInfo" and "Demographics". The LONGTEXT datatype was necessary because there are long lines of text in xml format.

### ETL

A [Python script](https://github.com/leorickli/teste-rox/blob/main/upload_s3.py) was made to upload the [.csv files](https://github.com/leorickli/rox-test/tree/main/cleaned_files) already cleaned through Data Cleaning.

A Lambda function is called through this [Python script](https://github.com/leorickli/rox-test/blob/main/lambda_function.py) each time a file is uploaded to the S3 bucket. This way, every time a file is inserted into the bucket, it will automatically be fed into our RDS database. It was also necessary to implement a [MySQL layer](https://github.com/leorickli/rox-test/blob/main/mysql_layer.zip) with the necessary packages to transform and load the .csv files into the RDS database through the Lambda function. The function timeout was increased because the first ETL was not successful, this action is recommended for when the function tends to process a large number of files, the three seconds that are designated by default across the platform are usually not enough for this type of transformation. Using environment variables inside the Python function to protect personal data is recommended.

<img width="595" alt="Screenshot 2023-07-24 at 09 00 17" src="https://github.com/leorickli/teste-rox/assets/106999054/445149d3-a3bf-479d-b076-3db4251855e3">

With the proper permissions established via IAM, it is possible to monitor the ETL process performed by Lambda through CloudWatch logs. This is great for monitoring the initial tests and the final ingestion of files into the RDS instance after the testing phase.

<img width="1143" alt="Screenshot 2023-07-24 at 09 23 30" src="https://github.com/leorickli/teste-rox/assets/106999054/9a08edcb-2ea1-4ddc-9b39-0b623e0e4e92">

### Data Analysis

Based on the implemented solution, answer the following questions:

1. Write a query that returns the number of rows in the Sales.SalesOrderDetail table by the SalesOrderID field, provided they have at least three rows of details.

```
SELECT 
	SalesOrderID as id, 
	COUNT(*) AS qtd 
FROM testeRox.SalesOrderDetail as sod
GROUP BY SalesOrderID
HAVING qtd >= 3
```

<img width="214" alt="Screenshot 2023-07-24 at 08 40 46" src="https://github.com/leorickli/teste-rox/assets/106999054/3e142ee6-a033-410b-a06b-2e3b49f037a4">


2. Write a query that links the tables Sales.SalesOrderDetail, Sales.SpecialOfferProduct and Production.Product and returns the 3 most sold products (Name) by the sum of OrderQty, grouped by the number of days to manufacture (DaysToManufacture).

```
SELECT * 
FROM(
  SELECT 
  	ROW_NUMBER() OVER(PARTITION BY p.DaysToManufacture ORDER BY sum(sod.OrderQty) DESC) as pos,
  	p.DaysToManufacture AS dtm,
    	p.Name as nome,
    	SUM(sod.OrderQty) AS qtd
  FROM testeRox.SpecialOfferProduct sop 
  JOIN testeRox.Product p ON sop.ProductID = p.ProductID
  JOIN testeRox.SalesOrderDetail sod ON sop.SpecialOfferID = sod.SalesOrderDetailID
  GROUP BY nome, p.DaysToManufacture
  ) as posicao
WHERE pos <= 3
```

<img width="528" alt="Screenshot 2023-07-24 at 08 41 12" src="https://github.com/leorickli/teste-rox/assets/106999054/83f6bd43-ed68-4469-a20f-41b0b31799b1">

3. Write a query linking the Person.Person, Sales.Customer, and Sales.SalesOrderHeader tables to get a list of customer names and a count of orders placed.

```
SELECT
	c.CustomerID AS id,
	CONCAT(p.FirstName, ' ', p.LastName) AS nome, 
	COUNT(*) AS qtd
FROM testeRox.SalesOrderHeader soh
JOIN testeRox.Customer c ON soh.CustomerID = c.CustomerID
JOIN testeRox.Person p ON c.PersonID = p.BusinessEntityID 
GROUP BY c.CustomerID, p.FirstName, p.LastName
ORDER BY qtd DESC;
```

<img width="346" alt="Screenshot 2023-07-24 at 08 42 24" src="https://github.com/leorickli/teste-rox/assets/106999054/e5254176-ea58-490e-93e6-a3c06151801f">

4. Write a query using the tables Sales.SalesOrderHeader, Sales.SalesOrderDetail and Production.Product, to obtain the total sum of products (OrderQty) by ProductID and OrderDate.

```
SELECT
    sod.ProductID AS id,
    p.Name AS nome,
    SUM(sod.OrderQty) AS qtd,
    CAST(soh.OrderDate AS DATE) AS data_pedido
FROM testeRox.SalesOrderDetail sod
JOIN testeRox.SalesOrderHeader soh ON sod.SalesOrderID = soh.SalesOrderID
JOIN testeRox.Product p ON sod.ProductID = p.ProductID
GROUP BY id, nome, data_pedido
ORDER BY data_pedido, qtd DESC;
```

<img width="527" alt="Screenshot 2023-07-26 at 11 45 35" src="https://github.com/leorickli/teste-rox/assets/106999054/8c1fbcd1-dc85-4fc5-bf18-00e8da569364">

5. Write a query showing the SalesOrderID, OrderDate, and TotalDue fields from the Sales.SalesOrderHeader table. Get only the lines where the order was placed during September/2011 and the total due is above 1,000. Sort by descending total due.
```
SELECT 
	SalesOrderID as id,
	CAST(OrderDate AS DATE) AS data, 
	TotalDue AS total_devido
FROM testeRox.SalesOrderHeader
WHERE OrderDate BETWEEN '2011-09-01' AND '2011-09-30' AND TotalDue > 1000
ORDER BY total_devido;
```
*In this case, the query did not return any values because there is no data in this proposed interval.*

<img width="362" alt="Screenshot 2023-07-24 at 08 44 47" src="https://github.com/leorickli/teste-rox/assets/106999054/e5ec5004-9ce2-4a83-ab5a-61d51649e492">

### Data Visualization

Using AWS QuickSight and making sure that the proper permissions are granted to IAM through roles and VPC alignment, we can use it to connect to RDS and generate dashboards. Below are some visualizations.

<img width="760" alt="Screenshot 2023-07-24 at 10 45 08" src="https://github.com/leorickli/teste-rox/assets/106999054/f743d1d2-4db3-432c-98e1-d3cd3adb73a9">
<img width="777" alt="Screenshot 2023-07-24 at 10 49 45" src="https://github.com/leorickli/teste-rox/assets/106999054/acbc55d7-964b-48f5-9611-d50bc567d3f1">

### Other Architectures

In the conception of the project and in the course of the processes, some proposals for different approaches and architectures emerged that could be discussed and/or perhaps addressed in the future. Below are some of these approaches:

1. When testing the on-premises data transfer to the MySQL database in the RDS instance, there is the possibility of directly transferring the on-premises files to the existing database in the cloud. This measure is not viable because the data transfer is very slow, it requires a schema to already be established in the database and the architecture is poor, making future automation and improvements unfeasible.
2. In the AWS documentation, it was suggested to back up the on-premises database using Percona's XtraBackup tool. This measure may be feasible in the event of a direct transfer from the on-premises database to the cloud.
3. After designing this project, it is possible to create a template in the CloudFormation tool to automate the creation of the stack used in this repository.
4. It is possible that the data ingestion of objects (.csv files) within S3 is done by the AWS Glue tool for performing ETL. Subsequently, this processed data is sent to AWS Athena for data analysis. Athena is easily connected to Tableau for data visualization in addition to QuickSight.
