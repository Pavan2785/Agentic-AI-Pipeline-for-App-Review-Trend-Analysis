import json
import os
import csv
from agents import BaseAgent
from datetime import datetime, timedelta
from typing import Dict


TREND_STORE_PATH = "storage/trend_store/trends.json"
OUTPUT_DIR = "output"
WINDOW_DAYS = 30


class ReportGeneratorAgent(BaseAgent):
    def __init__(self):
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    def run(self, target_date: str):
        trend_store = self._load_trend_store()
        date_columns = self._generate_date_range(target_date)

        # Build full report
        json_report = {}
        for topic, date_counts in trend_store.items():
            json_report[topic] = {
                d: date_counts.get(d, 0) for d in date_columns
            }

        # Filter out topics with all-zero values
        filtered_report = {
            topic: counts
            for topic, counts in json_report.items()
            if any(value > 0 for value in counts.values())
        }

        # Write outputs
        self._write_json(filtered_report)
        self._write_csv(filtered_report, date_columns)
        self._write_html(filtered_report, date_columns)

    def _load_trend_store(self) -> Dict:
        with open(TREND_STORE_PATH, "r") as f:
            return json.load(f)

    def _generate_date_range(self, target_date: str):
        end = datetime.strptime(target_date, "%Y-%m-%d").date()
        start = end - timedelta(days=WINDOW_DAYS - 1)

        dates = []
        current = start
        while current <= end:
            dates.append(current.isoformat())
            current += timedelta(days=1)

        return dates

    def _write_json(self, report: Dict):
        path = os.path.join(OUTPUT_DIR, "trend_report.json")
        with open(path, "w") as f:
            json.dump(report, f, indent=2)
        return path

    def _write_csv(self, report: Dict, dates):
        path = os.path.join(OUTPUT_DIR, "trend_report.csv")

        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Topic"] + dates)

            for topic, date_counts in report.items():
                writer.writerow([topic] + [date_counts[d] for d in dates])

        return os.path.abspath(path)

    def _write_html(self, report: Dict, dates):
        path = os.path.join(OUTPUT_DIR, "trend_report.html")

        with open(path, "w", encoding="utf-8") as f:
            f.write("<html><head><title>Trend Report</title>")
            f.write("""
                <style>
    body {
        font-family: "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        background-color: #f8f9f8;
        padding: 40px;
        color: #2f362f;
    }

    h2 {
        margin-bottom: 24px;
        color: #3e4d41;
        font-weight: 600;
        letter-spacing: -0.01em;
    }

    table {
        border-collapse: separate;
        border-spacing: 0;
        width: 100%;
        background-color: #ffffff;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        border: 1px solid #e1e8e1;
    }

    th, td {
        border-bottom: 1px solid #edf2ed;
        padding: 14px 18px;
        text-align: center;
        font-size: 14px;
    }

    th {
        background-color: #4a5d4e;
        color: #ffffff;
        font-weight: 500;
        text-transform: uppercase;
        font-size: 12px;
        letter-spacing: 0.05em;
        position: sticky;
        top: 0;
        z-index: 1;
    }

    td:first-child {
        font-weight: 600;
        text-align: left;
        color: #2f362f;
        background-color: #fbfcfa;
        border-right: 1px solid #edf2ed;
    }

    tr:nth-child(even) {
        background-color: #f1f4f1;
    }

    tr:hover {
        background-color: #e2e8e2 !important;
        transition: background-color 0.2s ease;
    }
</style>
            """)
            f.write("</head><body>")
            f.write("<h2>30-Day Trend Report</h2>")
            f.write("<table>")

            # Header
            f.write("<tr><th>Topic</th>")
            for d in dates:
                f.write(f"<th>{d}</th>")
            f.write("</tr>")

            # Rows
            for topic, counts in report.items():
                f.write(f"<tr><td>{topic}</td>")
                for d in dates:
                    f.write(f"<td>{counts[d]}</td>")
                f.write("</tr>")

            f.write("</table></body></html>")

        return os.path.abspath(path)
