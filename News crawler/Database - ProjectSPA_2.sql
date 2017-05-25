use master;

if db_id('ProjectSPA_2') is not null
  drop database ProjectSPA_2; 
go

create DATABASE ProjectSPA_2
go

use ProjectSPA_2
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
Stock_Time		bigint,
Closing			varchar(255),
High			varchar(255),
Low				varchar(255),
Stock_Open		varchar(255),
Volume			varchar(255),
Loggtime		datetime DEFAULT(getdate()),

Constraint PK_Data
	primary key(Stock_ID, Stock_Time),

Constraint FK_Data
	foreign key(Stock_ID)
	references Stock(Stock_ID)
);
GO

create table NewsArticle(
Article_ID		int identity(1, 1),
Title			varchar(255),
Article_Descr	text,
Content			text,
Author			varchar(255),
Link			varchar(255),
Post_Time		smalldatetime,
Logg_Time		smalldatetime,

Constraint PK_NewsArticle
	primary key(Article_ID)
);

create table StockArticle(
Article_ID		int,
Stock_ID		int,

Constraint PK_StockArticle
	primary key(Article_ID, Stock_ID),

Constraint FK_StockArticle_Stock
	foreign key(Stock_ID)
	references Stock(Stock_ID),

Constraint FK_StockArticle_NewsArticle
	foreign key (Article_ID)
	references NewsArticle(Article_ID)
);

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

 

IF EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'spAddNews') 
   DROP PROCEDURE spAddNews 
GO 

CREATE PROCEDURE spAddNews
( 
   --@Article_ID	Integer,
   @Title		Varchar(255),
   @Article_Descr	Varchar(255),
   @Content		Varchar(255),
   @Author		Varchar(255),
   @Link		Varchar(255),
   @Post_Time	smalldatetime
   --@Logg_Time	smalldatetime

) 
AS 
BEGIN 

INSERT INTO NewsArticle(Title, Article_Descr, Content, Author, Link, Post_Time, Logg_Time)
VALUES		(@Title, @Article_Descr, @Content, @Author, @Link, @Post_Time, getdate())



IF @@ERROR <> 0
		BEGIN TRANSACTION

		ROLLBACK 
		RAISERROR ('Er is een fout opgetreden.', 16, 1) 
		RETURN 
	COMMIT

END
GO

IF EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'spNewsToStock') 
   DROP PROCEDURE spNewsToStock 
GO 

CREATE PROCEDURE spNewsToStock
( 
   @Article_ID	Integer,
   @Stock_ID	Integer

) 
AS 
BEGIN 

INSERT INTO StockArticle(Stock_ID, Article_ID)
VALUES		(@Stock_ID, @Article_ID)

IF @@ERROR <> 0
		BEGIN TRANSACTION

		ROLLBACK 
		RAISERROR ('Er is een fout opgetreden.', 16, 1) 
		RETURN 
	COMMIT

END
GO