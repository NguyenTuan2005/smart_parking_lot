from dao.ReportDAO import ReportDAO


class ReportService:
    def __init__(self):
        self.dao = ReportDAO()

    def get_report_data(self, start_date, end_date):
        rows = self.dao.get_parking_history(start_date, end_date)
        print("[SERVICE] Rows fetched:", len(rows))

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
