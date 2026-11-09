

import csv
import os

# Project Settings
SUBJECTS = ["English", "Math", "Science", "ICT", "Bangla"]
CSV_FILE = "students.csv"


# =====================================
# 1. STUDENT CLASS
# =====================================

class Student:

    def __init__(self, name, student_id, marks):
        self.name = name
        self.student_id = student_id
        self.marks = marks

    def calculate_total(self):
        return sum(self.marks.values())

    def calculate_average(self):
        return self.calculate_total() / len(SUBJECTS)

    def calculate_percentage(self):
        return (self.calculate_total() / 500) * 100

    def calculate_grade(self):
        average = self.calculate_average()

        if average >= 80:
            return "A+"
        elif average >= 70:
            return "A"
        elif average >= 60:
            return "A-"
        elif average >= 50:
            return "B"
        elif average >= 40:
            return "C"
        else:
            return "F"

    def get_status(self):
        for mark in self.marks.values():
            if mark < 33:
                return "FAIL"

        return "PASS"

    def display_result(self):
        print("\n========== STUDENT RESULT ==========")
        print("Name:", self.name)
        print("Student ID:", self.student_id)

        for subject, mark in self.marks.items():
            print(subject, ":", mark)

        print("------------------------------------")
        print("Total Marks:", self.calculate_total(), "/ 500")
        print("Average:", round(self.calculate_average(), 2))
        print("Percentage:", round(self.calculate_percentage(), 2), "%")
        print("Grade:", self.calculate_grade())
        print("Status:", self.get_status())
        print("====================================")


# =====================================
# 2. RESULT MANAGER CLASS
# =====================================

class ResultManager:

    def __init__(self):
        self.students = []
        self.load_data()

    # Save student information in CSV
    def save_data(self):

        try:
            with open(CSV_FILE, "w", newline="") as file:

                csv_writer = csv.writer(file)

                csv_writer.writerow(
                    ["Student ID", "Name"] + SUBJECTS
                )

                for student in self.students:

                    row = [
                        student.student_id,
                        student.name
                    ]

                    for subject in SUBJECTS:
                        row.append(student.marks[subject])

                    csv_writer.writerow(row)

            print("Student data saved successfully!")

        except OSError as error:
            print("Error saving data:", error)

    # Load student information from CSV
    def load_data(self):

        if not os.path.exists(CSV_FILE):
            return

        try:
            with open(CSV_FILE, "r", newline="") as file:

                reader = csv.DictReader(file)

                for row in reader:

                    marks = {}

                    for subject in SUBJECTS:
                        mark = int(row[subject])

                        if not 0 <= mark <= 100:
                            raise ValueError("Invalid marks in CSV.")

                        marks[subject] = mark

                    student = Student(
                        row["Name"],
                        row["Student ID"],
                        marks
                    )

                    self.students.append(student)

            print("Previous student data loaded successfully!")

        except (ValueError, KeyError, TypeError, csv.Error) as error:
            self.students = []
            print("Error loading CSV data:", error)

        except OSError as error:
            print("Error opening CSV file:", error)

    # Search student by ID
    def search_student(self, student_id, show_message=True):

        for student in self.students:

            if student.student_id == student_id:

                if show_message:
                    student.display_result()

                return student

        if show_message:
            print("Student not found!")

        return None

    # Add new student
    def add_student(self):

        print("\n========== ADD NEW STUDENT ==========")

        name = input("Enter student name: ").strip()
        student_id = input("Enter student ID: ").strip()

        if not name or not student_id:
            print("Name and ID cannot be empty!")
            return

        if self.search_student(student_id, False):
            print("This Student ID already exists!")
            return

        marks = {}

        for subject in SUBJECTS:

            while True:

                try:
                    mark = int(input(f"Enter {subject} marks (0-100): "))

                    if 0 <= mark <= 100:
                        marks[subject] = mark
                        break

                    else:
                        print("Marks must be between 0 and 100.")

                except ValueError:
                    print("Please enter a valid number!")

        student = Student(name, student_id, marks)

        self.students.append(student)
        self.save_data()

        print("\nStudent added successfully!")

    # Display all students
    def display_all_students(self):

        if not self.students:
            print("No student records available!")
            return

        print("\n========== ALL STUDENTS ==========")

        for student in self.students:
            student.display_result()

    # Find highest scoring student
    def highest_student(self):

        if not self.students:
            print("No student records available!")
            return

        highest = max(
            self.students,
            key=lambda student: student.calculate_total()
        )

        print("\n========== HIGHEST SCORING STUDENT ==========")
        highest.display_result()

    # Find lowest scoring student
    def lowest_student(self):

        if not self.students:
            print("No student records available!")
            return

        lowest = min(
            self.students,
            key=lambda student: student.calculate_total()
        )

        print("\n========== LOWEST SCORING STUDENT ==========")
        lowest.display_result()

    # Class performance summary
    def class_summary(self):

        if not self.students:
            print("No student records available!")
            return

        total_students = len(self.students)

        passed = sum(
            1 for student in self.students
            if student.get_status() == "PASS"
        )

        failed = total_students - passed

        total_marks = sum(
            student.calculate_total()
            for student in self.students
        )

        class_average = total_marks / (total_students * len(SUBJECTS))

        pass_rate = (passed / total_students) * 100
        fail_rate = (failed / total_students) * 100

        print("\n========== CLASS PERFORMANCE SUMMARY ==========")
        print("Total Students:", total_students)
        print("Passed Students:", passed)
        print("Failed Students:", failed)
        print("Class Average:", round(class_average, 2))
        print("Pass Rate:", round(pass_rate, 2), "%")
        print("Fail Rate:", round(fail_rate, 2), "%")
        print("================================================")


# =====================================
# 3. MAIN MENU FUNCTION
# =====================================

def main():

    manager = ResultManager()

    while True:

        print("\n")
        print("==========================================")
        print(" STUDENT RESULT & PERFORMANCE MANAGEMENT")
        print("==========================================")
        print("1. Add New Student")
        print("2. Search Student by ID")
        print("3. Display All Students")
        print("4. Highest Scoring Student")
        print("5. Lowest Scoring Student")
        print("6. Class Performance Summary")
        print("7. Exit")
        print("==========================================")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            manager.add_student()

        elif choice == "2":
            student_id = input("Enter Student ID: ").strip()
            manager.search_student(student_id)

        elif choice == "3":
            manager.display_all_students()

        elif choice == "4":
            manager.highest_student()

        elif choice == "5":
            manager.lowest_student()

        elif choice == "6":
            manager.class_summary()

        elif choice == "7":
            print("\nThank you for using the system!")
            print("Program closed successfully.")
            break

        else:
            print("Invalid choice! Please select 1-7.")


# =====================================
# 4. START THE PROGRAM
# =====================================

if __name__ == "__main__":
    main()
