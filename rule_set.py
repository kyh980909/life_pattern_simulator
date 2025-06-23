import json
from typing import List, Dict

class RuleSet:
    """Simple rule-set manager for automation rules."""

    def __init__(self, path: str = "rules.json"):
        self.path = path
        self.rules: List[Dict] = []
        self.load()

    def load(self) -> None:
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                self.rules = json.load(f)
        except FileNotFoundError:
            self.rules = []

    def save(self) -> None:
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(self.rules, f, ensure_ascii=False, indent=2)

    def add_rule(self, rule: Dict) -> None:
        """Add a new rule and persist it."""
        self.rules.append(rule)
        self.save()

    def get_rules(self) -> List[Dict]:
        return list(self.rules)
