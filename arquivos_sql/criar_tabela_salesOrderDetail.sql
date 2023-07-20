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