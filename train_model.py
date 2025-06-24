import csv
import sys
import pickle
from typing import Dict, List
from sklearn.linear_model import LogisticRegression


def load_dataset(path: str) -> List[Dict[str, str]]:
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def preprocess(data: List[Dict[str, str]]):
    X = []
    y = []
    device_map: Dict[str, int] = {}
    for row in data:
        ts = row['timestamp']
        hh, mm = map(int, ts[11:16].split(':'))
        minutes = hh * 60 + mm
        device = row['device']
        if device not in device_map:
            device_map[device] = len(device_map)
        device_id = device_map[device]
        action = row['action'].strip().upper()
        label = 1 if action == 'ON' else 0
        X.append([minutes, device_id])
        y.append(label)
    return X, y, device_map


def train(csv_path: str, model_path: str = 'trained_model.pkl'):
    data = load_dataset(csv_path)
    X, y, device_map = preprocess(data)
    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)
    with open(model_path, 'wb') as f:
        pickle.dump({'model': model, 'device_map': device_map}, f)
    print(f'Model saved to {model_path}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python train_model.py <csv_path> [model_path]')
        sys.exit(1)
    csv_path = sys.argv[1]
    model_path = sys.argv[2] if len(sys.argv) > 2 else 'trained_model.pkl'
    train(csv_path, model_path)
