# gui.py
# run: python gui.py
# features: search, add/edit student, dashboard, pdf export

import json
import os
from datetime import date

import customtkinter as ctk
from tkinter import messagebox
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from students import students
from report import make_report, save_report

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


# ── PDF export function ──────────────────────────────────────

def export_pdf(student):
    os.makedirs("reports", exist_ok=True)
    fname = student["name"].replace(" ", "_") + "_report.pdf"
    path = os.path.join("reports", fname)

    doc = SimpleDocTemplate(path, pagesize=A4,
                            rightMargin=40, leftMargin=40,
                            topMargin=40, bottomMargin=40)

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle("title",
        fontSize=18, fontName="Helvetica-Bold",
        textColor=colors.HexColor("#1db954"),
        spaceAfter=4)

    heading_style = ParagraphStyle("heading",
        fontSize=11, fontName="Helvetica-Bold",
        textColor=colors.HexColor("#bbbbbb"),
        spaceBefore=14, spaceAfter=4)

    body_style = ParagraphStyle("body",
        fontSize=10, fontName="Helvetica",
        textColor=colors.HexColor("#dddddd"),
        spaceAfter=3, leading=16)

    meta_style = ParagraphStyle("meta",
        fontSize=9, fontName="Helvetica",
        textColor=colors.HexColor("#888888"),
        spaceAfter=2)

    total = len(student["done"]) + len(student["pending"])
    percent = int((len(student["done"]) / total) * 100) if total else 0

    story = []

    # header
    story.append(Paragraph("OJHA TECHNOLOGY", ParagraphStyle(
        "brand", fontSize=9, fontName="Helvetica",
        textColor=colors.HexColor("#1db954"), spaceAfter=2)))
    story.append(Paragraph("AI Lab — Student Report", title_style))
    story.append(Spacer(1, 6))

    # student meta info table
    meta_data = [
        ["Name", student["name"]],
        ["Class", student["class"]],
        ["School", student["school"]],
        ["Month", student["month"]],
        ["Date", date.today().strftime("%d %B %Y")],
        ["Progress", f"{percent}%"],
    ]
    meta_table = Table(meta_data, colWidths=[1.2*inch, 4.5*inch])
    meta_table.setStyle(TableStyle([
        ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME", (1,0), (1,-1), "Helvetica"),
        ("FONTSIZE", (0,0), (-1,-1), 10),
        ("TEXTCOLOR", (0,0), (0,-1), colors.HexColor("#888888")),
        ("TEXTCOLOR", (1,0), (1,-1), colors.HexColor("#dddddd")),
        ("ROWBACKGROUNDS", (0,0), (-1,-1),
         [colors.HexColor("#1a1a1a"), colors.HexColor("#222222")]),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 12))

    # skills learned
    story.append(Paragraph("SKILLS LEARNED", heading_style))
    for skill in student["done"]:
        story.append(Paragraph(f"✓  {skill}", body_style))

    # in progress
    if student["pending"]:
        story.append(Paragraph("IN PROGRESS", heading_style))
        for skill in student["pending"]:
            story.append(Paragraph(f"◷  {skill}", body_style))

    # projects
    story.append(Paragraph("PROJECTS COMPLETED", heading_style))
    for p in student["projects"]:
        story.append(Paragraph(f"★  {p}", body_style))

    # teacher note
    story.append(Paragraph("TEACHER'S NOTE", heading_style))
    story.append(Paragraph(student["strength"], body_style))

    # goals
    story.append(Paragraph("NEXT MONTH GOALS", heading_style))
    for g in student["next_goals"]:
        story.append(Paragraph(f"→  {g}", body_style))

    # footer
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "Ojha Technology Pvt. Ltd — AI Lab Program",
        ParagraphStyle("footer", fontSize=8, fontName="Helvetica",
                       textColor=colors.HexColor("#555555"))))

    doc.build(story)
    return path


# ── Add / Edit student form ──────────────────────────────────

