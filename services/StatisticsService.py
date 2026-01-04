from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dao.StatisticsDAO import StatisticsDAO
from datetime import datetime
import calendar


class StatisticsService:

    def __init__(self):
        self._dao = StatisticsDAO()

    def get_revenue_trend_data(
        self, year: int = None, start_date: datetime = None, end_date: datetime = None
    ) -> Tuple[List[str], List[float]]:
        """
        Lấy dữ liệu doanh thu theo tháng để vẽ biểu đồ
        """
        data = self._dao.get_revenue_by_month(year, start_date, end_date)

        if not data:
            # Trả về dữ liệu mẫu nếu không có dữ liệu
            if start_date and end_date:
                # Nếu có khoảng thời gian, trả về các tháng trong khoảng đó
                start_month = start_date.month
                end_month = end_date.month
                months = [f"T{i}" for i in range(start_month, end_month + 1)]
                revenues = [0.0] * len(months)
            else:
                months = [
                    "T1",
                    "T2",
                    "T3",
                    "T4",
                    "T5",
                    "T6",
                    "T7",
                    "T8",
                    "T9",
                    "T10",
                    "T11",
                    "T12",
                ]
                revenues = [0.0] * 12
            return months, revenues

        # Nếu có khoảng thời gian, chỉ trả về các tháng trong khoảng đó
        if start_date and end_date:
            start_month = start_date.month
            end_month = end_date.month
            months = [f"T{i}" for i in range(start_month, end_month + 1)]
            revenues = [0.0] * (end_month - start_month + 1)
            
            for item in data:
                month_idx = item["month"] - start_month  # index từ 0 trong khoảng
                if 0 <= month_idx < len(revenues):
                    revenues[month_idx] = item["revenue"] / 1000  # nghìn đồng
        else:
            # Chuyển đổi sang format cho biểu đồ (toàn bộ năm)
            month_names = [
                "T1",
                "T2",
                "T3",
                "T4",
                "T5",
                "T6",
                "T7",
                "T8",
                "T9",
                "T10",
                "T11",
                "T12",
            ]
            revenues = [0.0] * 12

            for item in data:
                month_idx = item["month"] - 1  # month từ 1-12, index từ 0-11
                if 0 <= month_idx < 12:
                    revenues[month_idx] = item["revenue"] / 1000  # nghìn đồng

            months = month_names

        return months, revenues

    def get_daily_revenue_data(
        self, month: int = None, year: int = None
    ) -> Tuple[List[str], List[float]]:
        now = datetime.now()
        m = month if month else now.month
        y = year if year else now.year

        data = self._dao.get_revenue_by_day_in_month(m, y)

        _, num_days = calendar.monthrange(y, m)
        days = list(range(1, num_days + 1))
        revenues = [0.0] * num_days

        for item in data:
            day_idx = item["day"] - 1
            if 0 <= day_idx < num_days:
                revenues[day_idx] = item["revenue"] / 1000  # nghìn đồng

        return days, revenues

    def get_vehicle_mix_data(
        self, start_date: datetime = None, end_date: datetime = None
    ) -> Tuple[List[str], List[int]]:
        """
        Lấy dữ liệu cơ cấu lượt xe
        Returns: (labels, values)
        """
        data = self._dao.get_vehicle_mix(start_date, end_date)

        labels = ["Thẻ Tháng", "Lượt / Vãng lai"]
        values = [data.get("monthly", 0), data.get("single", 0)]

        return labels, values

    def get_duration_boxplot_data(
        self, start_date: datetime = None, end_date: datetime = None
    ) -> Dict[str, List[int]]:
        """
        Lấy dữ liệu thời gian đỗ theo nhóm khách
        Returns: {'Thẻ Tháng': [durations], 'Lượt / Vãng lai': [durations]}
        """
        data = self._dao.get_duration_by_card_type(start_date, end_date)

        # Nếu không có dữ liệu, trả về mẫu
        if not data.get("single") and not data.get("monthly"):
            return {
                "Thẻ Tháng": [120, 90, 80, 150, 110, 95, 130],
                "Lượt / Vãng lai": [
                    20,
                    35,
                    40,
                    50,
                    60,
                    30,
                    25,
                    45,
                    15,
                    20,
                    18,
                    25,
                    30,
                    22,
                    28,
                ],
            }

        return {
            "Thẻ Tháng": data.get("monthly", []),
            "Lượt / Vãng lai": data.get("single", []),
        }

    def get_traffic_heatmap_data(
        self, start_date: datetime = None, end_date: datetime = None
    ) -> Tuple[List[str], List[str], List[List[int]]]:
        """
        Lấy dữ liệu heatmap lượt xe theo giờ & ngày
        Returns: (days, hours, traffic_matrix)
        """
        data = self._dao.get_traffic_by_hour_and_day(start_date, end_date)

        days = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
        hours = ["06-09", "09-12", "12-15", "15-18", "18-22"]
        hour_ranges = [(6, 9), (9, 12), (12, 15), (15, 18), (18, 22)]

        # Tạo ma trận 7x5
        traffic_matrix = [[0] * len(hours) for _ in range(len(days))]

        # Tạo dict để tra cứu nhanh
        data_dict = {}
        for item in data:
            key = (item["day_of_week"], item["hour"])
            data_dict[key] = item["count"]

        # Điền dữ liệu vào ma trận
        for day_idx, day_of_week in enumerate(range(1, 8)):  # 1-7 tương ứng T2-CN
            for hour_idx, (start_hour, end_hour) in enumerate(hour_ranges):
                count = 0
                for hour in range(start_hour, end_hour):
                    key = (day_of_week, hour)
                    count += data_dict.get(key, 0)
                traffic_matrix[day_idx][hour_idx] = count

        return days, hours, traffic_matrix

    def get_dow_entries_data(
        self, start_date: datetime = None, end_date: datetime = None
    ) -> Tuple[List[str], List[int], List[int]]:
        """
        Lấy dữ liệu lượt vào/ra theo ngày trong tuần
        Returns: (days, entries, exits)
        """
        data = self._dao.get_entries_exits_by_day_of_week(start_date, end_date)

        days = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
        entries = data.get("entries", [0] * 7)
        exits = data.get("exits", [0] * 7)

        return days, entries, exits

    def get_fee_vs_duration_data(
        self, start_date: datetime = None, end_date: datetime = None
    ) -> Tuple[List[int], List[float]]:
        """
        Lấy dữ liệu tương quan phí và thời gian đỗ
        Returns: (durations, fees)
        """
        data = self._dao.get_fee_vs_duration(start_date, end_date)

        if not data:
            # Dữ liệu mẫu
            durations = [20, 35, 40, 50, 60, 80, 100, 120, 140, 160]
            fees = [15, 25, 28, 32, 36, 45, 55, 60, 70, 78]
            return durations, fees

        durations = [item["duration"] for item in data]
        fees = [item["fee"] / 1000 for item in data]  # Chuyển sang nghìn đồng

        return durations, fees

    def get_hour_histogram_data(
        self, start_date: datetime = None, end_date: datetime = None
    ) -> List[int]:
        """
        Lấy dữ liệu phân bố lượt xe theo giờ
        Returns: List[int] - 24 phần tử
        """
        data = self._dao.get_traffic_by_hour(start_date, end_date)

        if not data or sum(data) == 0:
            # Dữ liệu mẫu
            return [
                0,
                0,
                0,
                0,
                0,
                0,
                1,
                2,
                3,
                2,
                1,
                1,
                1,
                0,
                1,
                2,
                3,
                4,
                3,
                2,
                1,
                0,
                0,
                0,
            ]

        return data

    def get_date_range_from_quick_filter(
        self, filter_name: str
    ) -> Tuple[datetime, datetime]:
        """
        Chuyển đổi filter nhanh thành khoảng thời gian
        Returns: (start_date, end_date)
        """
        now = datetime.now()
        end_date = now.replace(hour=23, minute=59, second=59, microsecond=999999)

        if filter_name == "Hôm nay":
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif filter_name == "Tuần này":
            # Lấy thứ 2 đầu tuần
            days_since_monday = now.weekday()
            start_date = (now - timedelta(days=days_since_monday)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
        elif filter_name == "Tháng này":
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        elif filter_name == "Năm nay":
            start_date = now.replace(
                month=1, day=1, hour=0, minute=0, second=0, microsecond=0
            )
        else:
            # Mặc định là hôm nay
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)

        return start_date, end_date

    def get_overnight_vehicles_count(self) -> int:
        return self._dao.get_overnight_vehicles_count()

    def get_expiring_monthly_cards_count(self) -> int:
        return self._dao.get_expiring_monthly_cards_count()

    def get_active_cameras_count(self) -> int:
        return self._dao.get_active_cameras_count()
