import tkinter as tk
from rule_set import RuleSet

class ChatbotUI:
    """Simple Tkinter chatbot interface for rule confirmations."""

    def __init__(self, master: tk.Tk, rule_set: RuleSet, on_rule_added=None):
        self.master = master
        self.master.title("Home Control Chatbot")
        self.rule_set = rule_set
        self.on_rule_added = on_rule_added

        self.text_area = tk.Text(self.master, state="disabled", width=40, height=15)
        self.text_area.pack(padx=10, pady=10)

        self.entry = tk.Entry(self.master)
        self.entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.entry.bind("<Return>", self.on_enter)

        self.pending_rule = None

    def display(self, text: str, sender: str = "bot") -> None:
        prefix = "Bot: " if sender == "bot" else "You: "
        self.text_area.config(state="normal")
        self.text_area.insert(tk.END, prefix + text + "\n")
        self.text_area.see(tk.END)
        self.text_area.config(state="disabled")

    def ask_yes_no(self, message: str, rule: dict) -> None:
        self.pending_rule = rule
        self.display(message)

    def on_enter(self, event=None) -> None:
        user_text = self.entry.get().strip()
        if not user_text:
            return
        self.entry.delete(0, tk.END)
        self.display(user_text, sender="user")

        if self.pending_rule:
            if user_text.lower() == "yes":
                self.rule_set.add_rule(self.pending_rule)
                self.display("규칙이 저장되었습니다.")
                if self.on_rule_added:
                    self.on_rule_added()
            else:
                self.display("규칙이 저장되지 않았습니다.")
            self.pending_rule = None

