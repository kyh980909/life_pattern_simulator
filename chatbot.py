import re
from typing import Tuple
from rule_set import RuleSet

class Chatbot:
    """Simple command-line chatbot for creating automation rules."""

    def __init__(self, rules: RuleSet):
        self.rules = rules

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

    def run(self) -> None:
        print("자동화 권고 챗봇 (종료하려면 'quit' 입력)")
        while True:
            user_input = input("사용자 입력> ").strip()
            if user_input.lower() in {"quit", "exit"}:
                break
            self.suggest_rule(user_input)

if __name__ == "__main__":
    rs = RuleSet()
    bot = Chatbot(rs)
    bot.run()
