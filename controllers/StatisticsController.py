from datetime import datetime
from typing import Dict, List, Tuple, Optional
from services.StatisticsService import StatisticsService


class StatisticsController:
    """Controller điều khiển logic thống kê và biểu đồ"""
    
    def __init__(self, view):
        self.view = view
        self.service = StatisticsService()
        
        # Kết nối signals từ view nếu có
        if hasattr(view, 'filter_changed'):
            view.filter_changed.connect(self.on_filter_changed)
        if hasattr(view, 'chart_type_changed'):
            view.chart_type_changed.connect(self.on_chart_type_changed)

    def get_revenue_trend_data(self, year: int = None) -> Tuple[List[str], List[float]]:
        """Lấy dữ liệu doanh thu theo tháng"""
        return self.service.get_revenue_trend_data(year)

    def get_vehicle_mix_data(self, start_date: datetime = None, end_date: datetime = None) -> Tuple[List[str], List[int]]:
        """Lấy dữ liệu cơ cấu lượt xe"""
        return self.service.get_vehicle_mix_data(start_date, end_date)

    def get_duration_boxplot_data(self, start_date: datetime = None, end_date: datetime = None) -> Dict[str, List[int]]:
        """Lấy dữ liệu thời gian đỗ theo nhóm khách"""
        return self.service.get_duration_boxplot_data(start_date, end_date)

    def get_traffic_heatmap_data(self, start_date: datetime = None, end_date: datetime = None) -> Tuple[List[str], List[str], List[List[int]]]:
        """Lấy dữ liệu heatmap lượt xe"""
        return self.service.get_traffic_heatmap_data(start_date, end_date)

    def get_dow_entries_data(self, start_date: datetime = None, end_date: datetime = None) -> Tuple[List[str], List[int], List[int]]:
        """Lấy dữ liệu lượt vào/ra theo ngày trong tuần"""
        return self.service.get_dow_entries_data(start_date, end_date)

    def get_fee_vs_duration_data(self, start_date: datetime = None, end_date: datetime = None) -> Tuple[List[int], List[float]]:
        """Lấy dữ liệu tương quan phí và thời gian đỗ"""
        return self.service.get_fee_vs_duration_data(start_date, end_date)

    def get_hour_histogram_data(self, start_date: datetime = None, end_date: datetime = None) -> List[int]:
        """Lấy dữ liệu phân bố lượt xe theo giờ"""
        return self.service.get_hour_histogram_data(start_date, end_date)

    def get_date_range_from_quick_filter(self, filter_name: str) -> Tuple[datetime, datetime]:
        """Chuyển đổi filter nhanh thành khoảng thời gian"""
        return self.service.get_date_range_from_quick_filter(filter_name)

    def on_filter_changed(self, start_date: datetime, end_date: datetime):
        """Xử lý khi filter thay đổi"""
        # Có thể cập nhật lại biểu đồ ở đây
        if hasattr(self.view, 'refresh_charts'):
            self.view.refresh_charts(start_date, end_date)

    def on_chart_type_changed(self, chart_type: str):
        """Xử lý khi loại biểu đồ thay đổi"""
        if hasattr(self.view, 'update_chart'):
            self.view.update_chart(chart_type)

