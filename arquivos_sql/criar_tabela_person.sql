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