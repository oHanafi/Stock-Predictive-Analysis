use master;

if db_id('ProjectSPA') is not null
  drop database ProjectSPA; 
go

create DATABASE ProjectSPA
go

use ProjectSPA
go

create table Stock (
Stock_ID		int identity(1, 1),
Short			varchar(50) not null,
Stock_Desc		varchar(255),

Constraint PK_Stock
	primary key(Stock_ID)

);

create table StockAlias (
Alias_ID		int identity(1,1),
Name			varchar(50),
Stock_ID		int,

Constraint PK_Alias
	primary key(Alias_ID),

Constraint FK_Stock_ID
	foreign key(Stock_ID)
	references Stock(Stock_ID)
);

create table StockData (
Stock_ID		int,
Stock_Time		varchar(255),
Closing			varchar(255),

Constraint PK_Data
	primary key(Stock_ID, Stock_Time),

Constraint FK_Data
	foreign key(Stock_ID)
	references Stock(Stock_ID)
);


create table NewsArticle(
Article_ID		int identity(1, 1),
Stock_ID		int,
Title			varchar(255)not null,
Content			text not null,
Author			varchar(255),
Link			varchar(255)not null,
Post_Time		datetime,
Logg_Time		datetime,
Polarity		decimal(3,2),
Subjectivity	decimal(3,2),

Constraint PK_NewsArticle
	primary key(Article_ID, Stock_ID,Link),

Constraint FK_Stock_Article
	foreign key(Stock_ID)
	references Stock(Stock_ID)

);
GO
--Insert companies
INSERT INTO STOCK(Short, Stock_Desc) VALUES ('AAPL', 'APPLE INC.');
INSERT INTO STOCK(Short, Stock_Desc) VALUES ('MSFT', 'APPLE CORPORATION');
INSERT INTO STOCK(Short, Stock_Desc) VALUES ('GOOG', 'ALPHABET INC. (GOOGLE)');
INSERT INTO STOCK(Short, Stock_Desc) VALUES ('TSLA', 'TESLA INC.');
INSERT INTO STOCK(Short, Stock_Desc) VALUES ('AMD', 'ADVANCED MICRO DEVICES');
INSERT INTO STOCK(Short, Stock_Desc) VALUES ('INTC', 'INTEL CORPORATION');
INSERT INTO STOCK(Short, Stock_Desc) VALUES ('NVDA', 'NVIDIA CORPORATION');
INSERT INTO STOCK(Short, Stock_Desc) VALUES ('QCOM', 'QUALCOMM, INC.');
INSERT INTO STOCK(Short, Stock_Desc) VALUES ('NXPI', 'NXP SEMICONDUCTORS NV');
INSERT INTO STOCK(Short, Stock_Desc) VALUES ('ASML', 'ASML');
INSERT INTO STOCK(Short, Stock_Desc) VALUES ('HPQ', 'HP INC.');

 