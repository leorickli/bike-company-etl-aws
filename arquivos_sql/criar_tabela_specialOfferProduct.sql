CREATE TABLE IF NOT EXISTS Sales.SpecialOfferProduct
(
SpecialOfferID INT(2) NOT NULL,
ProductID INT(3) NOT NULL,
rowguid VARCHAR(36),
ModifiedDate DATETIME,
PRIMARY KEY (SpecialOfferID, ProductID),
FOREIGN KEY (ProductID) REFERENCES Production.Product(ProductID)
)