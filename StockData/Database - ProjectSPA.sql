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
Post_Time		timestamp,
Logg_Time		timestamp DEFAULT(getdate()),

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
);l