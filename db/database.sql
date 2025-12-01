--DROP DATABASE SmartParkingLotSystem;
CREATE DATABASE SmartParkingLotSystem;

USE SmartParkingLotSystem;

CREATE TABLE [cameras] (
  [id] bigint PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [source_type] varchar(10),
  [rtsp_url] varchar(255),
  [file_path] varchar(255),
  [description] varchar(255),
  [created_at] datetime,
  [updated_at] datetime
)
GO

CREATE TABLE [vehicles] (
  [id] bigint PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [plate_number] varchar(20),
  [created_at] datetime,
  [updated_at] datetime
)
GO

CREATE TABLE [alpr_logs] (
  [id] bigint PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [camera_id] bigint,
  [vehicle_id] bigint NOT NULL,
  [detected_at] datetime,
  [image_path] varchar(255)
)
GO

CREATE TABLE [monthly_cards] (
  [id] bigint PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [customer_id] bigint,
  [vehicle_id] bigint NOT NULL,
  [price] int,
  [start_date] date,
  [end_date] date,
  [active] bit,
  [created_at] datetime,
  [updated_at] datetime
)
GO

CREATE TABLE [customers] (
  [id] bigint PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [full_name] varchar(100),
  [phone_number] varchar(20) UNIQUE,
  [email] varchar(50)
)
GO

CREATE TABLE [cards] (
  [id] bigint PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [vehicle_id] bigint NOT NULL,
  [card_type] varchar(10),
  [entry_time] datetime,
  [exit_time] datetime,
  [fee] int,
  [created_at] datetime,
  [updated_at] datetime,
  [created_by] bigint,
  [closed_by] bigint
)
GO

CREATE TABLE [vehicle_cards] (
  [id] bigint PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [vehicle_id] bigint NOT NULL,
  [card_id] bigint NOT NULL
)
GO

CREATE TABLE [staffs] (
  [id] bigint PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [username] varchar(50) UNIQUE,
  [password] varchar(255),
  [fullname] varchar(100),
  [phone_number] varchar(20),
  [role] int,
  [created_at] datetime,
  [updated_at] datetime
)
GO

CREATE TABLE [payments] (
  [id] bigint PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [card_id] bigint,
  [monthly_card_id] bigint,
  [amount] int,
  [payment_date] datetime,
  [method] varchar(20),
  [processed_by] bigint
)
GO

ALTER TABLE [cards] ADD FOREIGN KEY ([created_by]) REFERENCES [staffs] ([id])
GO

ALTER TABLE [cards] ADD FOREIGN KEY ([closed_by]) REFERENCES [staffs] ([id])
GO

ALTER TABLE [payments] ADD FOREIGN KEY ([processed_by]) REFERENCES [staffs] ([id])
GO

ALTER TABLE [alpr_logs] ADD FOREIGN KEY ([camera_id]) REFERENCES [cameras] ([id])
GO

ALTER TABLE [alpr_logs] ADD FOREIGN KEY ([vehicle_id]) REFERENCES [vehicles] ([id])
GO

ALTER TABLE [monthly_cards] ADD FOREIGN KEY ([customer_id]) REFERENCES [customers] ([id])
GO

ALTER TABLE [monthly_cards] ADD FOREIGN KEY ([vehicle_id]) REFERENCES [vehicles] ([id])
GO

ALTER TABLE [payments] ADD FOREIGN KEY ([monthly_card_id]) REFERENCES [monthly_cards] ([id])
GO

ALTER TABLE [vehicle_cards] ADD FOREIGN KEY ([vehicle_id]) REFERENCES [vehicles] ([id])
GO

ALTER TABLE [vehicle_cards] ADD FOREIGN KEY ([card_id]) REFERENCES [cards] ([id])
GO

ALTER TABLE [payments] ADD FOREIGN KEY ([card_id]) REFERENCES [cards] ([id])
GO
