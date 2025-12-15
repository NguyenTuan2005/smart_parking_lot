USE SmartParkingLotSystem;
--1. STAFFS
SET IDENTITY_INSERT staffs ON;
INSERT INTO staffs (id, username, password, fullname, phone_number, role) VALUES
(1, 'admin', '123', 'Nguyen Van A', '0901000001', 1),
(2, 'employee', '123', 'Nguyen Van B', '0901000002', 2),
(3, 'tuan', '123', 'Nguyen Vo Quoc Tuan', '0901000002', 1),
(4, 'chi', '123', 'Chi', '0901000003', 1),
(5, 'hoang', '123', 'Phan Ba Huy Hoang', '0901000003', 2),
(6, 'tri', '123', 'Trí', '0901000003', 2);
SET IDENTITY_INSERT staffs OFF;


SET IDENTITY_INSERT vehicles ON;
INSERT INTO vehicles (id, vehicle_type, plate_number) VALUES
(1,'Xe máy','59X1-11111'),
(2,'Xe máy','59X1-22222'),
(3,'Xe máy','59X1-33333'),
(4,'Xe máy','51A-11111'),
(5,'Xe máy','51A-22222'),
(6,'Xe máy','51A-33333'),
(7,'Xe máy','60C-11111'),
(8,'Xe máy','60C-22222'),
(9,'Xe máy','62X1-44444'),
(10,'Xe máy','61A-55555');
SET IDENTITY_INSERT vehicles OFF;


SET IDENTITY_INSERT customers ON;
INSERT INTO customers (id, full_name, phone_number, email) VALUES
(1,N'Nguyễn Minh Tài','0911111111','tfc1@gmail.com'),
(2,N'Trần Minh Hi','0911111112','tav2@gmail.com'),
(3,N'Lê Minh Khôi','0911111113','lmk3@gmail.com'),
(4,N'Phạm Minh Linh','0911111114','phm4@gmail.com'),
(5,N'Hoàng Minh Mẫn','0911111115','hmm5@gmail.com'),
(6,N'Vũ Minh Nhật','0911111116','vmn6@gmail.com'),
(7,N'Đặng Minh Phương','0911111117','dmph7@gmail.com'),
(8,N'Ngô Minh Quân','0911111118','nmq8@gmail.com'),
(9,N'Bùi Minh Đức','0911111119','bmd9@gmail.com'),
(10,N'Đỗ Minh Sang','0911111120','dms10@gmail.com');
SET IDENTITY_INSERT customers OFF;


SET IDENTITY_INSERT monthly_cards ON;
INSERT INTO monthly_cards (id, card_code, customer_id, vehicle_id, monthly_fee, start_date, expiry_date, is_paid) VALUES
(1,'CM0001',1,1,150000,'2025-01-01','2025-01-31',1),
(2,'CM0002',2,2,150000,'2025-01-01','2025-01-31',1),
(3,'CM0003',3,3,150000,'2025-01-01','2025-01-31',0),
(4,'CM0004',4,4,150000,'2025-01-01','2025-01-31',1),
(5,'CM0005',5,5,150000,'2025-01-01','2025-01-31',1),
(6,'CM0006',6,6,150000,'2025-01-01','2025-01-31',0),
(7,'CM0007',7,7,150000,'2025-01-01','2025-01-31',1),
(8,'CM0008',8,8,150000,'2025-01-01','2025-01-31',1),
(9,'CM0009',9,9,150000,'2025-01-01','2025-01-31',1),
(10,'CM0010',10,10,150000,'2025-01-01','2025-01-31',1);
SET IDENTITY_INSERT monthly_cards OFF;


SET IDENTITY_INSERT cards ON;
INSERT INTO cards (id, card_code, price, created_by)
VALUES
(1,'C0001',3000,1),
(2,'C0002',3000,1),
(3,'C0003',3000,2),
(4,'C0004',3000,2),
(5,'C0005',3000,3),
(6,'C0006',3000,3),
(7,'C0007',3000,4),
(8,'C0008',3000,4),
(9,'C0009',3000,5),
(10,'C0010',3000,5);
SET IDENTITY_INSERT cards OFF;


