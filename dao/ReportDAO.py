from db.database import Database


class ReportDAO:
    def __init__(self):
        self._db = Database()

    def get_parking_history(self, start_date, end_date):
        conn = self._db.connect()
        cursor = conn.cursor()

        sd = start_date.strftime('%Y-%m-%d')
        ed = end_date.strftime('%Y-%m-%d')

        query = """
            SELECT 
                cl.entry_at, 
                CASE 
                    WHEN mc.id IS NOT NULL THEN N'Vé Tháng' 
                    ELSE N'Vé Lượt' 
                END AS card_type,
                v.plate_number,
                CASE 
                    WHEN cl.exit_at IS NULL THEN N'Vào' 
                    ELSE N'Ra' 
                END AS action_type,
                ISNULL(cl.fee, 0) AS fee,
                CASE 
                    WHEN cl.exit_at IS NULL THEN N'Đang gửi' 
                    ELSE N'Hoàn tất' 
                END AS note
            FROM card_logs cl
            JOIN vehicles v ON cl.vehicle_id = v.id
            JOIN cards c ON cl.card_id = c.id
            LEFT JOIN monthly_cards mc ON c.card_code = mc.card_code
            WHERE CAST(cl.entry_at AS DATE) BETWEEN ? AND ?
            ORDER BY cl.entry_at DESC
        """

        print(f"[DAO] SQL Execute from {sd} to {ed}")

        cursor.execute(query, (sd, ed))
        rows = cursor.fetchall()

        cursor.close()
        conn.close()
        return rows
