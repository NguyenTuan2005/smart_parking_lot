from datetime import datetime
from typing import List, Dict, Tuple, Optional
from db.database import Database


class StatisticsDAO:
    def __init__(self):
        self._db = Database()

    def get_revenue_by_month(self, year: int = None) -> List[Dict]:
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()
            result = []
            # tính doanh thu theo tháng của 1 năm
            if year:
                # Doanh thu từ thẻ lượt (cards)
                sql_single = """
                             SELECT
                                 MONTH (exit_at) as month, SUM (fee) as revenue
                             FROM card_logs
                             WHERE YEAR (exit_at) = ?
                               AND exit_at IS NOT NULL
                               AND fee IS NOT NULL
                             GROUP BY MONTH (exit_at)
                             """
                single_cards = cursor.execute(sql_single, year).fetchall()

                # Doanh thu từ thẻ tháng (monthly_cards)
                sql_monthly = """
                              SELECT
                                  MONTH (start_date) as month, SUM (monthly_fee) as revenue
                              FROM monthly_cards
                              WHERE YEAR (start_date) = ?
                                AND is_paid = 1
                              GROUP BY MONTH (start_date)
                              """
                monthly_cards = cursor.execute(sql_monthly, year).fetchall()

                # Gộp doanh thu
                revenue_dict = {}
                for row in single_cards:
                    month = row[0]
                    revenue_dict[month] = revenue_dict.get(month, 0) + int(row[1] or 0)

                for row in monthly_cards:
                    month = row[0]
                    revenue_dict[month] = revenue_dict.get(month, 0) + int(row[1] or 0)

                result = [{'month': month, 'revenue': revenue}
                          for month, revenue in sorted(revenue_dict.items())]
        
            return result
        except Exception as e:
            print(f"Lỗi StatisticsDAO.get_revenue_by_month: {e}")
            import traceback
            traceback.print_exc()
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # Doanh thu theo ngày trong tháng
    def get_revenue_by_day_in_month(self, month: int, year: int) -> List[Dict]:
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()
            
            # Doanh thu thẻ lượt
            sql_single = """
                SELECT DAY(exit_at) as day, SUM(fee) as revenue
                FROM card_logs
                WHERE YEAR(exit_at) = ? AND MONTH(exit_at) = ?
                AND exit_at IS NOT NULL AND fee IS NOT NULL
                GROUP BY DAY(exit_at)
            """
            single_cards = cursor.execute(sql_single, year, month).fetchall()

            # Doanh thu thẻ tháng
            sql_monthly = """
                SELECT DAY(created_at) as day, SUM(monthly_fee) as revenue
                FROM monthly_cards
                WHERE YEAR(created_at) = ? AND MONTH(created_at) = ?
                AND is_paid = 1
                GROUP BY DAY(created_at)
            """
            monthly_cards = cursor.execute(sql_monthly, year, month).fetchall()

            revenue_dict = {}
            for row in single_cards:
                day = row[0]
                revenue_dict[day] = revenue_dict.get(day, 0) + int(row[1] or 0)
            for row in monthly_cards:
                day = row[0]
                revenue_dict[day] = revenue_dict.get(day, 0) + int(row[1] or 0)

            return [{'day': day, 'revenue': revenue} for day, revenue in sorted(revenue_dict.items())]
        except Exception as e:
            print(f"Lỗi StatisticsDAO.get_revenue_by_day_in_month: {e}")
            return []
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def get_vehicle_mix(self, start_date: datetime = None, end_date: datetime = None) -> Dict[str, int]:
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            # Đếm thẻ lượt: Những xe trong card_logs mà card_id KHÔNG thuộc monthly_cards
            single_sql = """
                         SELECT COUNT(*)
                         FROM card_logs cl
                         JOIN cards c ON cl.card_id = c.id
                         WHERE c.card_code NOT IN (SELECT card_code FROM monthly_cards WHERE is_active = 1)
                         """
            params = []
            if start_date and end_date:
                single_sql += " AND cl.entry_at BETWEEN ? AND ?"
                params.extend([start_date, end_date])

            single_count = cursor.execute(single_sql, tuple(params) if params else ()).fetchone()[0] or 0

            # Đếm thẻ tháng: Những xe trong card_logs mà card_id THUỘC monthly_cards
            monthly_sql = """
                          SELECT COUNT(*)
                          FROM card_logs cl
                          JOIN cards c ON cl.card_id = c.id
                          WHERE c.card_code IN (SELECT card_code FROM monthly_cards WHERE is_active = 1)
                          """
            monthly_params = []
            if start_date and end_date:
                monthly_sql += " AND cl.entry_at BETWEEN ? AND ?"
                monthly_params.extend([start_date, end_date])

            monthly_count = cursor.execute(monthly_sql, tuple(monthly_params) if monthly_params else ()).fetchone()[0] or 0

            return {
                'single': single_count,
                'monthly': monthly_count
            }
        except Exception as e:
            print(f"Lỗi StatisticsDAO.get_vehicle_mix: {e}")
            return {'single': 0, 'monthly': 0}
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def get_duration_by_card_type(self, start_date: datetime = None, end_date: datetime = None) -> Dict[str, List[int]]:
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            # Thời gian đỗ cho thẻ lượt
            single_sql = """
                         SELECT DATEDIFF(MINUTE, cl.entry_at, cl.exit_at)
                         FROM card_logs cl
                         JOIN cards c ON cl.card_id = c.id
                         WHERE cl.exit_at IS NOT NULL
                           AND c.card_code NOT IN (SELECT card_code FROM monthly_cards WHERE is_active = 1)
                         """
            params = []
            if start_date and end_date:
                single_sql += " AND cl.entry_at BETWEEN ? AND ?"
                params.extend([start_date, end_date])

            single_rows = cursor.execute(single_sql, tuple(params) if params else ()).fetchall()
            single_durations = [row[0] for row in single_rows if row[0] is not None and row[0] > 0]

            # Thẻ tháng
            monthly_sql = """
                          SELECT DATEDIFF(MINUTE, cl.entry_at, cl.exit_at)
                          FROM card_logs cl
                          JOIN cards c ON cl.card_id = c.id
                          WHERE cl.exit_at IS NOT NULL
                            AND c.card_code IN (SELECT card_code FROM monthly_cards WHERE is_active = 1)
                          """
            monthly_params = []
            if start_date and end_date:
                monthly_sql += " AND cl.entry_at BETWEEN ? AND ?"
                monthly_params.extend([start_date, end_date])

            monthly_rows = cursor.execute(monthly_sql, tuple(monthly_params) if monthly_params else ()).fetchall()
            monthly_durations = [row[0] for row in monthly_rows if row[0] is not None and row[0] > 0]

            return {
                'single': single_durations,
                'monthly': monthly_durations
            }
        except Exception as e:
            print(f"Lỗi StatisticsDAO.get_duration_by_card_type: {e}")
            return {'single': [], 'monthly': []}
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def get_traffic_by_hour_and_day(self, start_date: datetime = None, end_date: datetime = None) -> List[Dict]:
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            sql = """
                  SELECT CASE WHEN DATEPART(WEEKDAY, entry_at) = 1 THEN 7 ELSE DATEPART(WEEKDAY, entry_at) - 1 END as day_of_week, 
                         DATEPART(HOUR, entry_at) as hour,
                         COUNT(*) as count
                  FROM card_logs
                  WHERE 1=1
                  """
            params = []
            if start_date and end_date:
                sql += " AND entry_at BETWEEN ? AND ?"
                params.extend([start_date, end_date])

            sql += " GROUP BY CASE WHEN DATEPART(WEEKDAY, entry_at) = 1 THEN 7 ELSE DATEPART(WEEKDAY, entry_at) - 1 END, DATEPART(HOUR, entry_at)"
            sql += " ORDER BY day_of_week, hour"

            rows = cursor.execute(sql, tuple(params) if params else ()).fetchall()
            return [{'day_of_week': row[0], 'hour': row[1], 'count': row[2]} for row in rows]
        except Exception as e:
            print(f"Lỗi StatisticsDAO.get_traffic_by_hour_and_day: {e}")
            return []
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def get_entries_exits_by_day_of_week(self, start_date: datetime = None, end_date: datetime = None) -> Dict[str, List[int]]:
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            entry_sql = """
                        SELECT CASE WHEN DATEPART(WEEKDAY, entry_at) = 1 THEN 7 ELSE DATEPART(WEEKDAY, entry_at) - 1 END as day_of_week, 
                               COUNT(*) as count
                        FROM card_logs
                        WHERE 1=1
                        """
            params = []
            if start_date and end_date:
                entry_sql += " AND entry_at BETWEEN ? AND ?"
                params.extend([start_date, end_date])
            entry_sql += " GROUP BY CASE WHEN DATEPART(WEEKDAY, entry_at) = 1 THEN 7 ELSE DATEPART(WEEKDAY, entry_at) - 1 END"

            exit_sql = """
                       SELECT CASE WHEN DATEPART(WEEKDAY, exit_at) = 1 THEN 7 ELSE DATEPART(WEEKDAY, exit_at) - 1 END as day_of_week, 
                              COUNT(*) as count
                       FROM card_logs
                       WHERE exit_at IS NOT NULL
                       """
            exit_params = []
            if start_date and end_date:
                exit_sql += " AND exit_at BETWEEN ? AND ?"
                exit_params.extend([start_date, end_date])
            exit_sql += " GROUP BY CASE WHEN DATEPART(WEEKDAY, exit_at) = 1 THEN 7 ELSE DATEPART(WEEKDAY, exit_at) - 1 END"

            entry_rows = cursor.execute(entry_sql, tuple(params) if params else ()).fetchall()
            exit_rows = cursor.execute(exit_sql, tuple(exit_params) if exit_params else ()).fetchall()

            entries_dict = {row[0]: row[1] for row in entry_rows}
            exits_dict = {row[0]: row[1] for row in exit_rows}

            return {
                'entries': [entries_dict.get(i, 0) for i in range(1, 8)],
                'exits': [exits_dict.get(i, 0) for i in range(1, 8)]
            }
        except Exception as e:
            print(f"Lỗi StatisticsDAO.get_entries_exits_by_day_of_week: {e}")
            return {'entries': [0]*7, 'exits': [0]*7}
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def get_fee_vs_duration(self, start_date: datetime = None, end_date: datetime = None) -> List[Dict]:
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            sql = """
                  SELECT DATEDIFF(MINUTE, entry_at, exit_at), fee
                  FROM card_logs
                  WHERE exit_at IS NOT NULL AND fee IS NOT NULL
                  """
            params = []
            if start_date and end_date:
                sql += " AND entry_at BETWEEN ? AND ?"
                params.extend([start_date, end_date])

            rows = cursor.execute(sql, tuple(params) if params else ()).fetchall()
            return [{'duration': row[0], 'fee': float(row[1] or 0)} for row in rows if row[0] is not None and row[0] > 0]
        except Exception as e:
            print(f"Lỗi StatisticsDAO.get_fee_vs_duration: {e}")
            return []
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def get_traffic_by_hour(self, start_date: datetime = None, end_date: datetime = None) -> List[int]:
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()
            sql = "SELECT DATEPART(HOUR, entry_at), COUNT(*) FROM card_logs WHERE 1=1"
            params = []
            if start_date and end_date:
                sql += " AND entry_at BETWEEN ? AND ?"
                params.extend([start_date, end_date])
            sql += " GROUP BY DATEPART(HOUR, entry_at)"
            rows = cursor.execute(sql, tuple(params) if params else ()).fetchall()
            hour_dict = {row[0]: row[1] for row in rows}
            return [hour_dict.get(i, 0) for i in range(24)]
        except Exception as e:
            print(f"Lỗi StatisticsDAO.get_traffic_by_hour: {e}")
            return [0] * 24
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    # xe qua đêm (sau 10 tối đến 6h sáng)
    def get_overnight_vehicles_count(self) -> int:
        conn = None
        cursor = None
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
            return cursor.execute(sql).fetchone()[0] or 0
        except Exception as e:
            print(f"Lỗi get_overnight_vehicles_count: {e}")
            return 0
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def get_expiring_monthly_cards_count(self, days: int = 3) -> int:
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()
            sql = """
                  SELECT COUNT(*) FROM monthly_cards 
                  WHERE is_active = 1 AND is_paid = 1
                  AND expiry_date BETWEEN GETDATE() AND DATEADD(day, ?, GETDATE())
                  """
            return cursor.execute(sql, days).fetchone()[0] or 0
        except Exception as e:
            print(f"Lỗi get_expiring_monthly_cards_count: {e}")
            return 0
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def get_active_cameras_count(self) -> int:
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()
            sql = "SELECT COUNT(*) FROM cameras"
            return cursor.execute(sql).fetchone()[0] or 0
        except Exception as e:
            print(f"Lỗi get_active_cameras_count: {e}")
            return 0
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
