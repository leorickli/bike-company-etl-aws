CREATE TABLE IF NOT EXISTS testeRox.SalesOrderDetail
(
SalesOrderID INT,
SalesOrderDetailID INT NOT NULL,
CarrierTrackingNumber VARCHAR(255),
OrderQty INT,
ProductID INT,
SpecialOfferID INT,
UnitPrice FLOAT,
UnitPriceDiscount FLOAT,
LineTotal FLOAT,
rowguid VARCHAR(255),
ModifiedDate DATETIME,
PRIMARY KEY (SalesOrderDetailID)
)