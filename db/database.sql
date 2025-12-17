--DROP DATABASE SmartParkingLotSystem;
CREATE DATABASE SmartParkingLotSystem;

USE SmartParkingLotSystem;

CREATE TABLE [cameras] (
  [id] bigint PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [source_type] varchar(10),
  [rtsp_url] varchar(255),
  [file_path] varchar(255),
  [description] varchar(255),
  [created_at] datetime NOT NULL DEFAULT GETDATE(),
  [updated_at] datetime NOT NULL DEFAULT GETDATE()
)

CREATE TABLE [vehicles] (
  [id] bigint PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [vehicle_type] varchar(100),
  [plate_number] varchar(20),
  [created_at] datetime NOT NULL DEFAULT GETDATE(),
  [updated_at] datetime NOT NULL DEFAULT GETDATE()
)

CREATE TABLE [alpr_logs] (
  [id] bigint PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [camera_id] bigint,
  [vehicle_id] bigint NOT NULL,
  [detected_at] datetime NOT NULL DEFAULT GETDATE(),
  [image_path] varchar(255) NOT NULL DEFAULT GETDATE()
)

CREATE TABLE [monthly_cards] (
  [id] bigint PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [card_code] varchar(10) NOT NULL,
  [customer_id] bigint,
  [vehicle_id] bigint NOT NULL,
  [monthly_fee] int,
  [start_date] date,
  [expiry_date] date,
  [is_paid] bit,
  [is_active] bit NOT NULL DEFAULT 1,
  [created_at] datetime NOT NULL DEFAULT GETDATE(),
  [updated_at] datetime NOT NULL DEFAULT GETDATE()
)

CREATE TABLE [customers] (
  [id] bigint PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [full_name] nvarchar(100),
  [phone_number] varchar(20) UNIQUE,
  [email] varchar(50),
  [created_at] datetime NOT NULL DEFAULT GETDATE(),
  [updated_at] datetime NOT NULL DEFAULT GETDATE()
)

CREATE TABLE [cards] (
  [id] bigint PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [card_code] varchar(10) NOT NULL,
  [price] INT,
  [created_at] datetime NOT NULL DEFAULT GETDATE(),
  [updated_at] datetime NOT NULL DEFAULT GETDATE(),
  [is_active] bit NOT NULL DEFAULT 1,
  [created_by] bigint
)


CREATE TABLE card_logs (
  id BIGINT PRIMARY KEY IDENTITY,
  card_id BIGINT NOT NULL,
  vehicle_id BIGINT NOT NULL,
  entry_at DATETIME NOT NULL DEFAULT GETDATE(),
  exit_at DATETIME,
  fee INT,
  created_by BIGINT,
  closed_by BIGINT,
);

CREATE TABLE [vehicle_cards] (
  [id] bigint PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [vehicle_id] bigint NOT NULL,
  [card_id] bigint NOT NULL,
  [created_at] datetime NOT NULL DEFAULT GETDATE(),
  [updated_at] datetime NOT NULL DEFAULT GETDATE()
)

CREATE TABLE [staffs] (
  [id] bigint PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [fullname] nvarchar(100),
  [phone_number] varchar(20),
  [username] varchar(50) UNIQUE,
  [password] varchar(255),
  [role] int,
  [created_at] datetime NOT NULL DEFAULT GETDATE(),
  [updated_at] datetime NOT NULL DEFAULT GETDATE()
)

CREATE TABLE [payments] (
  [id] bigint PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [card_id] bigint,
  [monthly_card_id] bigint,
  [amount] int,
  [payment_date] datetime,
  [method] varchar(20),
  [processed_by] bigint,
  [created_at] datetime NOT NULL DEFAULT GETDATE(),
  [updated_at] datetime NOT NULL DEFAULT GETDATE()
)

ALTER TABLE [cards] ADD FOREIGN KEY ([created_by]) REFERENCES [staffs] ([id])

ALTER TABLE [payments] ADD FOREIGN KEY ([processed_by]) REFERENCES [staffs] ([id])

ALTER TABLE [alpr_logs] ADD FOREIGN KEY ([camera_id]) REFERENCES [cameras] ([id])

ALTER TABLE [alpr_logs] ADD FOREIGN KEY ([vehicle_id]) REFERENCES [vehicles] ([id])

ALTER TABLE [monthly_cards] ADD FOREIGN KEY ([customer_id]) REFERENCES [customers] ([id])

ALTER TABLE [monthly_cards] ADD FOREIGN KEY ([vehicle_id]) REFERENCES [vehicles] ([id])

ALTER TABLE [payments] ADD FOREIGN KEY ([monthly_card_id]) REFERENCES [monthly_cards] ([id])

ALTER TABLE [card_logs] ADD FOREIGN KEY ([vehicle_id]) REFERENCES [vehicles] ([id])
GO

ALTER TABLE [card_logs] ADD FOREIGN KEY ([card_id]) REFERENCES [cards] ([id])
GO

ALTER TABLE [payments] ADD FOREIGN KEY ([card_id]) REFERENCES [cards] ([id])
