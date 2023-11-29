import tkinter as tk
from datetime import datetime, timedelta

class Task:
    def __init__(self, name, priority, deadline):
        self.name = name
        self.priority = priority
        self.deadline = deadline

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Scheduler")

        self.schedule_label = tk.Label(root, text="Enter Preexisting Schedule (one entry per line):")
        self.schedule_label.pack()

        self.schedule_text = tk.Text(root, height=10, width=40)
        self.schedule_text.pack()

        self.add_task_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_task_button.pack()

        self.generate_schedule_button = tk.Button(root, text="Generate Schedule", command=self.generate_schedule)
        self.generate_schedule_button.pack()

        self.tasks = []

    def add_task(self):
        task_name = input("Enter task name: ")
        task_priority = int(input("Enter task priority (1 to 10): "))
        task_deadline = datetime.strptime(input("Enter task deadline (YYYY-MM-DD): "), "%Y-%m-%d")

        task = Task(task_name, task_priority, task_deadline)
        self.tasks.append(task)

    def generate_schedule(self):
        sorted_tasks = sorted(self.tasks, key=lambda x: (x.deadline, -x.priority))

        preexisting_schedule = self.schedule_text.get("1.0", tk.END).splitlines()
        schedule_text = ""

        current_time = datetime.now()
        for entry in preexisting_schedule:
            if entry:
                schedule_text += f"{current_time.strftime('%Y-%m-%d %H:%M')} - {entry}\n"
                current_time += timedelta(hours=1)  # Assuming each entry takes an hour

        for task in sorted_tasks:
            if current_time < task.deadline:
                schedule_text += f"{task.name} (Priority: {task.priority}, Deadline: {task.deadline})\n"
                current_time += timedelta(hours=1)  # Assuming each task takes an hour

        self.schedule_text.delete(1.0, tk.END)
        self.schedule_text.insert(tk.END, schedule_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
