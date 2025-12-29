from datetime import datetime
from typing import List, Dict, Tuple, Optional
from db.database import Database


class StatisticsDAO:
    """DAO để lấy dữ liệu thống kê từ database"""
    
    def __init__(self):
        self._db = Database()

    def get_revenue_by_month(self, year: int = None) -> List[Dict]:
        """
        Lấy doanh thu theo tháng
        Returns: List[{'month': int, 'revenue': float}]
        """
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()
            
            if year:
                sql = """
                    SELECT 
                        MONTH(entry_at) as month,
                        SUM(fee) as revenue
                    FROM card_logs
                    WHERE YEAR(entry_at) = ? 
                        AND exit_at IS NOT NULL
                        AND fee IS NOT NULL
                    GROUP BY MONTH(entry_at)
                    ORDER BY month
                """
                rows = cursor.execute(sql, year).fetchall()
            else:
                sql = """
                    SELECT 
                        YEAR(entry_at) as year,
                        MONTH(entry_at) as month,
                        SUM(fee) as revenue
                    FROM card_logs
                    WHERE exit_at IS NOT NULL
                        AND fee IS NOT NULL
                    GROUP BY YEAR(entry_at), MONTH(entry_at)
                    ORDER BY year, month
                """
                rows = cursor.execute(sql).fetchall()
            
            result = []
            for row in rows:
                if year:
                    result.append({'month': row[0], 'revenue': float(row[1] or 0)})
                else:
                    result.append({'year': row[0], 'month': row[1], 'revenue': float(row[2] or 0)})
            
            return result
        except Exception as e:
            print(f"Lỗi StatisticsDAO.get_revenue_by_month: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_vehicle_mix(self, start_date: datetime = None, end_date: datetime = None) -> Dict[str, int]:
        """
        Lấy cơ cấu lượt xe: thẻ tháng vs thẻ lượt
        Returns: {'monthly': int, 'single': int}
        """
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()
            
            # Đếm thẻ lượt từ card_logs (cards table)
            single_sql = """
                SELECT COUNT(*) 
                FROM card_logs cl
                INNER JOIN cards c ON cl.card_id = c.id
                WHERE c.is_active = 1
            """
            params = []
            
            if start_date and end_date:
                single_sql += " AND cl.entry_at BETWEEN ? AND ?"
                params.extend([start_date, end_date])
            
            single_count = cursor.execute(single_sql, tuple(params)).fetchone()[0] or 0
            
            # Đếm thẻ tháng: đếm số lượt vào từ card_logs mà card_id thuộc monthly_cards
            monthly_sql = """
                SELECT COUNT(DISTINCT cl.id)
                FROM card_logs cl
                INNER JOIN monthly_cards mc ON cl.card_id = mc.id
                WHERE mc.is_active = 1
            """
            monthly_params = []
            
            if start_date and end_date:
                monthly_sql += " AND cl.entry_at BETWEEN ? AND ?"
                monthly_params.extend([start_date, end_date])
            
            monthly_count = cursor.execute(monthly_sql, tuple(monthly_params)).fetchone()[0] or 0
            
            return {
                'single': single_count,
                'monthly': monthly_count
            }
        except Exception as e:
            print(f"Lỗi StatisticsDAO.get_vehicle_mix: {e}")
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
            
            # Thời gian đỗ cho thẻ lượt
            single_sql = """
                SELECT DATEDIFF(MINUTE, cl.entry_at, cl.exit_at) as duration
                FROM card_logs cl
                INNER JOIN cards c ON cl.card_id = c.id
                WHERE cl.exit_at IS NOT NULL
                    AND c.is_active = 1
            """
            params = []
            
            if start_date and end_date:
                single_sql += " AND cl.entry_at BETWEEN ? AND ?"
                params.extend([start_date, end_date])
            
            single_rows = cursor.execute(single_sql, tuple(params)).fetchall()
            single_durations = [row[0] for row in single_rows if row[0] is not None]
            
            # Thẻ tháng: lấy từ payments (giả sử thẻ tháng đỗ cả tháng = 30 ngày)
            # Hoặc có thể tính từ card_logs nếu có
            monthly_durations = []  # Có thể tính từ dữ liệu khác nếu có
            
            return {
                'single': single_durations,
                'monthly': monthly_durations
            }
        except Exception as e:
            print(f"Lỗi StatisticsDAO.get_duration_by_card_type: {e}")
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
        """
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()
            
            sql = """
                SELECT 
                    DATEPART(WEEKDAY, entry_at) as day_of_week,
                    DATEPART(HOUR, entry_at) as hour,
                    COUNT(*) as count
                FROM card_logs
                WHERE 1=1
            """
            params = []
            
            if start_date and end_date:
                sql += " AND entry_at BETWEEN ? AND ?"
                params.extend([start_date, end_date])
            
            sql += " GROUP BY DATEPART(WEEKDAY, entry_at), DATEPART(HOUR, entry_at) ORDER BY day_of_week, hour"
            
            rows = cursor.execute(sql, tuple(params)).fetchall()
            
            return [
                {'day_of_week': row[0], 'hour': row[1], 'count': row[2]}
                for row in rows
            ]
        except Exception as e:
            print(f"Lỗi StatisticsDAO.get_traffic_by_hour_and_day: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_entries_exits_by_day_of_week(self, start_date: datetime = None, end_date: datetime = None) -> Dict[str, List[int]]:
        """
        Lấy lượt vào/ra theo ngày trong tuần
        Returns: {'entries': [counts], 'exits': [counts]} - mỗi list có 7 phần tử (T2-CN)
        """
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()
            
            sql = """
                SELECT 
                    DATEPART(WEEKDAY, entry_at) as day_of_week,
                    COUNT(*) as count
                FROM card_logs
                WHERE 1=1
            """
            params = []
            
            if start_date and end_date:
                sql += " AND entry_at BETWEEN ? AND ?"
                params.extend([start_date, end_date])
            
            sql += " GROUP BY DATEPART(WEEKDAY, entry_at) ORDER BY day_of_week"
            
            entry_rows = cursor.execute(sql, tuple(params)).fetchall()
            
            # Lấy lượt ra
            exit_sql = """
                SELECT 
                    DATEPART(WEEKDAY, exit_at) as day_of_week,
                    COUNT(*) as count
                FROM card_logs
                WHERE exit_at IS NOT NULL
            """
            exit_params = []
            
            if start_date and end_date:
                exit_sql += " AND exit_at BETWEEN ? AND ?"
                exit_params.extend([start_date, end_date])
            
            exit_sql += " GROUP BY DATEPART(WEEKDAY, exit_at) ORDER BY day_of_week"
            
            exit_rows = cursor.execute(exit_sql, tuple(exit_params)).fetchall()
            
            # Tạo dict với key là day_of_week
            entries_dict = {row[0]: row[1] for row in entry_rows}
            exits_dict = {row[0]: row[1] for row in exit_rows}
            
            # Tạo list 7 phần tử (1-7 tương ứng T2-CN)
            entries = [entries_dict.get(i, 0) for i in range(1, 8)]
            exits = [exits_dict.get(i, 0) for i in range(1, 8)]
            
            return {'entries': entries, 'exits': exits}
        except Exception as e:
            print(f"Lỗi StatisticsDAO.get_entries_exits_by_day_of_week: {e}")
            return {'entries': [0] * 7, 'exits': [0] * 7}
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_fee_vs_duration(self, start_date: datetime = None, end_date: datetime = None) -> List[Dict]:
        """
        Lấy tương quan phí và thời gian đỗ
        Returns: List[{'duration': int, 'fee': float}]
        """
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()
            
            sql = """
                SELECT 
                    DATEDIFF(MINUTE, entry_at, exit_at) as duration,
                    fee
                FROM card_logs
                WHERE exit_at IS NOT NULL
                    AND fee IS NOT NULL
            """
            params = []
            
            if start_date and end_date:
                sql += " AND entry_at BETWEEN ? AND ?"
                params.extend([start_date, end_date])
            
            rows = cursor.execute(sql, tuple(params)).fetchall()
            
            return [
                {'duration': row[0], 'fee': float(row[1] or 0)}
                for row in rows
                if row[0] is not None and row[1] is not None
            ]
        except Exception as e:
            print(f"Lỗi StatisticsDAO.get_fee_vs_duration: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_traffic_by_hour(self, start_date: datetime = None, end_date: datetime = None) -> List[int]:
        """
        Lấy phân bố lượt xe theo giờ trong ngày
        Returns: List[int] - 24 phần tử tương ứng 24 giờ
        """
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()
            
            sql = """
                SELECT 
                    DATEPART(HOUR, entry_at) as hour,
                    COUNT(*) as count
                FROM card_logs
                WHERE 1=1
            """
            params = []
            
            if start_date and end_date:
                sql += " AND entry_at BETWEEN ? AND ?"
                params.extend([start_date, end_date])
            
            sql += " GROUP BY DATEPART(HOUR, entry_at) ORDER BY hour"
            
            rows = cursor.execute(sql, tuple(params)).fetchall()
            
            # Tạo list 24 phần tử
            hour_dict = {row[0]: row[1] for row in rows}
            result = [hour_dict.get(i, 0) for i in range(24)]
            
            return result
        except Exception as e:
            print(f"Lỗi StatisticsDAO.get_traffic_by_hour: {e}")
            return [0] * 24
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_card_logs_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """
        Lấy tất cả card_logs trong khoảng thời gian
        Returns: List[Dict] với các thông tin cần thiết
        """
        conn = None
        cursor = None
        try:
            conn = self._db.connect()
            cursor = conn.cursor()
            
            sql = """
                SELECT 
                    cl.id,
                    cl.entry_at,
                    cl.exit_at,
                    cl.fee,
                    c.id as card_id,
                    CASE 
                        WHEN mc.id IS NOT NULL THEN 'monthly'
                        ELSE 'single'
                    END as card_type
                FROM card_logs cl
                INNER JOIN cards c ON cl.card_id = c.id
                LEFT JOIN monthly_cards mc ON c.id = mc.id
                WHERE cl.entry_at BETWEEN ? AND ?
                ORDER BY cl.entry_at DESC
            """
            
            rows = cursor.execute(sql, start_date, end_date).fetchall()
            
            return [
                {
                    'id': row[0],
                    'entry_at': row[1],
                    'exit_at': row[2],
                    'fee': row[3],
                    'card_id': row[4],
                    'card_type': row[5]
                }
                for row in rows
            ]
        except Exception as e:
            print(f"Lỗi StatisticsDAO.get_card_logs_by_date_range: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
