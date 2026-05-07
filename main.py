# main.py
# bas terminal mein:  python main.py

from students import students
from report import make_report, save_report


def main():
    print("\n=== Kamrta Robotics — Report Generator ===")
    print(f"Total students: {len(students)}\n")

    for s in students:
        report = make_report(s)

        # screen pe dikhao
        print(report)
        print()

        # file mein save karo
        path = save_report(s, report)
        print(f"  saved → {path}\n")

    print("Done! Check the reports/ folder.")


if __name__ == "__main__":
    main()