SET IDENTITY_INSERT vehicle_cards ON;
INSERT INTO vehicle_cards (id, vehicle_id, card_id)
VALUES
(1,1,1),(2,2,2),(3,3,3),(4,4,4),(5,5,5),
(6,6,6),(7,7,7),(8,8,8),(9,9,9),(10,10,10);
SET IDENTITY_INSERT vehicle_cards OFF;


SET IDENTITY_INSERT card_logs ON;
INSERT INTO card_logs (id, card_id, vehicle_id, entry_at, exit_at, fee, created_by, closed_by)
VALUES
(1,1,1,GETDATE(),NULL,NULL,1,NULL),
(2,2,2,GETDATE(),GETDATE(),3000,2,2),
(3,3,3,GETDATE(),GETDATE(),3000,2,2),
(4,4,4,GETDATE(),NULL,NULL,3,NULL),
(5,5,5,GETDATE(),GETDATE(),3000,3,3),
(6,6,6,GETDATE(),NULL,NULL,4,NULL),
(7,7,7,GETDATE(),GETDATE(),3000,4,4),
(8,8,8,GETDATE(),GETDATE(),10000,5,5),
(9,9,9,GETDATE(),NULL,NULL,5,NULL),
(10,10,10,GETDATE(),GETDATE(),15000,1,1);
SET IDENTITY_INSERT card_logs OFF;


SET IDENTITY_INSERT payments ON;
INSERT INTO payments (id, card_id, monthly_card_id, amount, payment_date, method, processed_by) VALUES
(1,1,NULL,5000,'2025-01-10','cash',2),
(2,2,NULL,6000,'2025-01-10','cash',2),
(3,3,NULL,7000,'2025-01-10','cash',3),
(4,4,NULL,15000,'2025-01-10','bank',3),
(5,5,NULL,15000,'2025-01-10','bank',4),
(6,NULL,1,1500000,'2025-01-01','bank',1),
(7,NULL,2,1500000,'2025-01-01','bank',1),
(8,NULL,3,1500000,'2025-01-01','bank',1),
(9,NULL,4,2500000,'2025-01-01','cash',1),
(10,NULL,5,2500000,'2025-01-01','cash',1);
SET IDENTITY_INSERT payments OFF;


SET IDENTITY_INSERT cameras ON;
INSERT INTO cameras (id, source_type, rtsp_url, file_path, description) VALUES
(1,'RTSP','rtsp://cam1','','Cổng trước'),
(2,'RTSP','rtsp://cam2','','Cổng sau'),
(3,'FILE','','video1.mp4','Bãi A'),
(4,'FILE','','video2.mp4','Bãi B'),
(5,'RTSP','rtsp://cam3','','Lầu 1'),
(6,'RTSP','rtsp://cam4','','Lầu 2'),
(7,'FILE','','video3.mp4','Khu VIP'),
(8,'RTSP','rtsp://cam5','','Kho'),
(9,'FILE','','video4.mp4','Bãi ngoài'),
(10,'RTSP','rtsp://cam6','','Cổng phụ');
SET IDENTITY_INSERT cameras OFF;

SET IDENTITY_INSERT alpr_logs ON;
INSERT INTO alpr_logs (id, camera_id, vehicle_id, image_path) VALUES
(1,1,1,'img1.jpg'),
(2,2,2,'img2.jpg'),
(3,3,3,'img3.jpg'),
(4,4,4,'img4.jpg'),
(5,5,5,'img5.jpg'),
(6,6,6,'img6.jpg'),
(7,7,7,'img7.jpg'),
(8,8,8,'img8.jpg'),
(9,9,9,'img9.jpg'),
(10,10,10,'img10.jpg');
SET IDENTITY_INSERT alpr_logs OFF;
