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

    def get_vehicle_mix(self, start_date: datetime = None, end_date: datetime = None) -> Dict[str, int]:
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            # Đếm thẻ lượt từ cards (card_type = 'single')
            single_sql = """
                         SELECT COUNT(*)
                         FROM cards
                         WHERE card_type = 'single'
                           AND is_active = 0 \
                         """
            params = []

            if start_date and end_date:
                single_sql += " AND entry_at BETWEEN ? AND ?"
                params.extend([start_date, end_date])

            single_count = cursor.execute(single_sql, tuple(params) if params else ()).fetchone()[0] or 0

            # Đếm thẻ tháng: đếm số lượt vào từ card_logs
            monthly_sql = """
                          SELECT COUNT(*)
                          FROM card_logs
                          WHERE 1 = 1 \
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
            import traceback
            traceback.print_exc()
            return {'single': 0, 'monthly': 0}
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_duration_by_card_type(self, start_date: datetime = None, end_date: datetime = None) -> Dict[str, List[int]]:
        """
        Lấy thời gian đỗ (phút) theo loại thẻ
        Returns: {'monthly': [durations], 'single': [durations]}
        """
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            # Thời gian đỗ cho thẻ lượt từ cards
            single_sql = """
                         SELECT DATEDIFF(MINUTE, entry_at, exit_at) as duration
                         FROM cards
                         WHERE exit_at IS NOT NULL
                           AND card_type = 'single'
                           AND is_active = 0 \
                         """
            params = []

            if start_date and end_date:
                single_sql += " AND entry_at BETWEEN ? AND ?"
                params.extend([start_date, end_date])

            single_rows = cursor.execute(single_sql, tuple(params) if params else ()).fetchall()
            single_durations = [row[0] for row in single_rows if row[0] is not None and row[0] > 0]

            # Thẻ tháng: lấy từ card_logs
            monthly_sql = """
                          SELECT DATEDIFF(MINUTE, entry_at, exit_at) as duration
                          FROM card_logs
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
            import traceback
            traceback.print_exc()
            return {'single': [], 'monthly': []}
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_traffic_by_hour_and_day(self, start_date: datetime = None, end_date: datetime = None) -> List[Dict]:
        """
        Lấy lượt xe theo giờ và ngày trong tuần
        Returns: List[{'day_of_week': int, 'hour': int, 'count': int}]
        day_of_week: 1=Thứ 2, 2=Thứ 3, ..., 7=Chủ nhật
        """
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            # SQL Server: DATEPART(WEEKDAY) trả về 1=CN, 2=T2, ..., 7=T7
            # Cần chuyển đổi: (DATEPART(WEEKDAY) + 5) % 7 + 1
            # CN(1) -> 7, T2(2) -> 1, T3(3) -> 2, ..., T7(7) -> 6
            sql = """
                  SELECT CASE \
                             WHEN DATEPART(WEEKDAY, entry_at) = 1 THEN 7 \
                             ELSE DATEPART(WEEKDAY, entry_at) - 1 \
                             END as day_of_week, \
                         DATEPART(HOUR, entry_at) as hour,
                    COUNT(*) as count
                  FROM cards
                  WHERE card_type = 'single'
                    AND is_active = 0 \
                  """
            params = []

            if start_date and end_date:
                sql += " AND entry_at BETWEEN ? AND ?"
                params.extend([start_date, end_date])

            sql += " GROUP BY CASE WHEN DATEPART(WEEKDAY, entry_at) = 1 THEN 7 ELSE DATEPART(WEEKDAY, entry_at) - 1 END, DATEPART(HOUR, entry_at)"
            sql += " ORDER BY day_of_week, hour"

            rows = cursor.execute(sql, tuple(params) if params else ()).fetchall()

            return [
                {'day_of_week': row[0], 'hour': row[1], 'count': row[2]}
                for row in rows
            ]
        except Exception as e:
            print(f"Lỗi StatisticsDAO.get_traffic_by_hour_and_day: {e}")
            import traceback
            traceback.print_exc()
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_entries_exits_by_day_of_week(self, start_date: datetime = None, end_date: datetime = None) -> Dict[
        str, List[int]]:
        """
        Lấy lượt vào/ra theo ngày trong tuần
        Returns: {'entries': [counts], 'exits': [counts]} - mỗi list có 7 phần tử (T2-CN)
        """
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            # Lượt vào từ cards (thẻ lượt)
            entry_sql = """
                        SELECT CASE \
                                   WHEN DATEPART(WEEKDAY, entry_at) = 1 THEN 7 \
                                   ELSE DATEPART(WEEKDAY, entry_at) - 1 \
                                   END as day_of_week, \
                               COUNT(*) as count
                        FROM cards
                        WHERE card_type = 'single'
                          AND is_active = 0 \
                        """
            params = []

            if start_date and end_date:
                entry_sql += " AND entry_at BETWEEN ? AND ?"
                params.extend([start_date, end_date])

            entry_sql += " GROUP BY CASE WHEN DATEPART(WEEKDAY, entry_at) = 1 THEN 7 ELSE DATEPART(WEEKDAY, entry_at) - 1 END"
            entry_sql += " ORDER BY day_of_week"

            entry_rows = cursor.execute(entry_sql, tuple(params) if params else ()).fetchall()

            # Lượt ra
            exit_sql = """
                       SELECT CASE \
                                  WHEN DATEPART(WEEKDAY, exit_at) = 1 THEN 7 \
                                  ELSE DATEPART(WEEKDAY, exit_at) - 1 \
                                  END as day_of_week, \
                              COUNT(*) as count
                       FROM cards
                       WHERE exit_at IS NOT NULL
                         AND card_type = 'single'
                         AND is_active = 0 \
                       """
            exit_params = []

            if start_date and end_date:
                exit_sql += " AND exit_at BETWEEN ? AND ?"
                exit_params.extend([start_date, end_date])

            exit_sql += " GROUP BY CASE WHEN DATEPART(WEEKDAY, exit_at) = 1 THEN 7 ELSE DATEPART(WEEKDAY, exit_at) - 1 END"
            exit_sql += " ORDER BY day_of_week"

            exit_rows = cursor.execute(exit_sql, tuple(exit_params) if exit_params else ()).fetchall()

            # Tạo dict với key là day_of_week (1-7)
            entries_dict = {row[0]: row[1] for row in entry_rows}
            exits_dict = {row[0]: row[1] for row in exit_rows}

            # Tạo list 7 phần tử (1-7 tương ứng T2-CN)
            entries = [entries_dict.get(i, 0) for i in range(1, 8)]
            exits = [exits_dict.get(i, 0) for i in range(1, 8)]

            return {'entries': entries, 'exits': exits}
        except Exception as e:
            print(f"Lỗi StatisticsDAO.get_entries_exits_by_day_of_week: {e}")
            import traceback
            traceback.print_exc()
            return {'entries': [0] * 7, 'exits': [0] * 7}
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_fee_vs_duration(self, start_date: datetime = None, end_date: datetime = None) -> List[Dict]:
        """
        Lấy tương quan phí và thời gian đỗ từ cards (thẻ lượt)
        Returns: List[{'duration': int, 'fee': float}]
        """
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            sql = """
                  SELECT DATEDIFF(MINUTE, entry_at, exit_at) as duration, \
                         fee
                  FROM cards
                  WHERE exit_at IS NOT NULL
                    AND fee IS NOT NULL
                    AND card_type = 'single'
                    AND is_active = 0 \
                  """
            params = []

            if start_date and end_date:
                sql += " AND entry_at BETWEEN ? AND ?"
                params.extend([start_date, end_date])

            rows = cursor.execute(sql, tuple(params) if params else ()).fetchall()

            return [
                {'duration': row[0], 'fee': float(row[1] or 0)}
                for row in rows
                if row[0] is not None and row[1] is not None and row[0] > 0
            ]
        except Exception as e:
            print(f"Lỗi StatisticsDAO.get_fee_vs_duration: {e}")
            import traceback
            traceback.print_exc()
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_traffic_by_hour(self, start_date: datetime = None, end_date: datetime = None) -> List[int]:
        """
        Lấy phân bố lượt xe theo giờ trong ngày từ cards (thẻ lượt)
        Returns: List[int] - 24 phần tử tương ứng 24 giờ
        """
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            sql = """
                  SELECT DATEPART(HOUR, entry_at) as hour,
                    COUNT(*) as count
                  FROM cards
                  WHERE card_type = 'single'
                    AND is_active = 0 \
                  """
            params = []

            if start_date and end_date:
                sql += " AND entry_at BETWEEN ? AND ?"
                params.extend([start_date, end_date])

            sql += " GROUP BY DATEPART(HOUR, entry_at) ORDER BY hour"

            rows = cursor.execute(sql, tuple(params) if params else ()).fetchall()

            # Tạo list 24 phần tử
            hour_dict = {row[0]: row[1] for row in rows}
            result = [hour_dict.get(i, 0) for i in range(24)]

            return result
        except Exception as e:
            print(f"Lỗi StatisticsDAO.get_traffic_by_hour: {e}")
            import traceback
            traceback.print_exc()
            return [0] * 24
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()