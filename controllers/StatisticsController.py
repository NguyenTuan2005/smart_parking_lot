from datetime import datetime
from typing import Dict, List, Tuple, Optional
from services.StatisticsService import StatisticsService


class StatisticsController: 
    def __init__(self, view):
        self.view = view
        self.service = StatisticsService()

        if hasattr(view, 'filter_changed'):
            view.filter_changed.connect(self.on_filter_changed)
        if hasattr(view, 'chart_type_changed'):
            view.chart_type_changed.connect(self.on_chart_type_changed)

    def get_revenue_trend_data(self, year: int = None, start_date: datetime = None, end_date: datetime = None) -> Tuple[List[str], List[float]]:
        return self.service.get_revenue_trend_data(year, start_date, end_date)

    def get_daily_revenue_data(self, month: int = None, year: int = None) -> Tuple[List[str], List[float]]:
        return self.service.get_daily_revenue_data(month, year)

    def get_vehicle_mix_data(self, start_date: datetime = None, end_date: datetime = None) -> Tuple[List[str], List[int]]:
        return self.service.get_vehicle_mix_data(start_date, end_date)

    def get_duration_boxplot_data(self, start_date: datetime = None, end_date: datetime = None) -> Dict[str, List[int]]:
        return self.service.get_duration_boxplot_data(start_date, end_date)

    def get_traffic_heatmap_data(self, start_date: datetime = None, end_date: datetime = None) -> Tuple[List[str], List[str], List[List[int]]]:
        return self.service.get_traffic_heatmap_data(start_date, end_date)

    def get_dow_entries_data(self, start_date: datetime = None, end_date: datetime = None) -> Tuple[List[str], List[int], List[int]]:
        return self.service.get_dow_entries_data(start_date, end_date)

    def get_fee_vs_duration_data(self, start_date: datetime = None, end_date: datetime = None) -> Tuple[List[int], List[float]]:
        return self.service.get_fee_vs_duration_data(start_date, end_date)

    def get_hour_histogram_data(self, start_date: datetime = None, end_date: datetime = None) -> List[int]:
        return self.service.get_hour_histogram_data(start_date, end_date)

    def get_date_range_from_quick_filter(self, filter_name: str) -> Tuple[datetime, datetime]:
        return self.service.get_date_range_from_quick_filter(filter_name)

    def get_overnight_vehicles_count(self) -> int:
        return self.service.get_overnight_vehicles_count()

    def get_expiring_monthly_cards_count(self) -> int:
        return self.service.get_expiring_monthly_cards_count()

    def get_active_cameras_count(self) -> int:
        return self.service.get_active_cameras_count()

    def on_filter_changed(self, start_date: datetime, end_date: datetime):
        if hasattr(self.view, 'refresh_charts'):
            self.view.refresh_charts(start_date, end_date)

    def on_chart_type_changed(self, chart_type: str):
        if hasattr(self.view, 'update_chart'):
            self.view.update_chart(chart_type)

