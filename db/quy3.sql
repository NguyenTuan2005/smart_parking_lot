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
ALTER TABLE cards
ADD night_price INT NOT NULL DEFAULT 5000;
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



