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
-- ===== Q3 / 2023 =====
(51, 1, '2023-07-01 07:10', '2023-07-01 18:00', 1, 2),
(52, 2, '2023-07-05 07:20', '2023-07-05 18:10', 1, 3),
(53, 3, '2023-07-10 07:30', '2023-07-10 18:20', 2, 3),
(54, 4, '2023-07-15 07:40', '2023-07-15 18:30', 1, 2),
(55, 5, '2023-07-20 07:50', '2023-07-20 18:40', 2, 3),

(56, 6, '2023-08-01 08:00', '2023-08-01 18:00', 1, 2),
(57, 7, '2023-08-06 08:10', '2023-08-06 18:10', 1, 3),
(58, 8, '2023-08-12 08:20', '2023-08-12 18:20', 2, 3),
(59, 9, '2023-08-18 08:30', '2023-08-18 18:30', 1, 2),
(60,10, '2023-08-25 08:40', '2023-08-25 18:40', 2, 3),

(61,11, '2023-09-01 09:00', '2023-09-01 18:00', 1, 2),
(62,12, '2023-09-06 09:10', '2023-09-06 18:10', 1, 3),
(63,13, '2023-09-12 09:20', '2023-09-12 18:20', 2, 3),
(64,14, '2023-09-18 09:30', '2023-09-18 18:30', 1, 2),
(65,15, '2023-09-25 09:40', '2023-09-25 18:40', 2, 3),

-- ===== Q3 / 2024 =====
(66, 1, '2024-07-02 07:10', '2024-07-02 18:05', 1, 2),
(67, 2, '2024-07-07 07:20', '2024-07-07 18:15', 1, 3),
(68, 3, '2024-07-12 07:30', '2024-07-12 18:25', 2, 3),
(69, 4, '2024-07-17 07:40', '2024-07-17 18:35', 1, 2),
(70, 5, '2024-07-22 07:50', '2024-07-22 18:45', 2, 3),

(71, 6, '2024-08-03 08:00', '2024-08-03 18:05', 1, 2),
(72, 7, '2024-08-08 08:10', '2024-08-08 18:15', 1, 3),
(73, 8, '2024-08-14 08:20', '2024-08-14 18:25', 2, 3),
(74, 9, '2024-08-19 08:30', '2024-08-19 18:35', 1, 2),
(75,10, '2024-08-26 08:40', '2024-08-26 18:45', 2, 3),

(76,11, '2024-09-02 09:00', '2024-09-02 18:05', 1, 2),
(77,12, '2024-09-07 09:10', '2024-09-07 18:15', 1, 3),
(78,13, '2024-09-13 09:20', '2024-09-13 18:25', 2, 3),
(79,14, '2024-09-18 09:30', '2024-09-18 18:35', 1, 2),
(80,15, '2024-09-24 09:40', '2024-09-24 18:45', 2, 3),

-- ===== Q3 / 2025 =====
(81, 1, '2025-07-03 07:15', '2025-07-03 18:10', 1, 2),
(82, 2, '2025-07-08 07:25', '2025-07-08 18:20', 1, 3),
(83, 3, '2025-07-13 07:35', '2025-07-13 18:30', 2, 3),
(84, 4, '2025-07-18 07:45', '2025-07-18 18:40', 1, 2),
(85, 5, '2025-07-23 07:55', '2025-07-23 18:50', 2, 3),

(86, 6, '2025-08-04 08:05', '2025-08-04 18:10', 1, 2),
(87, 7, '2025-08-09 08:15', '2025-08-09 18:20', 1, 3),
(88, 8, '2025-08-15 08:25', '2025-08-15 18:30', 2, 3),
(89, 9, '2025-08-20 08:35', '2025-08-20 18:40', 1, 2),
(90,10, '2025-08-27 08:45', '2025-08-27 18:50', 2, 3),

(91,11, '2025-09-03 09:05', '2025-09-03 18:10', 1, 2),
(92,12, '2025-09-08 09:15', '2025-09-08 18:20', 1, 3),
(93,13, '2025-09-14 09:25', '2025-09-14 18:30', 2, 3),
(94,14, '2025-09-19 09:35', '2025-09-19 18:40', 1, 2),
(95,15, '2025-09-25 09:45', '2025-09-25 18:50', 2, 3),

(96,16, '2025-09-26 10:00', '2025-09-26 19:00', 1, 2),
(97,17, '2025-09-27 10:10', '2025-09-27 19:10', 1, 3),
(98,18, '2025-09-28 10:20', '2025-09-28 19:20', 2, 3),
(99,19, '2025-09-29 10:30', '2025-09-29 19:30', 1, 2),
(100,20,'2025-09-30 10:40', '2025-09-30 19:40', 1, 3);

SET IDENTITY_INSERT monthly_card_logs OFF;
