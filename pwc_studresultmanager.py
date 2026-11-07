
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from datetime import datetime

# ==========================================
# PWC-A STUDENTHUB
# Academic Performance Management System
# ==========================================

students = []

BG = "#101827"
PANEL = "#1c293b"
ACCENT = "#13b8a6"
WHITE = "#f1f5f9"
MUTED = "#94a3b8"


def get_grade(marks):
    if marks >= 90:
        return "A+"
    elif marks >= 80:
        return "A"
    elif marks >= 70:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 50:
        return "D"
    return "F"


def get_result(marks):
    return "PASS" if marks >= 40 else "FAIL"


class StudentHub:

    def __init__(self, root):
        self.root = root
        self.root.title("PWC-A | StudentHub")
        self.root.geometry("1150x700")
        self.root.configure(bg=BG)
        self.selected_id = None

        self.create_interface()
        self.refresh()

    # MAIN INTERFACE

    def create_interface(self):

        header = tk.Frame(self.root, bg=PANEL, height=85)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="PWC-A STUDENTHUB",
            font=("Arial", 22, "bold"),
            bg=PANEL,
            fg=ACCENT
        ).pack(anchor="w", padx=25, pady=(15, 0))

        tk.Label(
            header,
            text="Academic Performance Management System",
            font=("Arial", 10),
            bg=PANEL,
            fg=MUTED
        ).pack(anchor="w", padx=27)

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=20, pady=20)

        self.create_form(body)
        self.create_records(body)

        self.status = tk.Label(
            self.root,
            text="System Ready",
            bg=PANEL,
            fg=MUTED,
            anchor="w",
            padx=15
        )
        self.status.pack(fill="x", side="bottom")

    # STUDENT REGISTRATION

    def create_form(self, parent):

        form = tk.Frame(parent, bg=PANEL, width=280)
        form.pack(side="left", fill="y", padx=(0, 15))
        form.pack_propagate(False)

        tk.Label(
            form,
            text="Student Registration",
            font=("Arial", 15, "bold"),
            bg=PANEL,
            fg=WHITE
        ).pack(anchor="w", padx=18, pady=20)

        self.entries = {}

        fields = [
            ("Student ID", "id"),
            ("Student Name", "name"),
            ("Subject", "subject"),
            ("Marks (0-100)", "marks")
        ]

        for label, key in fields:

            tk.Label(
                form,
                text=label,
                bg=PANEL,
                fg=MUTED,
                font=("Arial", 10)
            ).pack(anchor="w", padx=18)

            entry = tk.Entry(
                form,
                font=("Arial", 11),
                bg="#26364b",
                fg=WHITE,
                insertbackground=WHITE,
                relief="flat"
            )

            entry.pack(fill="x", padx=18, pady=(5, 15), ipady=7)

            self.entries[key] = entry

        self.button(form, "REGISTER STUDENT", self.add_student)
        self.button(form, "UPDATE RECORD", self.update_student)
        self.button(form, "REMOVE STUDENT", self.delete_student)
        self.button(form, "CLEAR FORM", self.clear_form)

    def button(self, parent, text, command):

        tk.Button(
            parent,
            text=text,
            command=command,
            bg=ACCENT,
            fg="#071c22",
            activebackground="#0e9488",
            font=("Arial", 9, "bold"),
            relief="flat",
            cursor="hand2"
        ).pack(fill="x", padx=18, pady=6, ipady=8)

    # STUDENT RECORDS

    def create_records(self, parent):

        area = tk.Frame(parent, bg=PANEL)
        area.pack(side="right", fill="both", expand=True)

        tk.Label(
            area,
            text="Student Records",
            font=("Arial", 17, "bold"),
            bg=PANEL,
            fg=WHITE
        ).pack(anchor="w", padx=20, pady=(20, 10))

        search_area = tk.Frame(area, bg=PANEL)
        search_area.pack(fill="x", padx=20, pady=10)

        tk.Label(
            search_area,
            text="Search:",
            bg=PANEL,
            fg=MUTED
        ).pack(side="left")

        self.search = tk.Entry(
            search_area,
            bg="#26364b",
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat"
        )

        self.search.pack(
            side="left",
            padx=10,
            ipady=6,
            fill="x",
            expand=True
        )

        self.search.bind(
            "<KeyRelease>",
            lambda e: self.refresh()
        )

        columns = (
            "id", "name", "subject",
            "marks", "grade", "result"
        )

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="#26364b",
            foreground=WHITE,
            fieldbackground="#26364b",
            rowheight=32,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#33465e",
            foreground=WHITE,
            font=("Arial", 10, "bold")
        )

        self.table = ttk.Treeview(
            area,
            columns=columns,
            show="headings"
        )

        headings = {
            "id": "Student ID",
            "name": "Name",
            "subject": "Subject",
            "marks": "Marks",
            "grade": "Grade",
            "result": "Result"
        }

        for col, heading in headings.items():
            self.table.heading(col, text=heading)
            self.table.column(
                col,
                anchor="center",
                width=105
            )

        self.table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.table.bind(
            "<<TreeviewSelect>>",
            self.select_student
        )

        self.statistics = tk.Label(
            area,
            text="",
            bg=PANEL,
            fg=ACCENT,
            font=("Arial", 10, "bold"),
            justify="left"
        )

        self.statistics.pack(
            anchor="w",
            padx=20,
            pady=15
        )

        actions = tk.Frame(area, bg=PANEL)
        actions.pack(fill="x", padx=15, pady=10)

        tk.Button(
            actions,
            text="EXPORT CSV",
            command=self.export_csv,
            bg="#33465e",
            fg=WHITE,
            relief="flat"
        ).pack(side="left", padx=5, ipadx=10, ipady=7)

        tk.Button(
            actions,
            text="IMPORT CSV",
            command=self.import_csv,
            bg="#33465e",
            fg=WHITE,
            relief="flat"
        ).pack(side="left", padx=5, ipadx=10, ipady=7)

        tk.Button(
            actions,
            text="STUDENT REPORT",
            command=self.student_report,
            bg=ACCENT,
            fg="#071c22",
            relief="flat"
        ).pack(side="right", padx=5, ipadx=10, ipady=7)

    # ADD STUDENT

    def add_student(self):

        data = self.read_form()

        if not data:
            return

        if any(s["id"] == data["id"] for s in students):
            messagebox.showerror(
                "Error",
                "Student ID already exists."
            )
            return

        students.append(data)
        self.refresh()
        self.clear_form()

        self.status.config(
            text="Student registered successfully."
        )

    # INPUT VALIDATION

    def read_form(self):

        values = {
            key: entry.get().strip()
            for key, entry in self.entries.items()
        }

        if not all(values.values()):
            messagebox.showwarning(
                "Missing Data",
                "Please fill all fields."
            )
            return None

        try:
            marks = float(values["marks"])

            if not 0 <= marks <= 100:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Marks",
                "Enter a valid number between 0 and 100."
            )
            return None

        return {
            "id": values["id"],
            "name": values["name"],
            "subject": values["subject"],
            "marks": marks,
            "grade": get_grade(marks),
            "result": get_result(marks)
        }

    # SELECT STUDENT

    def select_student(self, event):

        selected = self.table.selection()

        if not selected:
            return

        student_id = self.table.item(
            selected[0]
        )["values"][0]

        student = next(
            (s for s in students if s["id"] == student_id),
            None
        )

        if student:

            self.selected_id = student_id

            for key in self.entries:
                self.entries[key].delete(0, tk.END)
                self.entries[key].insert(0, student[key])

    # UPDATE STUDENT

    def update_student(self):

        if self.selected_id is None:
            messagebox.showwarning(
                "Select",
                "Select a student first."
            )
            return

        data = self.read_form()

        if not data:
            return

        if data["id"] != self.selected_id:
            messagebox.showerror(
                "Invalid ID",
                "Student ID cannot be changed during an update."
            )
            return

        for i, student in enumerate(students):

            if student["id"] == self.selected_id:
                students[i] = data
                break

        self.refresh()
        self.clear_form()

        self.status.config(
            text="Student record updated."
        )

    # DELETE STUDENT

    def delete_student(self):

        if self.selected_id is None:
            messagebox.showwarning(
                "Select",
                "Select a student first."
            )
            return

        confirm = messagebox.askyesno(
            "Confirmation",
            "Do you want to delete this student?"
        )

        if confirm:

            students[:] = [
                s for s in students
                if s["id"] != self.selected_id
            ]

            self.refresh()
            self.clear_form()

            self.status.config(
                text="Student deleted."
            )

    # CLEAR FORM

    def clear_form(self):

        for entry in self.entries.values():
            entry.delete(0, tk.END)

        self.selected_id = None
        self.table.selection_remove(
            self.table.selection()
        )

    # REFRESH TABLE AND STATISTICS

    def refresh(self):

        for item in self.table.get_children():
            self.table.delete(item)

        query = self.search.get().lower()

        for student in sorted(
            students,
            key=lambda s: s["marks"],
            reverse=True
        ):

            if (
                query in student["name"].lower()
                or query in student["id"].lower()
            ):

                self.table.insert(
                    "",
                    "end",
                    values=(
                        student["id"],
                        student["name"],
                        student["subject"],
                        student["marks"],
                        student["grade"],
                        student["result"]
                    )
                )

        self.update_statistics()

    def update_statistics(self):

        if not students:
            self.statistics.config(
                text="No student records available."
            )
            return

        total = len(students)

        average = sum(
            s["marks"] for s in students
        ) / total

        passed = sum(
            1 for s in students
            if s["result"] == "PASS"
        )

        topper = max(
            students,
            key=lambda s: s["marks"]
        )

        percentage = (passed / total) * 100

        self.statistics.config(
            text=(
                f"TOTAL: {total}     "
                f"AVERAGE: {average:.2f}     "
                f"PASS: {passed}     "
                f"PASS RATE: {percentage:.1f}%\n"
                f"CLASS TOPPER: {topper['name']} "
                f"({topper['marks']} marks)"
            )
        )

    # CSV EXPORT

    def export_csv(self):

        if not students:
            messagebox.showinfo(
                "Empty",
                "No records to export."
            )
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
        )

        if not path:
            return

        try:
            with open(
                path,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.DictWriter(
                    file,
                    fieldnames=[
                        "id", "name", "subject",
                        "marks", "grade", "result"
                    ]
                )

                writer.writeheader()
                writer.writerows(students)

            messagebox.showinfo(
                "Success",
                "Records exported successfully."
            )

        except (OSError, csv.Error) as error:
            messagebox.showerror(
                "Export Error",
                str(error)
            )

    # CSV IMPORT

    def import_csv(self):

        path = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv")]
        )

        if not path:
            return

        try:
            with open(
                path,
                "r",
                newline="",
                encoding="utf-8-sig"
            ) as file:

                reader = csv.DictReader(file)

                required = {
                    "id", "name", "subject",
                    "marks", "grade", "result"
                }

                if not required.issubset(
                    reader.fieldnames or []
                ):
                    raise ValueError(
                        "Invalid CSV format."
                    )

                existing_ids = {
                    s["id"] for s in students
                }

                imported = []

                for row in reader:

                    student_id = (
                        row.get("id") or ""
                    ).strip()

                    name = (
                        row.get("name") or ""
                    ).strip()

                    subject = (
                        row.get("subject") or ""
                    ).strip()

                    if not student_id or not name or not subject:
                        raise ValueError(
                            "Missing student details in CSV."
                        )

                    if student_id in existing_ids:
                        continue

                    marks = float(row["marks"])

                    if not 0 <= marks <= 100:
                        raise ValueError(
                            "Invalid marks in CSV."
                        )

                    imported.append({
                        "id": student_id,
                        "name": name,
                        "subject": subject,
                        "marks": marks,
                        "grade": get_grade(marks),
                        "result": get_result(marks)
                    })

                    existing_ids.add(student_id)

            students.extend(imported)
            self.refresh()

            self.status.config(
                text=(
                    f"{len(imported)} "
                    "student record(s) imported."
                )
            )

            messagebox.showinfo(
                "Import Complete",
                f"{len(imported)} records imported successfully."
            )

        except (ValueError, OSError, csv.Error) as error:
            messagebox.showerror(
                "Import Error",
                str(error)
            )

    # INDIVIDUAL STUDENT REPORT

    def student_report(self):

        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "Select Student",
                "Select a student record first."
            )
            return

        student_id = self.table.item(
            selected[0]
        )["values"][0]

        student = next(
            (s for s in students if s["id"] == student_id),
            None
        )

        if not student:
            return

        report = f"""
PWC-A STUDENTHUB
STUDENT PERFORMANCE REPORT
----------------------------------

Student ID : {student['id']}
Name       : {student['name']}
Subject    : {student['subject']}

Marks      : {student['marks']}
Grade      : {student['grade']}
Result     : {student['result']}

----------------------------------
Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}
"""

        report_window = tk.Toplevel(self.root)
        report_window.title("Student Report")
        report_window.geometry("450x400")
        report_window.configure(bg=BG)

        tk.Label(
            report_window,
            text=report,
            bg=BG,
            fg=WHITE,
            font=("Consolas", 11),
            justify="left"
        ).pack(
            anchor="w",
            padx=25,
            pady=25
        )

        def save_report():

            path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt")]
            )

            if path:
                try:
                    with open(
                        path,
                        "w",
                        encoding="utf-8"
                    ) as file:
                        file.write(report)

                    messagebox.showinfo(
                        "Saved",
                        "Student report saved successfully."
                    )

                except OSError as error:
                    messagebox.showerror(
                        "Save Error",
                        str(error)
                    )

        tk.Button(
            report_window,
            text="SAVE REPORT",
            command=save_report,
            bg=ACCENT,
            fg="#071c22",
            relief="flat",
            font=("Arial", 10, "bold")
        ).pack(pady=10)


# RUN APPLICATION

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentHub(root)
    root.mainloop()
