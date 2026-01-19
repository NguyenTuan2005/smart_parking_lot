go
INSERT INTO staffs (fullname, phone_number, username, password, role)
VALUES
(N'Admin', '0900000000', 'admin', 'admin123', 1),
(N'Staff 1', '0900000001', 'staff1', '123', 2),
(N'Staff 2', '0900000002', 'staff2', '123', 2);

go
INSERT INTO cameras (source_type, rtsp_url, description)
VALUES
('rtsp','rtsp://cam1',N'Cổng vào'),
('rtsp','rtsp://cam2',N'Cổng ra'),
('rtsp','rtsp://cam3',N'Khu A');

go
DECLARE @i INT = 1;
WHILE @i <= 50
BEGIN
    INSERT INTO customers (full_name, phone_number, email)
    VALUES (
        N'Khách ' + CAST(@i AS NVARCHAR),
        '09' + RIGHT('00000000' + CAST(@i AS VARCHAR), 8),
        'user' + CAST(@i AS VARCHAR) + '@mail.com'
    );
    SET @i = @i + 1;
END
go


go
DECLARE @i INT = 1;
WHILE @i <= 50
BEGIN
    INSERT INTO vehicles (vehicle_type, plate_number)
    VALUES (N'Xe máy', CONCAT('59A-', RIGHT('00000'+CAST(@i AS VARCHAR),5)));
    SET @i = @i + 1;
END
go


go
DECLARE @i INT = 1;
WHILE @i <= 50
BEGIN
    INSERT INTO cards (card_code, price, created_by)
    VALUES ('CARD'+RIGHT('000'+CAST(@i AS VARCHAR),3), 3000, 1);
    SET @i = @i + 1;
END
go


go
UPDATE cards
SET night_price = 5000
WHERE night_price IS NULL;
go

go
INSERT INTO monthly_cards
(card_code, customer_id, vehicle_id, monthly_fee, start_date, expiry_date, is_paid)
SELECT
    'MCQ3' + RIGHT('000'+CAST(id AS VARCHAR),3),
    id,
    id,
    70000,
    DATEADD(DAY, id,
        CASE
            WHEN id % 3 = 0 THEN '2022-07-01'
            WHEN id % 3 = 1 THEN '2023-08-01'
            ELSE              '2024-09-01'
        END),
    DATEADD(MONTH, 1,
        DATEADD(DAY, id,
            CASE
                WHEN id % 3 = 0 THEN '2022-07-01'
                WHEN id % 3 = 1 THEN '2023-08-01'
                ELSE              '2024-09-01'
            END)),
    1
FROM customers;
go


go
INSERT INTO card_logs
(card_id, vehicle_id, entry_at, exit_at, fee, created_by, closed_by)
SELECT
    id,
    id,
    DATEADD(DAY, id,
        CASE
            WHEN id % 3 = 0 THEN '2022-07-01 07:00'
            WHEN id % 3 = 1 THEN '2023-08-01 08:00'
            ELSE              '2024-09-01 09:00'
        END),
    DATEADD(MINUTE, 90,
        DATEADD(DAY, id,
            CASE
                WHEN id % 3 = 0 THEN '2022-07-01 07:00'
                WHEN id % 3 = 1 THEN '2023-08-01 08:00'
                ELSE              '2024-09-01 09:00'
            END)),
    3000,
    2,
    2
FROM cards
WHERE id <= 50;
go

INSERT INTO payments (card_id, amount, payment_date, method, processed_by)
SELECT id, 3000, exit_at, 'cash', 2 FROM card_logs;

INSERT INTO payments (monthly_card_id, amount, payment_date, method, processed_by)
SELECT id, monthly_fee, start_date, 'bank', 1 FROM monthly_cards;



SET IDENTITY_INSERT monthly_card_logs ON;

INSERT INTO monthly_card_logs (id, monthly_card_id, entry_at, exit_at, created_by, closed_by) VALUES
-- ===== 2023 =====
(51, 1, '2023-01-05 07:10', '2023-01-05 18:20', 1, 2),
(52, 2, '2023-02-10 08:00', '2023-02-10 17:45', 1, 2),
(53, 3, '2023-03-15 07:30', '2023-03-15 18:00', 2, 3),
(54, 4, '2023-04-20 08:15', '2023-04-20 17:30', 2, 3),
(55, 5, '2023-05-25 07:00', '2023-05-25 18:10', 1, 2),
(56, 6, '2023-06-05 08:10', '2023-06-05 17:50', 1, 3),
(57, 7, '2023-07-12 07:20', '2023-07-12 18:30', 2, 3),
(58, 8, '2023-08-18 08:05', '2023-08-18 17:40', 1, 2),
(59, 9, '2023-09-22 07:50', '2023-09-22 18:15', 2, 3),
(60, 10,'2023-10-30 08:00', '2023-10-30 17:45', 1, 2),

