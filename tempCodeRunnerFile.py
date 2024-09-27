import tkinter as tk
from tkinter import messagebox, ttk
import csv
import matplotlib.pyplot as plt
import pandas as pd
from PIL import ImageTk, Image

# Load student and teacher data from CSV file
students_data = {}
teachers_data = {}

# Load student data
def load_student_data(file_path):
    global students_data
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row["Name"]
            attendance = row["Attendance"]
            marks = {
                "Math": row["Math"],
                "Science": row["Science"],
                "History": row["History"],
                "Biology": row["Biology"]
            }
            assignments = {
                "Math Assignment": row["Math Assignment"],
                "Science Project": row["Science Project"],
                "History Essay": row["History Essay"],
                "Biology Lab": row["Biology Lab"]
            }
            feedback = {
                "Math Assignment": "",
                "Science Project": "",
                "History Essay": "",
                "Biology Lab": ""
            }
            assignments = {k: v for k, v in assignments.items() if v}
            marks = {k: v for k, v in marks.items() if v}
            students_data[name] = {
                "attendance": attendance,
                "marks": marks,
                "performance": assignments,
                "feedback": feedback
            }

# Load teacher data
def load_teacher_data(file_path):
    global teachers_data
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row["Name"]
            teachers_data[name] = {
                "students": row["Students"].split(',')
            }

# Define color palette
bg_color = "#eaeaea"
header_color = "#4b9cd3"
button_color = "#1c5a99"
font_color = "#ffffff"
label_color = "#333333"

# Initialize the Tkinter window
root = tk.Tk()
root.title("Student Performance Evaluation")
root.geometry("700x700")
root.config(bg=bg_color)

# Set file paths for student and teacher data
student_file_path = r"student_data.csv"  # Update this path
teacher_file_path = r"teacher_data.csv"  # Update this path

# Load data files
load_student_data(student_file_path)
load_teacher_data(teacher_file_path)

current_user = None
user_type = None

# Function to login a student
def login_student():
    global current_user, user_type
    username = student_entry.get()
    if username in students_data:
        current_user = username
        user_type = "student"
        show_student_ui()
    else:
        messagebox.showerror("Error", "Student not found!")

# Function to login a teacher
def login_teacher():
    global current_user, user_type
    username = teacher_entry.get()
    password = teacher_password_entry.get()
    if username in teachers_data and password == "teacher":
        current_user = username
        user_type = "teacher"
        show_teacher_ui()
    else:
        messagebox.showerror("Error", "Teacher not found or invalid password!")

# Function to logout
def logout():
    global current_user, user_type
    current_user = None
    user_type = None
    login_screen()

# Function to visualize marks in a bar graph
def visualize_marks():
    marks = students_data[current_user]['marks']
    subjects = list(marks.keys())
    scores = [int(marks[subj]) for subj in subjects]
    
    plt.bar(subjects, scores, color='#eb9b34')
    plt.xlabel('Subjects')
    plt.ylabel('Marks')
    plt.title(f'Marks of {current_user}')
    plt.show()

# Function to display marks in tabular form
def display_marks_table():
    marks = students_data[current_user]['marks']
    df = pd.DataFrame(list(marks.items()), columns=['Subject', 'Marks'])
    table_window = tk.Toplevel(root)
    table_window.title(f"Marks for {current_user}")
    
    tree = ttk.Treeview(table_window, columns=('Subject', 'Marks'), show='headings')
    tree.heading('Subject', text='Subject')
    tree.heading('Marks', text='Marks')
    
    for index, row in df.iterrows():
        tree.insert("", "end", values=(row['Subject'], row['Marks']))
    
    tree.pack()

