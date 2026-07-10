import re
import sys
from pathlib import Path
from datetime import date
from calendar import monthrange

def calculate_age(birth_date):
    today = date.today()
    years = today.year - birth_date.year
    months = today.month - birth_date.month
    days = today.day - birth_date.day
    
    if days < 0:
        months -= 1

        prev_month = 12 if today.month == 1 else today.month - 1
        prev_year = today.year - 1 if today.month == 1 else today.year
        prev_month_days = monthrange(prev_year, prev_month)[1]
        days += prev_month_days
        
    if months < 0:
        years -= 1
        months += 12
        
    return f"{years} years, {months} months, {days} days"

def main():
    birth_date = date(2004, 1, 13)
    age_str = calculate_age(birth_date)
    
    RIGHT_WIDTH = 76
    bg = "".join(["." if i % 2 == 0 else " " for i in range(RIGHT_WIDTH)])
    prefix = ". Uptime: "
    suffix = f" {age_str}"
    
    chars = list(bg)
    for i, c in enumerate(prefix): 
        chars[i] = c
        
    start_suffix = RIGHT_WIDTH - len(suffix)
    for i, c in enumerate(suffix): 
        chars[start_suffix + i] = c
        
    new_line = "".join(chars)
    
    readme_path = Path(__file__).parent.parent / "README.md"

    content = readme_path.read_text(encoding="utf-8")

    updated, n = re.subn(r'^\.\sUptime:[^\n]*$', new_line, content, flags=re.MULTILINE)

    if n == 0:
        print("ERROR: Uptime line not found in README.md — no changes written.", file=sys.stderr)
        sys.exit(1)

    readme_path.write_text(updated, encoding="utf-8")
    print(f"Updated Uptime to: {age_str}")

if __name__ == "__main__":
    main()