-- ===== 2024 =====
(61, 1, '2024-01-03 07:10', '2024-01-03 18:00', 1, 2),
(62, 2, '2024-02-08 08:00', '2024-02-08 17:50', 1, 3),
(63, 3, '2024-03-14 07:30', '2024-03-14 18:20', 2, 3),
(64, 4, '2024-04-19 08:15', '2024-04-19 17:40', 2, 3),
(65, 5, '2024-05-24 07:00', '2024-05-24 18:10', 1, 2),
(66, 6, '2024-06-02 08:10', '2024-06-02 17:55', 1, 3),
(67, 7, '2024-07-11 07:20', '2024-07-11 18:30', 2, 3),
(68, 8, '2024-08-16 08:05', '2024-08-16 17:45', 1, 2),
(69, 9, '2024-09-21 07:50', '2024-09-21 18:15', 2, 3),
(70, 10,'2024-10-28 08:00', '2024-10-28 17:50', 1, 2),

-- ===== 2025 =====
(71, 1, '2025-01-04 07:10', '2025-01-04 18:05', 1, 2),
(72, 2, '2025-02-07 08:00', '2025-02-07 17:55', 1, 3),
(73, 3, '2025-03-13 07:30', '2025-03-13 18:25', 2, 3),
(74, 4, '2025-04-18 08:15', '2025-04-18 17:45', 2, 3),
(75, 5, '2025-05-23 07:00', '2025-05-23 18:15', 1, 2),
(76, 6, '2025-06-01 08:10', '2025-06-01 18:00', 1, 3),
(77, 7, '2025-07-10 07:20', '2025-07-10 18:35', 2, 3),
(78, 8, '2025-08-15 08:05', '2025-08-15 17:50', 1, 2),
(79, 9, '2025-09-20 07:50', '2025-09-20 18:20', 2, 3),
(80, 10,'2025-10-27 08:00', '2025-10-27 17:55', 1, 2),

-- ===== tiếp đến 100 =====
(81, 11,'2025-01-10 07:00', '2025-01-10 18:00', 1, 2),
(82, 12,'2025-01-11 07:10', '2025-01-11 18:10', 2, 3),
(83, 13,'2025-01-12 07:20', '2025-01-12 18:20', 1, 3),
(84, 14,'2025-01-13 07:30', '2025-01-13 18:30', 2, 3),
(85, 15,'2025-01-14 07:40', '2025-01-14 18:40', 1, 2),
(86, 16,'2025-01-15 07:50', '2025-01-15 18:50', 1, 3),
(87, 17,'2025-01-16 08:00', '2025-01-16 19:00', 2, 3),
(88, 18,'2025-01-17 08:10', '2025-01-17 19:10', 1, 2),
(89, 19,'2025-01-18 08:20', '2025-01-18 19:20', 2, 3),
(90, 20,'2025-01-19 08:30', '2025-01-19 19:30', 1, 2),
(91, 21,'2025-01-20 08:40', '2025-01-20 19:40', 1, 3),
(92, 22,'2025-01-21 08:50', '2025-01-21 19:50', 2, 3),
(93, 23,'2025-01-22 09:00', '2025-01-22 20:00', 1, 2),
(94, 24,'2025-01-23 09:10', '2025-01-23 20:10', 1, 3),
(95, 25,'2025-01-24 09:20', '2025-01-24 20:20', 2, 3),
(96, 26,'2025-01-25 09:30', '2025-01-25 20:30', 1, 2),
(97, 27,'2025-01-26 09:40', '2025-01-26 20:40', 1, 3),
(98, 28,'2025-01-27 09:50', '2025-01-27 20:50', 2, 3),
(99, 29,'2025-01-28 10:00', '2025-01-28 21:00', 1, 2),
(100,30,'2025-01-29 10:10', '2025-01-29 21:10', 1, 3);

SET IDENTITY_INSERT monthly_card_logs OFF;
