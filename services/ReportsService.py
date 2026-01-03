from dao.ReportDAO import ReportDAO


class ReportService:
    def __init__(self):
        self.dao = ReportDAO()

    def get_report_data(self, start_date, end_date):
        rows = self.dao.get_parking_history(start_date, end_date)

        total_in = 0
        total_out = 0
        total_revenue = 0
        table_data = []

        for row in rows:
            entry_time = row[0].strftime("%H:%M %d/%m/%Y") if row[0] else ""
            fee = int(row[4]) if row[4] else 0
            action = str(row[3])

            if action == "Vào":
                total_in += 1
            elif action == "Ra":
                total_out += 1
                total_revenue += fee

            table_data.append((
                entry_time,
                row[1],
                row[2],
                action,
                f"{fee:,}₫",
                row[5]
            ))

        avg_fee = total_revenue / total_out if total_out > 0 else 0

        return {
            "table_data": table_data,
            "stats": {
                "in": str(total_in),
                "out": str(total_out),
                "revenue": f"{int(total_revenue):,}₫",
                "avg": f"{int(avg_fee):,}₫/xe"
            }
        }

    def get_overview_stats(self):
        from datetime import date
        today = date.today()
        return {
            "revenue": self.dao.get_daily_revenue(today),
            "parked": self.dao.get_currently_parked_count(),
            "entries": self.dao.get_today_entries_count(today),
            "monthly": self.dao.get_active_monthly_cards_count(),
            "overnight": self.dao.get_overnight_vehicles_count(),
            "expiring": self.dao.get_expiring_monthly_cards_count(3),
            "cameras": self.dao.get_active_cameras_count()
        }
