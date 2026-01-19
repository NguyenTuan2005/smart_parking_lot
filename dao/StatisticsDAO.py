from datetime import datetime
from typing import List, Dict, Tuple, Optional
from db.database import Database


class StatisticsDAO:
    def __init__(self):
        self._db = Database()

    def get_revenue_by_month(self, year: int = None, start_date: datetime = None, end_date: datetime = None) -> List[
        Dict]:
        """Doanh thu theo tháng - BÁO CÁO CẢ NĂM VÀ THÁNG"""
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()
            result = []

            if year or (start_date and end_date):
                # Điều kiện filter
                date_condition = ""
                params = []

                if start_date and end_date:
                    date_condition = "AND exit_at BETWEEN ? AND ?"
                    params = [start_date, end_date]
                elif year:
                    date_condition = "AND YEAR(exit_at) = ?"
                    params = [year]

                # Doanh thu từ thẻ lượt - Luôn GROUP BY MONTH
                sql_single = f"""
                    SELECT
                        MONTH(exit_at) as month, 
                        SUM(fee) as revenue
                    FROM card_logs
                    WHERE exit_at IS NOT NULL
                      AND fee IS NOT NULL
                      {date_condition}
                    GROUP BY MONTH(exit_at)
                """
                single_cards = cursor.execute(sql_single, params).fetchall()

                # Doanh thu từ thẻ tháng - Luôn GROUP BY MONTH
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
                        MONTH(start_date) as month, 
                        SUM(monthly_fee) as revenue
                    FROM monthly_cards
                    WHERE is_paid = 1
                      {monthly_condition}
                    GROUP BY MONTH(start_date)
                """
                monthly_cards = cursor.execute(sql_monthly, monthly_params).fetchall()

                # Gộp doanh thu theo month
                revenue_dict = {}
                for row in single_cards:
                    month_val = row[0]
                    revenue_dict[month_val] = revenue_dict.get(month_val, 0) + int(row[1] or 0)

                for row in monthly_cards:
                    month_val = row[0]
                    revenue_dict[month_val] = revenue_dict.get(month_val, 0) + int(row[1] or 0)

                # Đảm bảo có tất cả tháng 1-12, với revenue = 0 nếu không có dữ liệu
                result = [
                    {'month': month, 'revenue': revenue_dict.get(month, 0)}
                    for month in range(1, 13)
                ]

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

    def get_revenue_by_day_in_month(self, month: int, year: int) -> List[Dict]:
        """Doanh thu theo ngày trong tháng"""
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            # Doanh thu thẻ lượt
            sql_single = """
                         SELECT DAY (exit_at) as day, SUM (fee) as revenue
                         FROM card_logs
                         WHERE YEAR (exit_at) = ? \
                           AND MONTH (exit_at) = ?
                           AND exit_at IS NOT NULL \
                           AND fee IS NOT NULL
                         GROUP BY DAY (exit_at) \
                         """
            single_cards = cursor.execute(sql_single, year, month).fetchall()

            # Doanh thu thẻ tháng
            sql_monthly = """
                          SELECT DAY (start_date) as day, SUM (monthly_fee) as revenue
                          FROM monthly_cards
                          WHERE YEAR (start_date) = ? \
                            AND MONTH (start_date) = ?
                            AND is_paid = 1
                          GROUP BY DAY (start_date) \
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
        """Cơ cấu loại xe: thẻ lượt vs thẻ tháng (dựa trên lượt vào/ra)"""
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            # Đếm thẻ lượt: Số lượt từ card_logs
            single_sql = """
                         SELECT COUNT(*)
                         FROM card_logs
                         WHERE 1 = 1 \
                         """
            params = []
            if start_date and end_date:
                single_sql += " AND entry_at BETWEEN ? AND ?"
                params.extend([start_date, end_date])

            single_count = cursor.execute(single_sql, tuple(params) if params else ()).fetchone()[0] or 0

            # Đếm thẻ tháng: Số lượt vào từ monthly_card_logs (entry_at có giá trị)
            monthly_sql = """
                          SELECT COUNT(*)
                          FROM monthly_card_logs
                          WHERE entry_at IS NOT NULL \
                          """
            monthly_params = []
            if start_date and end_date:
                monthly_sql += " AND entry_at BETWEEN ? AND ?"
                monthly_params.extend([start_date, end_date])

            monthly_count = cursor.execute(monthly_sql, tuple(monthly_params) if monthly_params else ()).fetchone()[
                                0] or 0

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
        """Thời gian đỗ xe theo loại thẻ"""
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            # Thời gian đỗ cho thẻ lượt từ card_logs
            single_sql = """
                         SELECT DATEDIFF(MINUTE, entry_at, exit_at)
                         FROM card_logs
                         WHERE exit_at IS NOT NULL \
                         """
            params = []
            if start_date and end_date:
                single_sql += " AND entry_at BETWEEN ? AND ?"
                params.extend([start_date, end_date])

            single_rows = cursor.execute(single_sql, tuple(params) if params else ()).fetchall()
            single_durations = [row[0] for row in single_rows if row[0] is not None and row[0] > 0]

            # Thẻ tháng - Lấy dữ liệu từ monthly_card_logs
            monthly_sql = """
                          SELECT DATEDIFF(MINUTE, entry_at, exit_at)
                          FROM monthly_card_logs
                          WHERE exit_at IS NOT NULL \
                          """
            monthly_params = []
            if start_date and end_date:
                monthly_sql += " AND entry_at BETWEEN ? AND ?"
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
        """Lưu lượng xe theo giờ và ngày trong tuần"""
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            sql = """
                  SELECT CASE \
                             WHEN DATEPART(WEEKDAY, entry_at) = 1 THEN 7 \
                             ELSE DATEPART(WEEKDAY, entry_at) - 1 \
                             END as day_of_week, \
                         DATEPART(HOUR, entry_at) as hour,
                    COUNT(*) as count
                  FROM card_logs
                  WHERE 1=1 \
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

    def get_entries_exits_by_day_of_week(self, start_date: datetime = None, end_date: datetime = None) -> Dict[
        str, List[int]]:
        """Lượt vào/ra theo ngày trong tuần"""
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            # Lượt vào
            entry_sql = """
                        SELECT CASE \
                                   WHEN DATEPART(WEEKDAY, entry_at) = 1 THEN 7 \
                                   ELSE DATEPART(WEEKDAY, entry_at) - 1 \
                                   END as day_of_week, \
                               COUNT(*) as count
                        FROM card_logs
                        WHERE 1=1 \
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

            # Lượt ra
            exit_sql = """
                       SELECT CASE \
                                  WHEN DATEPART(WEEKDAY, exit_at) = 1 THEN 7 \
                                  ELSE DATEPART(WEEKDAY, exit_at) - 1 \
                                  END as day_of_week, \
                              COUNT(*) as count
                       FROM card_logs
                       WHERE exit_at IS NOT NULL \
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
            return {'entries': [0] * 7, 'exits': [0] * 7}
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def get_fee_vs_duration(self, start_date: datetime = None, end_date: datetime = None) -> List[Dict]:
        """Tương quan phí và thời gian đỗ - kết hợp thẻ lượt và thẻ tháng"""
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            result = []

            # Dữ liệu từ thẻ lượt (card_logs)
            sql_single = """
                  SELECT DATEDIFF(MINUTE, entry_at, exit_at) as duration, \
                         fee
                  FROM card_logs
                  WHERE exit_at IS NOT NULL
                    AND fee IS NOT NULL \
                  """
            params = []
            if start_date and end_date:
                sql_single += " AND entry_at BETWEEN ? AND ?"
                params.extend([start_date, end_date])

            rows = cursor.execute(sql_single, tuple(params) if params else ()).fetchall()
            for row in rows:
                if row[0] is not None and row[0] > 0:
                    result.append({'duration': row[0], 'fee': float(row[1] or 0)})

            # Dữ liệu từ thẻ tháng (monthly_card_logs + monthly_cards)
            sql_monthly = """
                  SELECT DATEDIFF(MINUTE, mcl.entry_at, mcl.exit_at) as duration,
                         mc.monthly_fee as fee
                  FROM monthly_card_logs mcl
                  JOIN monthly_cards mc ON mcl.monthly_card_id = mc.id
                  WHERE mcl.exit_at IS NOT NULL \
                  """
            monthly_params = []
            if start_date and end_date:
                sql_monthly += " AND mcl.entry_at BETWEEN ? AND ?"
                monthly_params.extend([start_date, end_date])

            monthly_rows = cursor.execute(sql_monthly, tuple(monthly_params) if monthly_params else ()).fetchall()
            for row in monthly_rows:
                if row[0] is not None and row[0] > 0:
                    result.append({'duration': row[0], 'fee': float(row[1] or 0)})

            return result
        except Exception as e:
            print(f"Lỗi StatisticsDAO.get_fee_vs_duration: {e}")
            return []
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def get_traffic_by_hour(self, start_date: datetime = None, end_date: datetime = None) -> List[int]:
        """Lưu lượng xe theo giờ trong ngày"""
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            sql = """
                  SELECT DATEPART(HOUR, entry_at) as hour, COUNT(*) as count
                  FROM card_logs
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

    def get_overnight_vehicles_count(self) -> int:
        """Xe qua đêm (sau 10 tối đến 6h sáng hoặc chưa ra)"""
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()
            sql = """
                  SELECT COUNT(*)
                  FROM card_logs
                  WHERE exit_at IS NULL
                    AND (
                      (DATEPART(HOUR, entry_at) >= 22 OR DATEPART(HOUR, entry_at) < 6)
                          OR entry_at < CAST(GETDATE() AS DATE)
                      ) \
                  """
            return cursor.execute(sql).fetchone()[0] or 0
        except Exception as e:
            print(f"Lỗi get_overnight_vehicles_count: {e}")
            return 0
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def get_expiring_monthly_cards_count(self, days: int = 3) -> int:
        """Thẻ tháng sắp hết hạn"""
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()
            sql = """
                  SELECT COUNT(*) \
                  FROM monthly_cards
                  WHERE is_active = 1 \
                    AND is_paid = 1
                    AND expiry_date BETWEEN GETDATE() AND DATEADD(day, ?, GETDATE()) \
                  """
            return cursor.execute(sql, days).fetchone()[0] or 0
        except Exception as e:
            print(f"Lỗi get_expiring_monthly_cards_count: {e}")
            return 0
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def get_active_cameras_count(self) -> int:
        """Số camera đang hoạt động"""
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