# 📊 AI Lab Student Report Generator

A desktop application built with Python to generate professional progress reports for students learning AI and coding in school labs.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-green?style=flat-square)
![ReportLab](https://img.shields.io/badge/PDF-ReportLab-red?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 🎯 About The Project

Managing student progress in AI labs is time-consuming for teachers. This tool lets instructors generate clean, professional reports in seconds — saving hours of manual work and giving parents and school principals clear visibility into what students are learning.

Built specifically for EdTech and robotics lab environments where teachers need to track skills, projects, and goals for multiple students at once.

---

## ✨ Features

- **Student Dashboard** — overview of all students with progress bars at a glance
- **Progress Reports** — detailed per-student reports with skills learned, projects completed, and next goals
- **Add / Edit Students** — manage student data directly from the GUI, no need to touch code
- **Search Bar** — instantly filter students by name or school
- **Export as PDF** — generate clean, branded PDF reports to share with parents or principals
- **Save as TXT** — plain text version for quick reference
- **Dark Mode UI** — modern dark theme built with CustomTkinter

---

## 🖥️ Screenshots

> Run the app and explore — the interface is self-explanatory.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or above
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/ai-lab-report-generator.git
cd ai-lab-report-generator

# 2. Install dependencies
pip install customtkinter reportlab

# 3. Run the app
python gui.py
```

---

## 📁 Project Structure

```
ai-lab-report-generator/
│
├── gui.py          # Main application — run this
├── report.py       # Report generation logic
├── students.py     # Student data
├── reports/        # Generated reports saved here (auto-created)
└── README.md
```

---

## 🛠️ Built With

| Tool | Purpose |
|---|---|
| Python | Core language |
| CustomTkinter | Modern dark-mode GUI |
| ReportLab | PDF generation |
| Tkinter | Base GUI framework |

---

## 📖 How To Use

1. **Run** `python gui.py`
2. **Select** a student from the left panel
3. **View** their full progress report on the right
4. **Export** as PDF or save as TXT using the buttons at the bottom
5. **Add** new students using the `+ Add Student` button
6. **Edit** existing student data using the `Edit` button
7. **Dashboard** gives a quick overview of all students at once

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

This project is licensed under the MIT License — feel free to use and modify.

---

## 👨‍💻 Author


**Abhinav Ojha** — [github.com/Abhinavojha0145](https://github.com/Abhinavojha0145)
Built with purpose — to make AI education more transparent and trackable for students, teachers, and parents.

