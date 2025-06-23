import csv
from collections import defaultdict
from typing import List, Dict, Tuple


def load_csv(path: str) -> List[Dict[str, str]]:
    """Load events from a CSV file."""
    data = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data


def suggest_rules(events: List[Dict[str, str]], threshold: int = 3) -> List[Dict[str, str]]:
    """Return frequent (time, device, action) combinations as rule suggestions."""
    counts: Dict[Tuple[str, str, str], int] = defaultdict(int)
    for e in events:
        key = (e.get('timestamp', '')[11:16], e.get('device'), e.get('action'))
        counts[key] += 1
    suggestions = []
    for (time_str, device, action), count in counts.items():
        if count >= threshold:
            suggestions.append({'time': time_str, 'device': device, 'action': action})
    return suggestions


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Analyze dataset and print rule suggestions.')
    parser.add_argument('csv', help='CSV dataset file')
    parser.add_argument('--threshold', type=int, default=3, help='frequency threshold')
    args = parser.parse_args()

    events = load_csv(args.csv)
    rules = suggest_rules(events, threshold=args.threshold)
    for r in rules:
        print(f"{r['time']}에 {r['device']} {r['action']} ({args.threshold}+회)")
