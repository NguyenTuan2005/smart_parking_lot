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

        cursor.execute(query, (sd, ed))
        rows = cursor.fetchall()

        cursor.close()
        conn.close()
        return rows

    def get_daily_revenue(self, current_date):
        try:
            conn = self._db.connect()
            cursor = conn.cursor()
            date_str = current_date.strftime('%Y-%m-%d')

            query = """
                SELECT 
                    (SELECT ISNULL(SUM(fee), 0) FROM card_logs WHERE CAST(exit_at AS DATE) = ?) +
                    (SELECT ISNULL(SUM(monthly_fee), 0) FROM monthly_cards WHERE CAST(created_at AS DATE) = ? AND is_paid = 1)
            """
            cursor.execute(query, (date_str, date_str))
            result = cursor.fetchone()[0]
            return float(result) if result else 0.0
        except Exception as e:
            print(f"Error in get_daily_revenue: {e}")
            return 0.0
        finally:
            if conn: conn.close()

    def get_currently_parked_count(self):
        try:
            conn = self._db.connect()
            cursor = conn.cursor()
            query = "SELECT COUNT(*) FROM card_logs WHERE exit_at IS NULL"
            cursor.execute(query)
            return int(cursor.fetchone()[0])
        except Exception as e:
            print(f"Error in get_currently_parked_count: {e}")
            return 0
        finally:
            if conn: conn.close()

    def get_today_entries_count(self, current_date):
        try:
            conn = self._db.connect()
            cursor = conn.cursor()
            date_str = current_date.strftime('%Y-%m-%d')
            query = "SELECT COUNT(*) FROM card_logs WHERE CAST(entry_at AS DATE) = ?"
            cursor.execute(query, (date_str,))
            return int(cursor.fetchone()[0])
        except Exception as e:
            print(f"Error in get_today_entries_count: {e}")
            return 0
        finally:
            if conn: conn.close()

    def get_active_monthly_cards_count(self):
        try:
            conn = self._db.connect()
            cursor = conn.cursor()
            # Active monthly cards: is_active = 1 and expiry_date >= today
            from datetime import date
            today = date.today().strftime('%Y-%m-%d')
            query = "SELECT COUNT(*) FROM monthly_cards WHERE is_active = 1 AND expiry_date >= ?"
            cursor.execute(query, (today,))
            return int(cursor.fetchone()[0])
        except Exception as e:
            print(f"Error in get_active_monthly_cards_count: {e}")
            return 0
        finally:
            if conn: conn.close()

    # xe qua đêm (sau 10 tối đến 6h sáng)
    def get_overnight_vehicles_count(self) -> int:
        try:
            conn = self._db.connect()
            cursor = conn.cursor()
            sql = """
                  SELECT COUNT(*) FROM card_logs 
                  WHERE exit_at IS NULL 
                  AND (
                    (DATEPART(HOUR, entry_at) >= 22 OR DATEPART(HOUR, entry_at) < 6)
                    OR entry_at < CAST(GETDATE() AS DATE)
                  )
                  """
            cursor.execute(sql)
            return cursor.fetchone()[0] or 0
        except Exception:
            return 0
        finally:
            if conn: conn.close()

    def get_expiring_monthly_cards_count(self, days: int = 3) -> int:
        try:
            conn = self._db.connect()
            cursor = conn.cursor()
            sql = """
                  SELECT COUNT(*) FROM monthly_cards 
                  WHERE is_active = 1 AND is_paid = 1
                  AND expiry_date BETWEEN GETDATE() AND DATEADD(day, ?, GETDATE())
                  """
            cursor.execute(sql, (days,))
            return cursor.fetchone()[0] or 0
        except Exception:
            return 0
        finally:
            if conn: conn.close()

    def get_active_cameras_count(self) -> int:
        try:
            conn = self._db.connect()
            cursor = conn.cursor()
            sql = "SELECT COUNT(*) FROM cameras"
            cursor.execute(sql)
            return cursor.fetchone()[0] or 0
        except Exception:
            return 0
        finally:
            if conn: conn.close()
