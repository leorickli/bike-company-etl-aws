CREATE TABLE IF NOT EXISTS testeRox.Person
(
BusinessEntityID INT NOT NULL,
PersonType VARCHAR(255),
NameStyle INT,
Title VARCHAR(255),
FirstName VARCHAR(255),
MiddleName VARCHAR(255),
LastName VARCHAR(255),
Suffix VARCHAR(255),
EmailPromotion INT,
AdditionalContactInfo LONGTEXT,
Demographics LONGTEXT,
rowguid VARCHAR(255),
ModifiedDate DATETIME,
PRIMARY KEY(BusinessEntityID)
)