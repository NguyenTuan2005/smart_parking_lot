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


SET IDENTITY_INSERT vehicles ON;

INSERT INTO vehicles (id, vehicle_type, plate_number) VALUES
(1,'Xe máy','59X1-11111'),
(2,'Xe máy','59X1-22222'),
(3,'Xe máy','59X1-33333'),
(4,'Ô tô','51A-11111'),
(5,'Ô tô','51A-22222'),
(6,'Ô tô','51A-33333'),
(7,'Xe tải','60C-11111'),
(8,'Xe tải','60C-22222'),
(9,'Xe máy','62X1-44444'),
(10,'Ô tô','61A-55555');

SET IDENTITY_INSERT vehicles OFF;


SET IDENTITY_INSERT customers ON;
INSERT INTO customers (id, full_name, phone_number, email) VALUES
(1,N'Nguyễn Minh T','0911111111','t1@gmail.com'),
(2,N'Trần Minh H','0911111112','t2@gmail.com'),
(3,N'Lê Minh K','0911111113','t3@gmail.com'),
(4,N'Phạm Minh L','0911111114','t4@gmail.com'),
(5,N'Hoàng Minh M','0911111115','t5@gmail.com'),
(6,N'Vũ Minh N','0911111116','t6@gmail.com'),
(7,N'Đặng Minh P','0911111117','t7@gmail.com'),
(8,N'Ngô Minh Q','0911111118','t8@gmail.com'),
(9,N'Bùi Minh R','0911111119','t9@gmail.com'),
(10,N'Đỗ Minh S','0911111120','t10@gmail.com');
SET IDENTITY_INSERT customers OFF;


SET IDENTITY_INSERT monthly_cards ON;

INSERT INTO monthly_cards (id, card_code, customer_id, vehicle_id, fee, start_date, end_date, active) VALUES
(1,'MCARD0001',1,1,1500000,'2025-01-01','2025-01-31',1),
(2,'MCARD0002',2,2,1500000,'2025-01-01','2025-01-31',1),
(3,'MCARD0003',3,3,1500000,'2025-01-01','2025-01-31',0),
(4,'MCARD0004',4,4,2500000,'2025-01-01','2025-01-31',1),
(5,'MCARD0005',5,5,2500000,'2025-01-01','2025-01-31',1),
(6,'MCARD0006',6,6,2500000,'2025-01-01','2025-01-31',0),
(7,'MCARD0007',7,7,3000000,'2025-01-01','2025-01-31',1),
(8,'MCARD0008',8,8,3000000,'2025-01-01','2025-01-31',1),
(9,'MCARD0009',9,9,1500000,'2025-01-01','2025-01-31',1),
(10,'MCARD0010',10,10,2500000,'2025-01-01','2025-01-31',1);

SET IDENTITY_INSERT monthly_cards OFF;


SET IDENTITY_INSERT cards ON;

INSERT INTO cards (id, card_code, vehicle_id, card_type, entry_at, exit_at, fee, created_by, closed_by) VALUES
(1,'CARD0001',1,'SINGLE','2025-01-10 07:00','2025-01-10 09:00',5000,1,2),
(2,'CARD0002',2,'SINGLE','2025-01-10 08:00','2025-01-10 09:30',6000,1,2),
(3,'CARD0003',3,'SINGLE','2025-01-10 08:30','2025-01-10 10:00',7000,1,3),
(4,'CARD0004',4,'SINGLE','2025-01-10 09:00','2025-01-10 11:00',15000,1,3),
(5,'CARD0005',5,'SINGLE','2025-01-10 10:00','2025-01-10 12:00',15000,1,4),
(6,'CARD0006',6,'SINGLE','2025-01-10 11:00','2025-01-10 13:00',15000,1,4),
(7,'CARD0007',7,'SINGLE','2025-01-10 12:00','2025-01-10 15:00',20000,1,5),
(8,'CARD0008',8,'SINGLE','2025-01-10 13:00','2025-01-10 16:00',20000,1,5),
(9,'CARD0009',9,'SINGLE','2025-01-10 14:00','2025-01-10 17:00',8000,1,6),
(10,'CARD0010',10,'SINGLE','2025-01-10 15:00','2025-01-10 18:00',15000,1,6);

SET IDENTITY_INSERT cards OFF;


SET IDENTITY_INSERT vehicle_cards ON;

INSERT INTO vehicle_cards (id, vehicle_id, card_id) VALUES
(1,1,1),(2,2,2),(3,3,3),(4,4,4),(5,5,5),
(6,6,6),(7,7,7),(8,8,8),(9,9,9),(10,10,10);

SET IDENTITY_INSERT vehicle_cards OFF;


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
