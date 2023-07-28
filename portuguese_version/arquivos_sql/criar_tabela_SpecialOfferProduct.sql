CREATE TABLE IF NOT EXISTS testeRox.SpecialOfferProduct
(
SpecialOfferID INT,
ProductID INT NOT NULL,
rowguid VARCHAR(255),
ModifiedDate DATETIME,
PRIMARY KEY (ProductID)
)