# Function to save feedback to a file
def save_feedback(assignment_feedback_entries):
    with open("feedbacks.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([current_user] + [assignment_feedback_entries[assignment].get("1.0", tk.END).strip() for assignment in assignment_feedback_entries])

# Function to show student UI after login
def show_student_ui():
    clear_screen()
    
    header = tk.Label(root, text=f"Welcome {current_user}", bg=header_color, fg=font_color, font=("Arial", 18), padx=10, pady=10)
    header.pack(fill="x")

    performance_frame = tk.Frame(root, bg=bg_color)
    performance_frame.pack(pady=20, padx=20, fill="both", expand=True)

    tk.Label(performance_frame, text="Assignments", font=("Arial", 14, "bold"), bg=bg_color, fg=label_color).pack(pady=5)
    assignment_feedback_entries = {}
    
    for assignment, score in students_data[current_user]['performance'].items():
        tk.Label(performance_frame, text=f"{assignment}: {score}", bg=bg_color, fg=label_color).pack()
        feedback_label = tk.Label(performance_frame, text="Your Feedback:", bg=bg_color, fg=label_color)
        feedback_label.pack(pady=5)
        feedback_entry = tk.Text(performance_frame, height=2, width=50)
        feedback_entry.pack(pady=5)
        assignment_feedback_entries[assignment] = feedback_entry

    tk.Label(performance_frame, text="Attendance", font=("Arial", 14, "bold"), bg=bg_color, fg=label_color).pack(pady=5)
    tk.Label(performance_frame, text=students_data[current_user]['attendance'], bg=bg_color, fg=label_color).pack()

    tk.Label(performance_frame, text="Marks", font=("Arial", 14, "bold"), bg=bg_color, fg=label_color).pack(pady=5)
    for subject, mark in students_data[current_user]['marks'].items():
        tk.Label(performance_frame, text=f"{subject}: {mark}", bg=bg_color, fg=label_color).pack()

    tk.Button(performance_frame, text="Submit Feedback", bg=button_color, fg=font_color, command=lambda: save_feedback(assignment_feedback_entries)).pack(pady=0)
    tk.Button(root, text="Visualize Marks", bg=button_color, fg=font_color, command=visualize_marks).pack(pady=5)
    tk.Button(root, text="View Marks Table", bg=button_color, fg=font_color, command=display_marks_table).pack(pady=5)
    tk.Button(root, text="Logout", bg=button_color, fg=font_color, command=logout).pack(pady=5)

# Function to show teacher UI after login
def show_teacher_ui():
    clear_screen()
    
    header = tk.Label(root, text=f"Welcome Teacher {current_user}", bg=header_color, fg=font_color, font=("Arial", 18), padx=10, pady=10)
    header.pack(fill="x")
    
    performance_frame = tk.Frame(root, bg=bg_color)
    performance_frame.pack(pady=20, padx=20, fill="both", expand=True)

    tk.Label(performance_frame, text="Assigned Students Performance", font=("Arial", 16, "bold"), bg=bg_color, fg=label_color).pack(pady=10)
    
    for student in teachers_data[current_user]['students']:
        tk.Label(performance_frame, text=f"Performance of {student}:", font=("Arial", 14, "bold"), bg=bg_color, fg=label_color).pack(pady=5)
        if student in students_data:
            tk.Label(performance_frame, text=f"Attendance: {students_data[student]['attendance']}", bg=bg_color, fg=label_color).pack()
            tk.Label(performance_frame, text="Marks:", bg=bg_color, fg=label_color).pack()
            for subject, mark in students_data[student]['marks'].items():
                tk.Label(performance_frame, text=f"  {subject}: {mark}", bg=bg_color, fg=label_color).pack()

            tk.Label(performance_frame, text="Assignments:", bg=bg_color, fg=label_color).pack()
            for assignment, score in students_data[student]['performance'].items():
                tk.Label(performance_frame, text=f"  {assignment}: {score}", bg=bg_color, fg=label_color).pack()

            tk.Label(performance_frame, text="Feedback:", bg=bg_color, fg=label_color).pack()
            for assignment, feedback in students_data[student]['feedback'].items():
                tk.Label(performance_frame, text=f"  {assignment}: {feedback}", bg=bg_color, fg=label_color).pack()
    
    tk.Button(root, text="Logout", bg=button_color, fg=font_color, command=logout).pack(pady=20)

# Function to clear the screen
def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

# Login screen with logo and heading
def login_screen():
    clear_screen()

    login_frame = tk.Frame(root, bg=bg_color)
    login_frame.pack(pady=50)

    # Add your logo (ensure you have the image path set correctly)
    logo_image = Image.open("logo.png")  # Update the path to your logo image
    logo_image = logo_image.resize((180,140))
    logo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(login_frame, image=logo, bg=bg_color)
    logo_label.image = logo  # Keep a reference to the image
    logo_label.pack()

    # Add your heading
    heading = tk.Label(login_frame, text="Student and Teacher Performance Tracker", font=("Arial", 24), bg=header_color, fg=font_color, padx=10, pady=10)
    heading.pack(fill="x")

    tk.Label(login_frame, text="Login as a Student or Teacher", font=("Arial", 20), bg=header_color, fg=font_color, padx=10, pady=10).pack(fill="x")

    # Student login
    tk.Label(login_frame, text="Student Username", bg=bg_color, fg=label_color).pack(pady=5)
    global student_entry
    student_entry = tk.Entry(login_frame)
    student_entry.pack(pady=5)

    tk.Button(login_frame, text="Login as Student", bg=button_color, fg=font_color, command=login_student).pack(pady=10)

    # Teacher login
    tk.Label(login_frame, text="Teacher Username", bg=bg_color, fg=label_color).pack(pady=5)
    global teacher_entry, teacher_password_entry
    teacher_entry = tk.Entry(login_frame)
    teacher_entry.pack(pady=5)

    tk.Label(login_frame, text="Password", bg=bg_color, fg=label_color).pack(pady=5)
    teacher_password_entry = tk.Entry(login_frame, show="*")
    teacher_password_entry.pack(pady=5)

    tk.Button(login_frame, text="Login as Teacher", bg=button_color, fg=font_color, command=login_teacher).pack(pady=10)

# Start the login screen
login_screen()

root.mainloop()
