# teste-rox

Este é um teste da Rox Partner que pede uma infraestrutura na nuvem para engenharia/análise de dados de uma empresa fictícia que produz bicicletas. O teste pede habilidades de Engenharia de Dados para otimizar o processo. Os seguintes itens são solicitados:

1.	Fazer a modelagem conceitual dos dados;
2.	Criação da infraestrutura necessária;
3.	Criação de todos os artefatos necessários para carregar os arquivos para o banco criado;
4.	Desenvolvimento de SCRIPT para análise de dados;
5.	(opcional) Criar um relatório em qualquer ferramenta de visualização de dados.

Foi utilizada a plataforma AWS para criar a infraestrutura necessária pois creio oferecer a melhor solução para a atividade promovida, além de já possuir experiência e certificação Solutions Architect na plataforma. Foram utilizadas as seguintes ferramentas da AWS:

- RDS: Será utilizada uma ferramenta de RDBMS (Sistema de gerenciamento de base de dados relacionais) pois atende melhor à proposta. O banco de dados escolhido foi o MySQL 8.0.33, Single-AZ, db.t3.micro com 20GB de armazenamento General Purpose SSD (gp3), backup automático e acesso com IP público, mantendo nossa arquitetura no free-tier. Os dados apresentados não possuem um tamanho considerável então não precisamos de uma base de dados robusta em processamento para atender a situação.
- S3: Será criado um bucket para armazenar os [arquivos](https://github.com/leorickli/teste_rox/tree/main/arquivos_csv) fornecidos para o teste.
- Lambda: Utilizaremos Lambda para executarmos triggers para as ações de PUT no S3.
- Pandas: Será utilizado apenas para EDA (Análise Exploratória de Dados) básica.

Foi feita uma pequena EDA nos arquivos .csv fornecidos para contextualização dos dados fornecidos e para analisasr se há a necessidade de uma limpeza prévia nos mesmos.

--- INSERIR OS DADOS AQUI

Não foi encontrada a necessidade de limpeza ou problemas com relação à governança de dados. 

### Fazer a modelagem conceitual dos dados

De acordo com a topologia enviada juntamente com a documentação do teste, as databases foram divididas entre "Person", "Production" e "Sales". A modelagem foi feita da seguinte maneira:

1. Person
   - Person
2. Production
   - Product
3. Sales
   - Customer
   - SalesOrderDetail
   - SalesOrderHeader
   - SpecialOfferProduct

Analisando os arquivos .csv, encontramos as colunas, primary e foreign keys das tabelas. Foi feito um [script Python](https://github.com/leorickli/teste-rox/blob/main/criar_tabelas.py) para a conexão com a base de dados MySQL dentro da RDS para podermos executar as queries [neste repositório](https://github.com/leorickli/teste-rox/tree/main/arquivos_sql). Importante notar que, para que o script Python seja executado localmente em sua máquina, é necessário atualizarmos as inbound rules do security group alocado para a instância RDS, selecionando a porta 3306 (MySQL) e inserindo o IP de sua máquina. Não é boa prática utilizar o IP "0.0.0.0/0" pois ele é muito genérico, reduzindo a segurança em sua instância. Far-se-á também necessária a criação de um IP público no momento de criação da instância.

```
CREATE DATABASE IF NOT EXISTS Person
```

```
CREATE DATABASE IF NOT EXISTS Production
```

```
CREATE DATABASE IF NOT EXISTS Sales
```

```
CREATE TABLE IF NOT EXISTS Person.Person
(
BusinessEntityID INT(5) NOT NULL,
PersonType VARCHAR(2),
NameStyle INT(1),
Title VARCHAR(4),
FirstName VARCHAR(4),
MiddleName VARCHAR(16),
LastName VARCHAR(22),
Suffix VARCHAR(3),
EmailPromotion INT(1),
AdditionalContactInfo VARCHAR(1611),
Demographics VARCHAR(623),
rowguid VARCHAR(36),
ModifiedDate DATETIME,
PRIMARY KEY(BusinessEntityID)
)
```

```
CREATE TABLE IF NOT EXISTS Production.Product
(
ProductID INT(3) NOT NULL,
Name VARCHAR(32),
ProductNumber VARCHAR(10),
MakeFlag INT(1),
FinishedGoodsFlag INT(1),
Color VARCHAR(12),
SafetyStockLevel INT(4),
ReorderPoint INT(3),
StandardCost FLOAT(9),
ListPrice FLOAT(7),
Size VARCHAR(3),
SizeUnitMeasureCode VARCHAR(3),
WeightUnitMeasureCode VARCHAR(3),
Weight FLOAT(6),
DaysToManufacture INT(1),
ProductLine VARCHAR(3),
Class VARCHAR(3),
Style VARCHAR(3),
ProductSubcategoryID INT(4),
ProductModelID INT(5),
SellStartDate DATE,
SellEndDate DATE,
DiscontinuedDate DATE,
rowguid VARCHAR(36),
ModifiedDate DATETIME,
PRIMARY KEY (ProductID)
)
```

```
CREATE TABLE IF NOT EXISTS Sales.Customer
(
CustomerID INT(5) NOT NULL,
PersonID INT(7),
StoreID INT(6),
TerritoryID INT(2),
AccountNumber VARCHAR(10),
rowguid VARCHAR(36),
ModifiedDate DATETIME,
PRIMARY KEY (CustomerID)
FOREIGN KEY (PersonID) REFERENCES Person.Person(BusinessEntityID)
)
```

```
CREATE TABLE IF NOT EXISTS Sales.SalesOrderDetail
(
SalesOrderID INT(5) NOT NULL,
SalesOrderDetailID INT(6) NOT NULL,
CarrierTrackingNumber VARCHAR(12),
OrderQty INT(2),
ProductID INT(3),
SpecialOfferID INT(2),
UnitPrice FLOAT,
UnitPriceDiscount FLOAT,
LineTotal FLOAT,
rowguid VARCHAR(36),
ModifiedDate DATETIME,
PRIMARY KEY (SalesOrderID, SalesOrderDetailID),
FOREIGN KEY (SalesOrderID) REFERENCES Sales.SalesOrderHeader(SalesOrderID),
FOREIGN KEY (SpecialOfferID) REFERENCES Sales.SpecialOfferProduct(SpecialOfferID),
FOREIGN KEY (ProductID) REFERENCES Production.Product(ProductID)
)
```

```
CREATE TABLE IF NOT EXISTS Sales.SalesOrderHeader
(
SalesOrderID INT(5) NOT NULL,
RevisionNumber INT(1),
OrderDate DATE,
DueDate DATE,
ShipDate DATE,
Status INT(1),
OnlineOrderFlag INT(1),
SalesOrderNumber VARCHAR(7),
PurchaseOrderNumber VARCHAR(13),
AccountNumber VARCHAR(14),
CustomerID INT(5),
SalesPersonID INT(5),
TerritoryID INT(2),
BillToAddressID INT(5),
ShipToAddressID INT(5),
ShipMethodID INT(1),
CreditCardID INT(7),
CreditCardApprovalCode VARCHAR(15),
CurrencyRateID INT(7),
SubTotal FLOAT,
TaxAmt FLOAT,
Freight FLOAT,
TotalDue FLOAT,
Comment VARCHAR(3),
rowguid VARCHAR(36),
ModifiedDate DATETIME,
PRIMARY KEY (SalesOrderID),
FOREIGN KEY (CustomerID) REFERENCES Sales.Customer(CustomerID)
)
```

```
CREATE TABLE IF NOT EXISTS Sales.SpecialOfferProduct
(
SpecialOfferID INT(2) NOT NULL,
ProductID INT(3) NOT NULL,
rowguid VARCHAR(36),
ModifiedDate DATETIME,
PRIMARY KEY (SpecialOfferID, ProductID),
FOREIGN KEY (ProductID) REFERENCES Production.Product(ProductID)
)
```

