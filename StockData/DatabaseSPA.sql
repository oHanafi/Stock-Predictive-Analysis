use master;

if db_id('DatabaseSPA') is not null
  drop database DatabaseSPA; 
go

create DATABASE DatabaseSPA
go

use DatabaseSPA
go

create table Stock (
Stock_ID		Int,
Short		Varchar(50) not null,
Stock_Description Varchar(255),

Constraint PK_Stock
	primary key(Stock_ID)

);

create table Data (
Stock_ID		Int,
Stock_Time		Time,
Closing		Varchar(255),
High	 varchar(255),
Low	 varchar(255),
Stock_Open	 varchar(255),
Volume	 varchar(255),

Constraint PK_Data
	primary key(Stock_ID, Stock_Time),

Constraint FK_Data
	foreign key(Stock_ID)
	references Stock(Stock_ID)
);
GO

IF EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'spAddStock') 
   DROP PROCEDURE spAddStock 
GO 

CREATE PROCEDURE spAddStock
( 
   @Closing		Varchar(255),
   @High		Varchar(255),
   @Low		Varchar(255),
   @Open		Varchar(255),
   @Volume		Varchar(255)
) 
AS 
BEGIN 
DECLARE @Stock_ID integer

SELECT @Stock_ID = Max(Stock_ID)+1
FROM Stock

INSERT INTO Data(Stock_ID, Stock_Time, Closing,High,Low,Stock_Open,Volume)
VALUES		(@Stock_ID, CURRENT_TIMESTAMp, @Closing, @High, @Low, @Open, @Volume)


IF @@ERROR <> 0
		BEGIN TRANSACTION

		ROLLBACK 
		RAISERROR ('Er is een fout opgetreden.', 16, 1) 
		RETURN 
	COMMIT

END
GO
