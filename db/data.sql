USE SmartParkingLotSystem;

/* =====================================
   1. STAFFS
===================================== */
SET IDENTITY_INSERT staffs ON;
INSERT INTO staffs (id, username, password, fullname, phone_number, role, created_at, updated_at) VALUES
(1, 'admin', 'hashed_pw_1', 'Nguyen Van An', '0901000001', 1, GETDATE(), GETDATE()),
(2, 'staff1', 'hashed_pw_2', 'Tran Thi B', '0901000002', 2, GETDATE(), GETDATE()),
(3, 'staff2', 'hashed_pw_3', 'Le Van C', '0901000003', 2, GETDATE(), GETDATE());
SET IDENTITY_INSERT staffs OFF;



/* =====================================
   2. CAMERAS
===================================== */
SET IDENTITY_INSERT cameras ON;
INSERT INTO cameras (id, source_type, rtsp_url, file_path, description, created_at, updated_at) VALUES
(1, 'rtsp', 'rtsp://cam1/live', NULL, 'Cổng chính', GETDATE(), GETDATE()),
(2, 'rtsp', 'rtsp://cam2/live', NULL, 'Tầng hầm B1', GETDATE(), GETDATE()),
(3, 'file', NULL, 'D:\\videos\\cam3.mp4', 'Camera mô phỏng', GETDATE(), GETDATE());
SET IDENTITY_INSERT cameras OFF;



/* =====================================
   3. CUSTOMERS
===================================== */
SET IDENTITY_INSERT customers ON;
INSERT INTO customers (id, full_name, phone_number, email) VALUES
(1, 'Pham Minh Hoang', '0912000001', 'hoang@example.com'),
(2, 'Nguyen Thi Lan', '0912000002', 'lan@example.com'),
(3, 'Le Huu Phu', '0912000003', 'phu@example.com'),
(4, 'Tran Van Hai', '0912000004', 'hai@example.com'),
(5, 'Do Thi Ha', '0912000005', 'ha@example.com');
SET IDENTITY_INSERT customers OFF;



/* =====================================
   4. VEHICLES
===================================== */
SET IDENTITY_INSERT vehicles ON;
INSERT INTO vehicles (id, plate_number, created_at, updated_at) VALUES
(1, '30A-12345', GETDATE(), GETDATE()),
(2, '29B-22222', GETDATE(), GETDATE()),
(3, '88C-54321', GETDATE(), GETDATE()),
(4, '51H-33789', GETDATE(), GETDATE()),
(5, '60A-90909', GETDATE(), GETDATE()),
(6, '30K-88888', GETDATE(), GETDATE()),
(7, '17D-44556', GETDATE(), GETDATE()),
(8, '43A-67676', GETDATE(), GETDATE()),
(9, '75F-12399', GETDATE(), GETDATE()),
(10, '36C-00411', GETDATE(), GETDATE());
SET IDENTITY_INSERT vehicles OFF;



/* =====================================
   5. ALPR LOGS
===================================== */
SET IDENTITY_INSERT alpr_logs ON;
INSERT INTO alpr_logs (id, camera_id, vehicle_id, detected_at, image_path) VALUES
(1, 1, 1, GETDATE(), 'images/1.jpg'),
(2, 1, 2, GETDATE(), 'images/2.jpg'),
(3, 2, 3, GETDATE(), 'images/3.jpg'),
(4, 2, 4, GETDATE(), 'images/4.jpg'),
(5, 2, 5, GETDATE(), 'images/5.jpg'),
(6, 3, 6, GETDATE(), 'images/6.jpg'),
(7, 1, 7, GETDATE(), 'images/7.jpg'),
(8, 1, 8, GETDATE(), 'images/8.jpg'),
(9, 3, 9, GETDATE(), 'images/9.jpg'),
(10, 3, 10, GETDATE(), 'images/10.jpg');
SET IDENTITY_INSERT alpr_logs OFF;



