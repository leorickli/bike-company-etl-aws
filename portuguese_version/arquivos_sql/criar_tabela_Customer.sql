CREATE TABLE IF NOT EXISTS testeRox.Customer
(
CustomerID INT NOT NULL,
PersonID VARCHAR(255),
StoreID DOUBLE,
TerritoryID INT,
AccountNumber VARCHAR(255),
rowguid VARCHAR(255),
ModifiedDate DATETIME,
PRIMARY KEY (CustomerID)
)