class StudentForm(ctk.CTkToplevel):
    def __init__(self, parent, on_save, student=None):
        super().__init__(parent)
        self.on_save = on_save
        self.student = student
        self.title("Edit Student" if student else "Add New Student")
        self.geometry("520x680")
        self.resizable(False, False)
        self.grab_set()   # modal — baaki window block ho
        self._build()

    def _build(self):
        s = self.student or {}

        ctk.CTkLabel(self, text="Edit Student" if self.student else "Add Student",
                     font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 16))

        scroll = ctk.CTkScrollableFrame(self)
        scroll.pack(fill="both", expand=True, padx=20)

        def field(label, default=""):
            ctk.CTkLabel(scroll, text=label,
                         font=ctk.CTkFont(size=12),
                         text_color="gray").pack(anchor="w", pady=(8, 2))
            e = ctk.CTkEntry(scroll, width=440)
            e.insert(0, default)
            e.pack(anchor="w")
            return e

        def multifield(label, items):
            ctk.CTkLabel(scroll, text=label,
                         font=ctk.CTkFont(size=12),
                         text_color="gray").pack(anchor="w", pady=(8, 2))
            ctk.CTkLabel(scroll, text="(comma se alag karo)",
                         font=ctk.CTkFont(size=10),
                         text_color="#555555").pack(anchor="w")
            e = ctk.CTkEntry(scroll, width=440)
            e.insert(0, ", ".join(items))
            e.pack(anchor="w")
            return e

        self.f_name     = field("Name", s.get("name", ""))
        self.f_class    = field("Class", s.get("class", ""))
        self.f_school   = field("School", s.get("school", ""))
        self.f_month    = field("Month", s.get("month", date.today().strftime("%B %Y")))
        self.f_done     = multifield("Skills Learned", s.get("done", []))
        self.f_pending  = multifield("In Progress", s.get("pending", []))
        self.f_projects = multifield("Projects Completed", s.get("projects", []))
        self.f_strength = field("Teacher's Note", s.get("strength", ""))
        self.f_goals    = multifield("Next Month Goals", s.get("next_goals", []))

        ctk.CTkButton(self, text="Save Student",
                      command=self._save).pack(pady=16)

    def _save(self):
        def split(text):
            return [x.strip() for x in text.split(",") if x.strip()]

        new_student = {
            "name":       self.f_name.get().strip(),
            "class":      self.f_class.get().strip(),
            "school":     self.f_school.get().strip(),
            "month":      self.f_month.get().strip(),
            "done":       split(self.f_done.get()),
            "pending":    split(self.f_pending.get()),
            "projects":   split(self.f_projects.get()),
            "strength":   self.f_strength.get().strip(),
            "next_goals": split(self.f_goals.get()),
        }

        if not new_student["name"]:
            messagebox.showerror("Error", "Name khali nahi hona chahiye!")
            return

        self.on_save(new_student, self.student)
        self.destroy()


# ── Dashboard window ─────────────────────────────────────────

class Dashboard(ctk.CTkToplevel):
    def __init__(self, parent, student_list):
        super().__init__(parent)
        self.title("Dashboard — All Students Overview")
        self.geometry("700x500")
        self.resizable(False, False)
        self.grab_set()
        self._build(student_list)

    def _build(self, student_list):
        ctk.CTkLabel(self, text="All Students Overview",
                     font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 4))
        ctk.CTkLabel(self, text=f"Total students: {len(student_list)}",
                     font=ctk.CTkFont(size=12),
                     text_color="gray").pack(pady=(0, 16))

        scroll = ctk.CTkScrollableFrame(self)
        scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        for s in student_list:
            total = len(s["done"]) + len(s["pending"])
            percent = int((len(s["done"]) / total) * 100) if total else 0

            # card frame
            card = ctk.CTkFrame(scroll)
            card.pack(fill="x", pady=6)

            top = ctk.CTkFrame(card, fg_color="transparent")
            top.pack(fill="x", padx=14, pady=(10, 4))

            ctk.CTkLabel(top, text=s["name"],
                         font=ctk.CTkFont(size=13, weight="bold")).pack(side="left")
            ctk.CTkLabel(top, text=f"{percent}%",
                         font=ctk.CTkFont(size=13),
                         text_color="#1db954").pack(side="right")

            ctk.CTkLabel(card,
                         text=f"Class {s['class']}  •  {s['school']}",
                         font=ctk.CTkFont(size=11),
                         text_color="gray").pack(anchor="w", padx=14)

            bar = ctk.CTkProgressBar(card)
            bar.pack(fill="x", padx=14, pady=(6, 12))
            bar.set(percent / 100)

            # quick stats
            stats = ctk.CTkFrame(card, fg_color="transparent")
            stats.pack(fill="x", padx=14, pady=(0, 10))

            def stat_chip(parent, label, val):
                f = ctk.CTkFrame(parent, fg_color=("gray85", "gray20"),
                                 corner_radius=6)
                f.pack(side="left", padx=(0, 8))
                ctk.CTkLabel(f, text=f"{val} {label}",
                             font=ctk.CTkFont(size=11),
                             text_color="gray").pack(padx=8, pady=4)

            stat_chip(stats, "skills done", len(s["done"]))
            stat_chip(stats, "in progress", len(s["pending"]))
            stat_chip(stats, "projects", len(s["projects"]))