/* =====================================
   6. MONTHLY CARDS
===================================== */
SET IDENTITY_INSERT monthly_cards ON;
INSERT INTO monthly_cards (id, customer_id, vehicle_id, price, start_date, end_date, active, created_at, updated_at) VALUES
(1, 1, 1, 500000, '2025-01-01', '2025-01-31', 1, GETDATE(), GETDATE()),
(2, 2, 3, 450000, '2025-01-05', '2025-02-05', 1, GETDATE(), GETDATE()),
(3, 3, 5, 500000, '2025-01-10', '2025-02-10', 1, GETDATE(), GETDATE()),
(4, 4, 7, 480000, '2025-01-03', '2025-02-03', 1, GETDATE(), GETDATE()),
(5, 5, 8, 500000, '2025-01-01', '2025-01-31', 0, GETDATE(), GETDATE());
SET IDENTITY_INSERT monthly_cards OFF;



/* =====================================
   7. CARDS (LƯỢT VÀO - LƯỢT RA)
===================================== */
SET IDENTITY_INSERT cards ON;
INSERT INTO cards (id, vehicle_id, card_type, entry_time, exit_time, fee, created_at, updated_at, created_by, closed_by) VALUES
(1, 2, 'LE', GETDATE(), NULL, NULL, GETDATE(), GETDATE(), 2, NULL),
(2, 4, 'LE', GETDATE(), GETDATE(), 10000, GETDATE(), GETDATE(), 1, 3),
(3, 6, 'LE', GETDATE(), NULL, NULL, GETDATE(), GETDATE(), 2, NULL),
(4, 9, 'LE', GETDATE(), GETDATE(), 15000, GETDATE(), GETDATE(), 3, 1),
(5, 10, 'LE', GETDATE(), GETDATE(), 12000, GETDATE(), GETDATE(), 1, 2),
(6, 1, 'MONTH', GETDATE(), GETDATE(), 0, GETDATE(), GETDATE(), 1, 2),
(7, 3, 'MONTH', GETDATE(), NULL, 0, GETDATE(), GETDATE(), 2, NULL),
(8, 5, 'MONTH', GETDATE(), GETDATE(), 0, GETDATE(), GETDATE(), 3, 1),
(9, 7, 'MONTH', GETDATE(), NULL, 0, GETDATE(), GETDATE(), 1, NULL),
(10, 8, 'MONTH', GETDATE(), NULL, 0, GETDATE(), GETDATE(), 2, NULL);
SET IDENTITY_INSERT cards OFF;



/* =====================================
   8. VEHICLE-CARDS
===================================== */
SET IDENTITY_INSERT vehicle_cards ON;
INSERT INTO vehicle_cards (id, vehicle_id, card_id) VALUES
(1, 2, 1),
(2, 4, 2),
(3, 6, 3),
(4, 9, 4),
(5, 10, 5),
(6, 1, 6),
(7, 3, 7),
(8, 5, 8),
(9, 7, 9),
(10, 8, 10);
SET IDENTITY_INSERT vehicle_cards OFF;



/* =====================================
   9. PAYMENTS
===================================== */
SET IDENTITY_INSERT payments ON;
INSERT INTO payments (id, card_id, monthly_card_id, amount, payment_date, method, processed_by) VALUES
(1, 2, NULL, 10000, GETDATE(), 'cash', 1),
(2, 4, NULL, 15000, GETDATE(), 'cash', 2),
(3, 5, NULL, 12000, GETDATE(), 'momo', 3),
(4, NULL, 1, 500000, GETDATE(), 'bank', 1),
(5, NULL, 2, 450000, GETDATE(), 'momo', 2),
(6, NULL, 3, 500000, GETDATE(), 'cash', 3),
(7, NULL, 4, 480000, GETDATE(), 'cash', 1),
(8, NULL, 5, 500000, GETDATE(), 'bank', 2),
(9, 6, NULL, 0, GETDATE(), 'free', 1),
(10, 8, NULL, 0, GETDATE(), 'free', 2);
SET IDENTITY_INSERT payments OFF;
