import re
from rule_set import RuleSet

class Chatbot:
    """Very simple command-line chatbot for rule suggestions."""

    def __init__(self, rules: RuleSet):
        self.rules = rules

    def suggest_rule(self, text: str) -> None:
        text_lower = text.lower()
        if "조명" in text_lower and "off" in text_lower:
            print("매일 22:00에 조명을 끌까요? (Yes/No)")
            ans = input().strip().lower()
            if ans == "yes":
                rule = {"device": "거실", "action": "OFF", "time": "22:00"}
                self.rules.add_rule(rule)
                print("규칙이 저장되었습니다.")
        else:
            print("현재는 추천할 규칙이 없습니다.")

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
