import csv
from datetime import datetime, timedelta
from typing import List, Dict


def generate_script_data(script: List[Dict], start_date: str, days: int) -> List[Dict]:
    """Generate time-series data based on a simple script.

    Args:
        script: list of dicts with keys 'time', 'device', 'action'.
        start_date: starting date string 'YYYY-MM-DD'.
        days: number of days to repeat the script.
    """
    result = []
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    for d in range(days):
        day_dt = start_dt + timedelta(days=d)
        for entry in script:
            hh_mm = datetime.strptime(entry["time"], "%H:%M").time()
            dt = datetime.combine(day_dt, hh_mm)
            result.append({"timestamp": dt.isoformat(),
                           "device": entry["device"],
                           "action": entry["action"]})
    return result


def save_csv(data: List[Dict], path: str) -> None:
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "device", "action"])
        writer.writeheader()
        for row in data:
            writer.writerow(row)


if __name__ == "__main__":
    SCRIPT = [
        {"time": "22:00", "device": "거실", "action": "OFF"},
        {"time": "07:00", "device": "거실", "action": "ON"},
    ]
    dataset = generate_script_data(SCRIPT, "2024-01-01", 2)
    save_csv(dataset, "sample_data.csv")
    print("sample_data.csv created")
