CREATE TABLE IF NOT EXISTS Sales.Customer
(
CustomerID INT(5) NOT NULL,
PersonID INT(7),
StoreID INT(6),
TerritoryID INT(2),
AccountNumber VARCHAR(10),
rowguid VARCHAR(36),
ModifiedDate DATETIME,
PRIMARY KEY (CustomerID),
FOREIGN KEY (PersonID) REFERENCES Person.Person(BusinessEntityID)
)