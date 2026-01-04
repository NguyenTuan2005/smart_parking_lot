from datetime import datetime
from typing import List, Dict, Tuple, Optional
from db.database import Database


class StatisticsDAO:
    def __init__(self):
        self._db = Database()

    def get_revenue_by_month(self, year: int = None, start_date: datetime = None, end_date: datetime = None) -> List[Dict]:
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()
            result = []

            if year or (start_date and end_date):
                # Xác định điều kiện filter
                date_condition = ""
                params = []
                
                if start_date and end_date:
                    date_condition = "AND exit_at BETWEEN ? AND ?"
                    params = [start_date, end_date]
                elif year:
                    date_condition = "AND YEAR(exit_at) = ?"
                    params = [year]

                # Doanh thu từ thẻ lượt - Lấy từ bảng cards
                sql_single = f"""
                             SELECT
                                 MONTH (exit_at) as month, SUM (fee) as revenue
                             FROM cards
                             WHERE exit_at IS NOT NULL
                               AND fee IS NOT NULL
                               AND card_type = 'single'
                               {date_condition}
                             GROUP BY MONTH (exit_at) \
                             """
                single_cards = cursor.execute(sql_single, params).fetchall()

                # Doanh thu từ thẻ tháng - Lấy từ bảng monthly_cards
                # Dùng start_date làm tháng ghi nhận doanh thu
                monthly_condition = ""
                monthly_params = []
                
                if start_date and end_date:
                    monthly_condition = "AND start_date BETWEEN ? AND ?"
                    monthly_params = [start_date.date(), end_date.date()]
                elif year:
                    monthly_condition = "AND YEAR(start_date) = ?"
                    monthly_params = [year]

                sql_monthly = f"""
                              SELECT
                                  MONTH (start_date) as month, SUM (monthly_fee) as revenue
                              FROM monthly_cards
                              WHERE is_paid = 1
                                {monthly_condition}
                              GROUP BY MONTH (start_date) \
                              """
                monthly_cards = cursor.execute(sql_monthly, monthly_params).fetchall()

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

            # Đếm thẻ lượt: Những xe trong cards mà card_type = 'single'
            single_sql = """
                         SELECT COUNT(*)
                         FROM cards
                         WHERE card_type = 'single'
                         """
            params = []
            if start_date and end_date:
                single_sql += " AND entry_at BETWEEN ? AND ?"
                params.extend([start_date, end_date])

            single_count = cursor.execute(single_sql, tuple(params) if params else ()).fetchone()[0] or 0

            # Đếm thẻ tháng: Những xe trong monthly_cards
            monthly_sql = """
                          SELECT COUNT(*)
                          FROM monthly_cards
                          WHERE is_active = 1
                          """
            monthly_params = []
            if start_date and end_date:
                monthly_sql += " AND start_date <= ? AND expiry_date >= ?"
                monthly_params.extend([end_date.date(), start_date.date()])

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
        """
        Thời gian đỗ xe theo loại thẻ - SỬA ĐỂ DÙNG cards
        """
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            # Thời gian đỗ cho thẻ lượt
            single_sql = """
                SELECT DATEDIFF(MINUTE, entry_at, exit_at)
                FROM cards
                WHERE exit_at IS NOT NULL
                  AND card_type = 'single'
            """
            params = []
            if start_date and end_date:
                single_sql += " AND entry_at BETWEEN ? AND ?"
                params.extend([start_date, end_date])

            single_rows = cursor.execute(single_sql, tuple(params) if params else ()).fetchall()
            single_durations = [row[0] for row in single_rows if row[0] is not None and row[0] > 0]

            # Thẻ tháng - tính thời gian đỗ từ card_logs nếu có, hoặc giả định
            monthly_sql = """
                SELECT DATEDIFF(MINUTE, cl.entry_at, cl.exit_at)
                FROM card_logs cl
                JOIN monthly_cards mc ON cl.card_id = mc.id
                WHERE cl.exit_at IS NOT NULL
                  AND mc.is_active = 1
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
        """
        Lưu lượng xe theo giờ và ngày - SỬA ĐỂ DÙNG cards
        Dùng DATEPART(WEEKDAY) của SQL Server
        """
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            # SQL Server: DATEPART(WEEKDAY) trả về 1=Chủ Nhật, 2=Thứ 2, ..., 7=Thứ 7
            # Chuyển đổi: Thứ 2=1, ..., Chủ Nhật=7
            sql = """
                  SELECT CASE 
                             WHEN DATEPART(WEEKDAY, entry_at) = 1 THEN 7 -- Chủ Nhật 
                             ELSE DATEPART(WEEKDAY, entry_at) - 1 -- Thứ 2-7 
                             END as day_of_week, 
                         DATEPART(HOUR, entry_at) as hour,
                       COUNT(*) as count
                  FROM cards
                  WHERE 1=1 
                  """
            params = []
            if start_date and end_date:
                sql += " AND entry_at BETWEEN ? AND ?"
                params.extend([start_date, end_date])

            sql += """
                   GROUP BY 
                       CASE 
                           WHEN DATEPART(WEEKDAY, entry_at) = 1 THEN 7
                           ELSE DATEPART(WEEKDAY, entry_at) - 1
                       END,
                       DATEPART(HOUR, entry_at)
                   ORDER BY day_of_week, hour
               """

            rows = cursor.execute(sql, tuple(params) if params else ()).fetchall()
            return [{'day_of_week': row[0], 'hour': row[1], 'count': row[2]} for row in rows]
        except Exception as e:
            print(f"Lỗi StatisticsDAO.get_traffic_by_hour_and_day: {e}")
            import traceback
            traceback.print_exc()
            return []
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
    def get_entries_exits_by_day_of_week(self, start_date: datetime = None, end_date: datetime = None) -> Dict[str, List[int]]:
        """
        Lượt vào/ra theo ngày trong tuần - SỬA ĐỂ DÙNG cards
        """
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            entry_sql = """
                SELECT 
                    CASE 
                        WHEN DATEPART(WEEKDAY, entry_at) = 1 THEN 7
                        ELSE DATEPART(WEEKDAY, entry_at) - 1
                    END as day_of_week,
                    COUNT(*) as count
                FROM cards
                WHERE 1=1
            """
            params = []
            if start_date and end_date:
                entry_sql += " AND entry_at BETWEEN ? AND ?"
                params.extend([start_date, end_date])
            entry_sql += """
                GROUP BY 
                    CASE 
                        WHEN DATEPART(WEEKDAY, entry_at) = 1 THEN 7
                        ELSE DATEPART(WEEKDAY, entry_at) - 1
                    END
            """

            exit_sql = """
                SELECT 
                    CASE 
                        WHEN DATEPART(WEEKDAY, exit_at) = 1 THEN 7
                        ELSE DATEPART(WEEKDAY, exit_at) - 1
                    END as day_of_week,
                    COUNT(*) as count
                FROM cards
                WHERE exit_at IS NOT NULL
            """
            exit_params = []
            if start_date and end_date:
                exit_sql += " AND exit_at BETWEEN ? AND ?"
                exit_params.extend([start_date, end_date])
            exit_sql += """
                GROUP BY 
                    CASE 
                        WHEN DATEPART(WEEKDAY, exit_at) = 1 THEN 7
                        ELSE DATEPART(WEEKDAY, exit_at) - 1
                    END
            """

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
        """
        Tương quan phí và thời gian đỗ - CHỈ LẤY THẺ LƯỢT (thẻ tháng không có phí)
        """
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            # Chỉ lấy từ cards (thẻ lượt có fee)
            sql = """
                SELECT 
                    DATEDIFF(MINUTE, entry_at, exit_at) as duration,
                    fee
                FROM cards
                WHERE exit_at IS NOT NULL 
                  AND fee IS NOT NULL
                  AND card_type = 'single'
            """
            params = []
            if start_date and end_date:
                sql += " AND entry_at BETWEEN ? AND ?"
                params.extend([start_date, end_date])

            rows = cursor.execute(sql, tuple(params) if params else ()).fetchall()
            return [{'duration': row[0], 'fee': float(row[1] or 0)}
                   for row in rows if row[0] is not None and row[0] > 0]
        except Exception as e:
            print(f"Lỗi StatisticsDAO.get_fee_vs_duration: {e}")
            return []
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def get_traffic_by_hour(self, start_date: datetime = None, end_date: datetime = None) -> List[int]:
        """
        Lưu lượng xe theo giờ - SỬA ĐỂ DÙNG cards
        """
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            sql = """
                  SELECT DATEPART(HOUR, entry_at) as hour, COUNT(*) as count
                  FROM cards
                  WHERE 1=1 \
                  """
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
