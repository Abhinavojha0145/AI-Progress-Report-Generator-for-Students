# report.py

import os
from datetime import date


def progress_bar(done, pending):
    total = len(done) + len(pending)
    if total == 0:
        return "░░░░░░░░░░", 0
    percent = int((len(done) / total) * 100)
    filled = int(percent / 10)
    bar = "█" * filled + "░" * (10 - filled)
    return bar, percent


def make_report(s):
    # s = student dictionary
    bar, percent = progress_bar(s["done"], s["pending"])

    # message based on progress
    if percent >= 80:
        msg = "Excellent progress! Keep it up."
    elif percent >= 50:
        msg = "Good effort. Almost there!"
    else:
        msg = "More practice needed. You can do it!"

    lines = []
    lines.append("╔══════════════════════════════════════╗")
    lines.append("║        OJHA TECHNOLOGY               ║")
    lines.append("║       AI LAB — STUDENT REPORT        ║")
    lines.append("╚══════════════════════════════════════╝")
    lines.append("")
    lines.append(f"Name   : {s['name']}")
    lines.append(f"Class  : {s['class']}")
    lines.append(f"School : {s['school']}")
    lines.append(f"Month  : {s['month']}")
    lines.append(f"Date   : {date.today().strftime('%d %B %Y')}")
    lines.append("")

    lines.append("SKILLS LEARNED")
    lines.append("──────────────")
    for skill in s["done"]:
        lines.append(f"  ✅ {skill}")

    if s["pending"]:
        lines.append("")
        lines.append("IN PROGRESS")
        lines.append("───────────")
        for skill in s["pending"]:
            lines.append(f"  🔄 {skill}")

    lines.append("")
    lines.append("PROJECTS COMPLETED")
    lines.append("──────────────────")
    for p in s["projects"]:
        lines.append(f"  ⭐ {p}")

    lines.append("")
    lines.append("TEACHER'S NOTE")
    lines.append("──────────────")
    lines.append(f"  {s['strength']}")

    lines.append("")
    lines.append("NEXT MONTH GOALS")
    lines.append("────────────────")
    for g in s["next_goals"]:
        lines.append(f"  → {g}")

    lines.append("")
    lines.append(f"PROGRESS : {bar} {percent}%")
    lines.append(f"           {msg}")
    lines.append("")
    lines.append("══════════════════════════════════════")
    lines.append("       Ojha Technology Pvt. Ltd")
    lines.append("══════════════════════════════════════")

    return "\n".join(lines)


def save_report(student, text):
    os.makedirs("reports", exist_ok=True)
    fname = student["name"].replace(" ", "_") + "_report.txt"
    path = os.path.join("reports", fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path