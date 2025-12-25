from datetime import datetime, timedelta
import os
import json
import webbrowser

from config import APPS, WINDOW_DAYS, OUTPUT_DIR
from orchestrator.daily_controller import DailyController


# ---------------- RESET STATE ----------------
def reset_state():
    os.makedirs("storage/topic_store", exist_ok=True)
    os.makedirs("storage/trend_store", exist_ok=True)
    os.makedirs("storage/review_store", exist_ok=True)

    with open("storage/topic_store/topics.json", "w") as f:
        json.dump({}, f)

    with open("storage/trend_store/trends.json", "w") as f:
        json.dump({}, f)

    with open("storage/review_store/seen_reviews.json", "w") as f:
        json.dump([], f)


# ---------------- USER INPUT ----------------
def get_app_choice():
    print("Choose App:")
    print("1. Swiggy")
    print("2. Zomato")

    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "1":
        return "swiggy"
    elif choice == "2":
        return "zomato"
    else:
        raise ValueError("Invalid app choice")


def get_start_date():
    date_str = input("Enter start date (YYYY-MM-DD): ").strip()
    return datetime.strptime(date_str, "%Y-%m-%d").date()


# ---------------- MAIN ----------------
if __name__ == "__main__":
    reset_state()

    app_key = get_app_choice()
    start_date = get_start_date()

    app_id = APPS[app_key]["app_id"]

    end_date = start_date + timedelta(days=WINDOW_DAYS - 1)

    controller = DailyController()

    current_date = start_date
    day_index = 0

    while current_date <= end_date:
        controller.run_for_date(
            app_link=app_id,
            date=current_date.isoformat(),
            day_index=day_index
        )

        current_date += timedelta(days=1)
        day_index += 1

    html_path = os.path.abspath(
        os.path.join(OUTPUT_DIR, "trend_report.html")
    )
    webbrowser.open(html_path)