# ── Main App ─────────────────────────────────────────────────

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Ojha Technology — AI Lab Report Generator")
        self.geometry("940x640")
        self.resizable(False, False)

        # local copy — taaki add/edit kaam kare
        self.student_list = list(students)
        self.current_student = None

        self._build_ui()
        if self.student_list:
            self.show_report(self.student_list[0])

    def _build_ui(self):

        # ── left panel ──
        self.left = ctk.CTkFrame(self, width=230, corner_radius=0)
        self.left.pack(side="left", fill="y")
        self.left.pack_propagate(False)

        # brand label
        ctk.CTkLabel(self.left,
                     text="Ojha Technology",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#1db954").pack(pady=(18, 2), padx=16, anchor="w")
        ctk.CTkLabel(self.left,
                     text="AI Lab Reports",
                     font=ctk.CTkFont(size=11),
                     text_color="gray").pack(padx=16, anchor="w")

        # search
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", self._filter)

        ctk.CTkEntry(self.left,
                     placeholder_text="Search student...",
                     textvariable=self.search_var
                     ).pack(fill="x", padx=10, pady=(14, 6))

        # student buttons scrollable area
        self.btn_frame = ctk.CTkScrollableFrame(self.left, fg_color="transparent")
        self.btn_frame.pack(fill="both", expand=True)

        # add student button neeche
        ctk.CTkButton(self.left,
                      text="+ Add Student",
                      fg_color="transparent",
                      border_width=1,
                      command=self._add_student
                      ).pack(fill="x", padx=10, pady=(6, 6))

        # dashboard button
        ctk.CTkButton(self.left,
                      text="Dashboard",
                      fg_color="transparent",
                      border_width=1,
                      command=self._open_dashboard
                      ).pack(fill="x", padx=10, pady=(0, 16))

        # ── right panel ──
        right = ctk.CTkFrame(self, fg_color="transparent")
        right.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # top info
        top_row = ctk.CTkFrame(right, fg_color="transparent")
        top_row.pack(fill="x")

        info = ctk.CTkFrame(top_row, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True)

        self.name_label = ctk.CTkLabel(info, text="",
                                        font=ctk.CTkFont(size=20, weight="bold"))
        self.name_label.pack(anchor="w")

        self.meta_label = ctk.CTkLabel(info, text="",
                                        font=ctk.CTkFont(size=12),
                                        text_color="gray")
        self.meta_label.pack(anchor="w")

        # edit button top right
        self.edit_btn = ctk.CTkButton(top_row, text="Edit",
                                       width=70,
                                       fg_color="transparent",
                                       border_width=1,
                                       command=self._edit_student)
        self.edit_btn.pack(side="right", anchor="n")

        # progress bar
        self.progress = ctk.CTkProgressBar(right)
        self.progress.pack(fill="x", pady=(12, 2))
        self.progress.set(0)

        self.percent_label = ctk.CTkLabel(right, text="",
                                           font=ctk.CTkFont(size=11),
                                           text_color="gray")
        self.percent_label.pack(anchor="w", pady=(0, 10))

        # report textbox
        self.textbox = ctk.CTkTextbox(right,
                                       font=ctk.CTkFont(family="Courier", size=13),
                                       wrap="none")
        self.textbox.pack(fill="both", expand=True)

        # bottom buttons
        btn_row = ctk.CTkFrame(right, fg_color="transparent")
        btn_row.pack(fill="x", pady=(12, 0))

        self.save_txt_btn = ctk.CTkButton(btn_row,
                                           text="Save as .txt",
                                           fg_color="transparent",
                                           border_width=1,
                                           command=self._save_txt)
        self.save_txt_btn.pack(side="left", padx=(0, 8))

        self.save_pdf_btn = ctk.CTkButton(btn_row,
                                           text="Export PDF",
                                           command=self._save_pdf)
        self.save_pdf_btn.pack(side="left")

        # render student list
        self._render_buttons(self.student_list)

    # ── student list rendering ──

    def _render_buttons(self, lst):
        for w in self.btn_frame.winfo_children():
            w.destroy()

        if not lst:
            ctk.CTkLabel(self.btn_frame,
                         text="Koi student nahi mila",
                         text_color="gray",
                         font=ctk.CTkFont(size=12)).pack(pady=20)
            return

        for s in lst:
            btn = ctk.CTkButton(
                self.btn_frame,
                text=s["name"],
                anchor="w",
                fg_color="transparent",
                hover_color=("gray75", "gray25"),
                command=lambda x=s: self.show_report(x)
            )
            btn.pack(fill="x", padx=10, pady=3)

    def _filter(self, *args):
        q = self.search_var.get().lower().strip()
        if not q:
            self._render_buttons(self.student_list)
            return
        filtered = [s for s in self.student_list
                    if q in s["name"].lower() or q in s["school"].lower()]
        self._render_buttons(filtered)

    # ── show report ──

    def show_report(self, student):
        self.current_student = student

        self.name_label.configure(text=student["name"])
        self.meta_label.configure(
            text=f"Class {student['class']}  •  {student['school']}  •  {student['month']}"
        )

        total = len(student["done"]) + len(student["pending"])
        percent = int((len(student["done"]) / total) * 100) if total else 0
        self.progress.set(percent / 100)
        self.percent_label.configure(text=f"Progress: {percent}%")

        report_text = make_report(student)
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", report_text)
        self.textbox.configure(state="disabled")

    # ── add / edit ──

    def _add_student(self):
        StudentForm(self, on_save=self._on_student_saved)

    def _edit_student(self):
        if not self.current_student:
            return
        StudentForm(self, on_save=self._on_student_saved,
                    student=self.current_student)

    def _on_student_saved(self, new_data, old_data):
        if old_data:
            # edit — purana replace karo
            idx = next((i for i, s in enumerate(self.student_list)
                        if s["name"] == old_data["name"]), None)
            if idx is not None:
                self.student_list[idx] = new_data
        else:
            # naya student add karo
            self.student_list.append(new_data)

        self._render_buttons(self.student_list)
        self.show_report(new_data)

    # ── dashboard ──

    def _open_dashboard(self):
        Dashboard(self, self.student_list)

    # ── save buttons ──

    def _save_txt(self):
        if not self.current_student:
            return
        path = save_report(self.current_student, make_report(self.current_student))
        self.save_txt_btn.configure(text=f"Saved!")
        self.after(2500, lambda: self.save_txt_btn.configure(text="Save as .txt"))

    def _save_pdf(self):
        if not self.current_student:
            return
        try:
            path = export_pdf(self.current_student)
            self.save_pdf_btn.configure(text="PDF Saved!")
            self.after(2500, lambda: self.save_pdf_btn.configure(text="Export PDF"))
        except Exception as e:
            messagebox.showerror("PDF Error", str(e))


if __name__ == "__main__":
    app = App()
    app.mainloop()

    