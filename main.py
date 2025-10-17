# password_checker.py
import string
import re
from pathlib import Path

COMMON_FILE = Path("common.txt")

def load_common_passwords(path=COMMON_FILE):
    if not path.exists():
        return set()
    return set(line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip())

def character_class_score(password: str):
    """Return (class_count, class_flags) where class_count in 0..4"""
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)
    flags = {
        "upper": has_upper,
        "lower": has_lower,
        "digit": has_digit,
        "symbol": has_symbol
    }
    count = sum(flags.values())
    return count, flags

def length_bonus(password: str):
    """Return extra points based on length"""
    score = 0
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if len(password) >= 16:
        score += 1
    if len(password) >= 20:
        score += 1
    return score

def check_password_strength(password: str) -> int:
    """
    Combined scoring:
      - 0..4 points for presence of character classes (upper/lower/digit/symbol)
      - +0..4 points for length thresholds (8,12,16,20)
    Returns total score (0..8).
    """
    class_count, _ = character_class_score(password)
    if class_count < 4:
        # If not all classes present, still allow class_count to contribute,
        # but do not give length bonus until classes are complete (consistent with earlier logic).
        return class_count
    # If all classes present, add length bonuses
    total = class_count + length_bonus(password)
    return total

def friendly_strength_message(score: int, class_flags=None, length=None):
    """Map numeric score to friendly messages"""
    # Score mapping based on possible range 0..8
    if score == 0:
        return "🔴 Too weak"
    if 1 <= score <= 2:
        return "🔴 Weak"
    if score == 3:
        return "🟡 Average"
    if score == 4:
        return "🟡 Not that strong"
    if 5 <= score <= 6:
        return "✅ Strong"
    if score >= 7:
        return "🏆 Extremely strong"
    return "Unknown"

def check_password(password: str, common_passwords=None):
    if common_passwords is None:
        common_passwords = load_common_passwords()

    if password in common_passwords:
        print("❗ Password is too common. Strength: 0")
        return 0

    class_count, flags = character_class_score(password)
    score = check_password_strength(password)

    # Provide action-oriented suggestions if missing classes
    if class_count < 4:
        missing = [k for k, present in flags.items() if not present]
        print(f"Password strength score: {score} — missing: {', '.join(missing)}")
        print("Tip: include at least one uppercase, one lowercase, one digit, and one special character.")
        return score

    # If all classes present, show length and final rating
    print(f"Password strength score: {score} (classes=4, length={len(password)})")
    print(f"Rating: {friendly_strength_message(score)}")
    if score < 5:
        print("Tip: make the password longer (>=12 chars) to increase strength.")
    return score

def interactive_loop():
    common_pw = load_common_passwords()
    try:
        while True:
            pwd = input("Enter password (or type 'exit' to quit): ").strip()
            if pwd.lower() in ("exit", "quit"):
                break
            check_password(pwd, common_passwords=common_pw)
            print("-" * 40)
    except KeyboardInterrupt:
        print("\nExiting.")

if __name__ == "__main__":
    interactive_loop()

   
   
