CREATE LOGIN adminPy WITH PASSWORD = '123'
USE SmartParkingLotSystem;
CREATE USER adminPy FOR LOGIN adminPy;

ALTER ROLE db_owner ADD MEMBER adminPy;