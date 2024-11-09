import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("700x700")
        self.root.configure(bg="#f0f0f0")

        self.tasks = []
        self.filename = "todo_list.txt"
        self.load_tasks()

        #Title
        tk.Label(self.root, text="To-Do List", font=("Helvetica", 18, "bold"), bg="#f0f0f0", fg="#333").pack(pady=10)

        #Frames for input fields
        input_frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief=tk.GROOVE)
        input_frame.pack(padx=10, pady=10, fill=tk.BOTH)

        #UI Elements

        #Task Description

        tk.Label(input_frame, text = "Task Description:", font=("Helvetica", 12), bg="#ffffff").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.task_input = tk.Entry(input_frame, font=("Helvetica", 12), width=40, relief=tk.SOLID)
        self.task_input.grid(row=0, column=1, padx=5, pady=5)

        #Deadline

        tk.Label(input_frame, text="Deadline(YYYY-MM-DD):", font=("Helvetica", 12), bg="#ffffff").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.deadline_input = tk.Entry(input_frame, font=("Helvetica", 12), width=40, relief=tk.SOLID)
        self.deadline_input.grid(row=1, column=1, padx=5, pady=5)

        #Priority

        tk.Label(input_frame, text="Priority (Low, Medium, High):", font=("Helvetica", 12), bg="#ffffff").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.priority_input = tk.Entry(input_frame, font=("Helvetica", 12), width=40, relief=tk.SOLID)
        self.priority_input.grid(row=2, column=1, padx=5, pady=5)

        #Add Task Button

        self.add_task_button = tk.Button(self.root,text="Add Task", font=("Helvetica", 12), command=self.add_task, bg="#4CAF50", fg="white", bd=0, relief=tk.FLAT, width=20)
        self.add_task_button.pack(pady=10)

        #Task List Frame
        tasks_frame = tk.Frame(self.root, bg="#f0f0f0")
        tasks_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.tasks_listbox = tk.Listbox(tasks_frame, selectmode=tk.SINGLE, font=("Helvetica", 12), width=60, height=15, bg="#ffffff", fg="#333", bd=0, highlightthickness=0, relief=tk.FLAT)
        self.tasks_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        #ScrollBar for ListBox

        scrollbar = tk.Scrollbar(tasks_frame, orient=tk.VERTICAL, command=self.tasks_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tasks_listbox.config(yscrollcommand=scrollbar.set)

        #Completed and Delete Buttons

        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=10)
        self.mark_completed_button = tk.Button(button_frame, text="Mark as completed", font=("Helvetica", 12), command=self.mark_task_completed, bg="#2196F3", fg="white", bd=0, relief=tk.FLAT, width=15)
        self.mark_completed_button.grid(row=0, column=0, padx=10)

        self.delete_task_button = tk.Button(button_frame, text="Delete Task", font=("Helvetica", 12), command=self.delete_task, bg="#F44336", fg="white", bd=0, relief=tk.FLAT, width=15)
        self.delete_task_button.grid(row=0, column=1, padx=10)

        self.populate_tasks()

    def load_tasks(self):
            """Load tasks from a file."""
            if os.path.exists(self.filename):
                with open(self.filename,"r", encoding="utf-8") as file:
                    for line in file:
                        task, deadline, priority, status = line.strip().split(" | ")
                        self.tasks.append({
                            "task": task,
                            "deadline": deadline,
                            "priority": priority,
                            "completed": status == "True"
                        })

    def save_tasks(self):
         """Save tasks to a file."""
         with open(self.filename,"w") as file:
            for task in self.tasks:
                file.write(f"{task['task']} | {task['deadline']} | {task['priority']} | {task['completed']}\n")

    def add_task(self):
        """Add a new task."""
        task_text = self.task_input.get()
        deadline_text = self.deadline_input.get()
        priority_text = self.priority_input.get().capitalize()

        if task_text and deadline_text and priority_text in ["Low", "Medium", "High"]:
            try:
                    #Validate deadline data format
                 datetime.strptime(deadline_text, "%Y-%m-%d")
                 self.tasks.append({
                 "task": task_text,
                 "deadline": deadline_text,
                 "priority": priority_text,
                 "completed": False
                    })
                
                 self.task_input.delete(0, tk.END)
                 self.deadline_input.delete(0, tk.END)
                 self.priority_input.delete(0, tk.END)
                 self.populate_tasks()
                 self.save_tasks()
            except ValueError:

                    messagebox.showwarning("Input Error", "Please enter a valid date in YYYY-MM-DD format.")
            else:
                messagebox.showwarning("Input Error", "Please fill in all fields correctly.")

    def populate_tasks(self):
            """Display tasks in the ListBox."""
            self.tasks_listbox.delete(0, tk.END)
            for task in sorted(self.tasks, key=lambda x: x["priority"], reverse=True):
                status = "[Done]" if task["completed"] else "[Pending]"
                self.tasks_listbox.insert(tk.END, f"{task['task']} - Due: {task['deadline']} - Priority: {task['priority']}{status}")

    def mark_task_completed(self):
            """Mark the selected task as completed"""
            try:
                selected_index = self.tasks_listbox.curselection()[0]
                self.tasks[selected_index]["completed"] = True
                self.populate_tasks()
                self.save_tasks()
            except IndexError:
                messagebox.showwarning("Selection Error", "Please select a task to mark as completed.")

    def delete_task(self):
            """Delete the selected task."""
            try:
                selected_index = self.tasks_listbox.curselection()[0]
                del self.tasks[selected_index]
                self.populate_tasks()
                self.save_tasks()
            except IndexError:
                messagebox.showwarning("Selection Error", "Please select a task to delete.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()



