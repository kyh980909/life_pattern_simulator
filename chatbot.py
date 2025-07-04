import re
import sys
from typing import Tuple, List, Dict
from rule_set import RuleSet
from pattern_analyzer import load_csv, suggest_rules

class Chatbot:
    """Simple command-line chatbot for creating automation rules."""

    def __init__(self, rules: RuleSet):
        self.rules = rules

    def analyze_dataset(self, events: List[Dict[str, str]]) -> None:
        """Suggest rules based on dataset analysis."""
        suggestions = suggest_rules(events)
        for s in suggestions:
            phrase = f"매일 {s['time']}에 {s['device']}를 {s['action']} 하시겠습니까? (Yes/No)"
            print(phrase)
            ans = input().strip().lower()
            if ans == 'yes':
                self.rules.add_rule({'device': s['device'], 'action': s['action'], 'time': s['time']})
                print('규칙이 저장되었습니다.')

    @staticmethod
    def _extract_time(text: str) -> str | None:
        """Return first HH:MM string in the text if present."""
        match = re.search(r"([01]\d|2[0-3]):([0-5]\d)", text)
        return match.group(0) if match else None

    @staticmethod
    def _extract_device_action(text: str) -> Tuple[str | None, str | None]:
        text_lower = text.lower()
        device = None
        action = None
        if "조명" in text_lower:
            device = "거실"  # 데모용 고정값
            if any(word in text_lower for word in ["켜", "on"]):
                action = "ON"
            elif any(word in text_lower for word in ["꺼", "off"]):
                action = "OFF"
        return device, action

    def suggest_rule(self, text: str) -> None:
        time_str = self._extract_time(text)
        device, action = self._extract_device_action(text)

        if time_str and device and action:
            print(f"매일 {time_str}에 {device}를 {action} 하시겠습니까? (Yes/No)")
            ans = input().strip().lower()
            if ans == "yes":
                self.rules.add_rule({"device": device, "action": action, "time": time_str})
                print("규칙이 저장되었습니다.")
            else:
                print("규칙이 저장되지 않았습니다.")
        else:
            print("예시: '22:00에 거실 조명 꺼줘'와 같이 입력해주세요.")

    def run(self, dataset_path: str | None = None) -> None:
        print("자동화 권고 챗봇 (종료하려면 'quit' 입력)")

        if dataset_path:
            try:
                events = load_csv(dataset_path)
                print(f"데이터셋 {dataset_path} 분석 결과 권고를 제시합니다.")
                self.analyze_dataset(events)
            except FileNotFoundError:
                print(f"데이터셋 {dataset_path}을 찾을 수 없습니다.")

        while True:
            user_input = input("사용자 입력> ").strip()
            if user_input.lower() in {"quit", "exit"}:
                break
            self.suggest_rule(user_input)

if __name__ == "__main__":
    dataset = sys.argv[1] if len(sys.argv) > 1 else None
    rs = RuleSet()
    bot = Chatbot(rs)
    bot.run(dataset)
