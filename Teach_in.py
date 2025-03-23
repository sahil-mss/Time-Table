import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from csv import writer, reader

def write_teacher(teachers):
    with open('Teacher.csv', 'w', newline='') as f:
        csv_writer = writer(f)
        csv_writer.writerows(teachers)

def input_manual():
    def save_teachers():
        num = num_teach.get().strip()
        if not num.isdigit():
            messagebox.showerror("Error", "Enter a valid number")
            return
        num = int(num)
        teachers = []
        for i in range(num):
            name = name_entries[i].get().strip().title()
            subject = subject_entries[i].get().strip().title()
            if not name or not subject:
                messagebox.showerror("Error", "All fields must be filled!")
                return
            teachers.append([i+1, name, subject])
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to save?")
        if confirm:
            write_teacher(teachers)
            messagebox.showinfo("Success", "Teachers saved to Teacher.csv")
            manual_window.destroy()

    def generate_entries():
        num = num_teach.get().strip()
        if not num.isdigit():
            messagebox.showerror("Error", "Enter a valid number")
            return
        num = int(num)
        for widget in entry_frame.winfo_children():
            widget.destroy()
        name_entries.clear()
        subject_entries.clear()
        tk.Label(entry_frame, text="Teacher Name", font=("Arial", 10, "bold"), bg="white").grid(row = 0, column = 0, padx = 10, pady = 5)
        tk.Label(entry_frame, text="Subject", font=("Arial", 10, "bold"), bg="white").grid(row = 0, column = 1, padx = 10, pady = 5)
        def move_focus(event, entry_list, index, direction):
            new_index = index + direction
            if 0 <= new_index < len(entry_list):
                entry_list[new_index].focus_set()
        for i in range(num):
            name_entry = tk.Entry(entry_frame, width = 20, justify = 'center', relief = "flat", highlightthickness=0)
            subject_entry = tk.Entry(entry_frame, width = 20, justify='center', relief = "flat", highlightthickness=0)
            name_entry.grid(row = i+1, column = 0, padx = 10, pady = 5)
            subject_entry.grid(row = i+1, column = 1, padx = 10, pady = 5)
            name_entries.append(name_entry)
            subject_entries.append(subject_entry)
            name_entry.bind("<Down>", lambda e, i=i: move_focus(e, name_entries, i, 1))
            name_entry.bind("<Up>", lambda e, i=i: move_focus(e, name_entries, i, -1))
            subject_entry.bind("<Down>", lambda e, i=i: move_focus(e, subject_entries, i, 1))
            subject_entry.bind("<Up>", lambda e, i=i: move_focus(e, subject_entries, i, -1))
            name_entry.bind("<Right>", lambda e, i=i: subject_entries[i].focus_set())
            subject_entry.bind("<Left>", lambda e, i=i: name_entries[i].focus_set())
        save_button.pack_forget()
        save_button.pack(pady = 10)
        canvas.update_idletasks()
        canvas.config(scrollregion = canvas.bbox("all"))
    manual_window = tk.Toplevel(option_1)
    manual_window.title("Manual Input")
    manual_window.geometry("500x400")
    tk.Label(manual_window, text="Enter number of teachers:").pack()
    num_teach = tk.Entry(manual_window, width = 5)
    num_teach.pack(pady = 10)
    generate_button = tk.Button(manual_window, text="Generate Fields", command=generate_entries)
    generate_button.pack(pady = 5)
    canvas = tk.Canvas(manual_window, width = 400, height = 250)
    scrollbar = ttk.Scrollbar(manual_window, orient = "vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    scrollable_frame.bind("<Configure>", lambda e: canvas.config(scrollregion = canvas.bbox("all")))
    canvas.create_window((0, 0), window = scrollable_frame, anchor = "nw")
    canvas.configure(yscrollcommand = scrollbar.set)
    canvas.pack(side="left", fill = "both", expand=True)
    scrollbar.pack(side="right", fill="y")
    entry_frame = tk.Frame(scrollable_frame)
    entry_frame.pack()
    name_entries = []
    subject_entries = []
    save_button = tk.Button(manual_window, text = "Save Teachers", command=save_teachers)
    save_button.pack(pady = 10)

def input_file():
    file_path = filedialog.askopenfilename(title = "Select a file", filetypes = [("CSV Files", "*.csv"), ("Excel Files", "*.xlsx"), ("All Files", "*.*")])
    if not file_path:
        return
    teachers = []
    try:
        if file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
            teachers = df.values.tolist()
        elif file_path.endswith('.csv'):
            with open(file_path, 'r', newline='') as f:
                teachers = [row for row in reader(f)]
        else:
            messagebox.showerror("Error", "Invalid file type! Please select a CSV or Excel file.")
            return
        write_teacher(teachers)
        messagebox.showinfo("Success", "Teachers saved to Teacher.csv")
    except Exception as e:

        messagebox.showerror("Error", f"Failed to read file: {e}")
def teach_select():
    option_1 = tk.Tk()
    option_1.title("Add Teachers")
    option_1.geometry("200x85")
    button_manual = tk.Button(option_1, text="Input Teachers Manually", command=input_manual)
    button_manual.pack(pady = 10)
    button_file = tk.Button(option_1, text="Input Teachers From A File", command=input_file)
    button_file.pack()
    option_1.mainloop()
