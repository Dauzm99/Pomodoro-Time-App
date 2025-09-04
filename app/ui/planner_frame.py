# app/ui/planner_frame.py
import customtkinter as ctk
from tkcalendar import DateEntry
from tkinter import messagebox
from datetime import datetime

class PlannerFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._setup_widgets()
        self.update_theme()

    def _setup_widgets(self):
        # --- Create Tab View ---
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.tab_view.add("Add Task")
        self.tab_view.add("Add Event")
        self.tab_view._segmented_button.grid(sticky="ew") # Ensure tabs fill width

        # --- Populate "Add Task" Tab ---
        self.setup_task_tab()
        
        # --- Populate "Add Event" Tab ---
        self.setup_event_tab()

        # --- Task & Event List (remains the same) ---
        self.task_list_frame = ctk.CTkScrollableFrame(self, label_text="Task & Event List")
        self.task_list_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    def setup_task_tab(self):
        task_tab = self.tab_view.tab("Add Task")
        task_tab.grid_columnconfigure(0, weight=1)

        self.task_entry = ctk.CTkEntry(task_tab, placeholder_text="Enter new task description...")
        self.task_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.date_entry = DateEntry(task_tab, date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=0, column=1, padx=10, pady=10)

        self.priority_menu = ctk.CTkOptionMenu(task_tab, values=["Low", "Medium", "High"])
        self.priority_menu.grid(row=0, column=2, padx=10, pady=10)
        
        self.sync_to_gcal_check = ctk.CTkCheckBox(task_tab, text="Sync as All-Day Event")
        self.sync_to_gcal_check.grid(row=0, column=3, padx=10, pady=10)

        self.add_task_button = ctk.CTkButton(task_tab, text="Add Task", command=self.add_task)
        self.add_task_button.grid(row=0, column=4, padx=10, pady=10)

    def setup_event_tab(self):
        event_tab = self.tab_view.tab("Add Event")
        event_tab.grid_columnconfigure(1, weight=1)
        
        # Row 1: Summary and Date
        ctk.CTkLabel(event_tab, text="Event Summary:").grid(row=0, column=0, padx=(10,0), pady=10, sticky="w")
        self.event_summary_entry = ctk.CTkEntry(event_tab, placeholder_text="e.g., Doctor's Appointment")
        self.event_summary_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(event_tab, text="Date:").grid(row=0, column=3, padx=(10,0), pady=10, sticky="w")
        self.event_date_entry = DateEntry(event_tab, date_pattern='yyyy-mm-dd')
        self.event_date_entry.grid(row=0, column=4, padx=10, pady=10)

        # Row 2: Time Inputs
        time_options = [f"{h:02d}" for h in range(24)]
        minute_options = ["00", "15", "30", "45"]

        ctk.CTkLabel(event_tab, text="Start Time:").grid(row=1, column=0, padx=(10,0), pady=10, sticky="w")
        self.start_hour_menu = ctk.CTkOptionMenu(event_tab, values=time_options)
        self.start_hour_menu.grid(row=1, column=1, padx=(10,0), pady=10, sticky="w")
        self.start_minute_menu = ctk.CTkOptionMenu(event_tab, values=minute_options)
        self.start_minute_menu.grid(row=1, column=2, padx=(0,10), pady=10, sticky="w")
        
        ctk.CTkLabel(event_tab, text="End Time:").grid(row=1, column=3, padx=(10,0), pady=10, sticky="w")
        self.end_hour_menu = ctk.CTkOptionMenu(event_tab, values=time_options)
        self.end_hour_menu.grid(row=1, column=4, padx=(10,0), pady=10, sticky="w")
        self.end_minute_menu = ctk.CTkOptionMenu(event_tab, values=minute_options)
        self.end_minute_menu.grid(row=1, column=5, padx=(0,10), pady=10, sticky="w")
        
        self.add_event_button = ctk.CTkButton(event_tab, text="Add Event to Google Calendar", command=self.add_event)
        self.add_event_button.grid(row=2, column=0, columnspan=6, padx=10, pady=(10,20), sticky="ew")
        
    def add_task(self):
        # ... (This function is mostly unchanged, but now calls create_all_day_event)
        task_text = self.task_entry.get().strip()
        if not task_text: return messagebox.showwarning("Warning", "Task cannot be empty.")
            
        task = { "text": task_text, "deadline": self.date_entry.get_date().strftime('%Y-%m-%d'), "priority": self.priority_menu.get(), "done": False }
        
        mode = self.controller.current_mode.get()
        if 'tasks' not in self.controller.app_data: self.controller.app_data['tasks'] = {"Work": [], "Study": []}
        self.controller.app_data['tasks'][mode].append(task)
        
        if self.sync_to_gcal_check.get():
            event = self.controller.gcal_service.create_all_day_event(f"[{mode}] {task_text}", task['deadline'])
            if event: messagebox.showinfo("Success", "Task added as an all-day event to Google Calendar.")
            else: messagebox.showerror("Error", "Could not create Google Calendar event.")

        self.task_entry.delete(0, 'end')
        self.refresh_task_list()

    def add_event(self):
        summary = self.event_summary_entry.get().strip()
        if not summary: return messagebox.showwarning("Warning", "Event summary cannot be empty.")

        date = self.event_date_entry.get_date()
        start_hour, start_min = int(self.start_hour_menu.get()), int(self.start_minute_menu.get())
        end_hour, end_min = int(self.end_hour_menu.get()), int(self.end_minute_menu.get())

        try:
            start_dt = datetime.combine(date, datetime.min.time()).replace(hour=start_hour, minute=start_min)
            end_dt = datetime.combine(date, datetime.min.time()).replace(hour=end_hour, minute=end_min)

            if end_dt <= start_dt:
                return messagebox.showerror("Error", "End time must be after start time.")

            event = self.controller.gcal_service.create_timed_event(summary, start_dt.isoformat(), end_dt.isoformat())
            if event:
                messagebox.showinfo("Success", f"Event '{summary}' was added to your Google Calendar.")
                self.refresh_task_list()
            else:
                messagebox.showerror("Error", "Could not create event. Check console for details.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    # The rest of the file (refresh_task_list, display helpers, update_theme, on_show) remains IDENTICAL to the previous version
    def refresh_task_list(self):
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()
        self.display_gcal_events()
        self.display_local_tasks()

    def display_gcal_events(self):
        gcal_label = ctk.CTkLabel(self.task_list_frame, text="--- Upcoming Google Calendar Events ---", font=ctk.CTkFont(slant="italic"))
        gcal_label.pack(fill="x", padx=5, pady=(10, 5))
        try:
            events = self.controller.gcal_service.get_upcoming_events()
            if not events:
                ctk.CTkLabel(self.task_list_frame, text="No upcoming events found.").pack(padx=5, pady=2)
                return
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                time_str = dt.strftime('%b %d, %I:%M %p') if 'T' in start else dt.strftime('%b %d, All-day')
                event_widget = ctk.CTkLabel(self.task_list_frame, text=f"🗓️ {event['summary']} ({time_str})", anchor="w")
                event_widget.pack(fill="x", padx=5, pady=2)
        except Exception as e:
            ctk.CTkLabel(self.task_list_frame, text=f"Error fetching Google Calendar events: {e}", text_color="red").pack(padx=5, pady=2)

    def display_local_tasks(self):
        local_label = ctk.CTkLabel(self.task_list_frame, text="--- Your Local Tasks ---", font=ctk.CTkFont(slant="italic"))
        local_label.pack(fill="x", padx=5, pady=(20, 5))
        mode = self.controller.current_mode.get()
        tasks = self.controller.app_data.get('tasks', {}).get(mode, [])
        priority_map = {"High": 1, "Medium": 2, "Low": 3}
        sorted_tasks = sorted(tasks, key=lambda t: (t['done'], priority_map.get(t['priority'], 3)))
        for i, task in enumerate(sorted_tasks):
            self.create_task_widget(task, i).pack(fill="x", padx=5, pady=5)

    def create_task_widget(self, task, index):
        task_frame = ctk.CTkFrame(self.task_list_frame)
        check_var = ctk.StringVar(value="on" if task["done"] else "off")
        checkbox = ctk.CTkCheckBox(task_frame, text=task["text"], variable=check_var, onvalue="on", offvalue="off", command=lambda i=index: self.toggle_task_done(i))
        checkbox.pack(side="left", padx=10, pady=10)
        delete_button = ctk.CTkButton(task_frame, text="🗑️", width=30, command=lambda i=index: self.delete_task(i), fg_color="#58181F", hover_color="#C21A09")
        delete_button.pack(side="right", padx=10, pady=10)
        priority_colors = {"High": "#E74C3C", "Medium": "#F39C12", "Low": "#3498DB"}
        priority_label = ctk.CTkLabel(task_frame, text=task["priority"], width=80, text_color=priority_colors.get(task["priority"]), font=ctk.CTkFont(weight="bold"))
        priority_label.pack(side="right", padx=10, pady=10)
        deadline_label = ctk.CTkLabel(task_frame, text=f"Due: {task['deadline']}")
        deadline_label.pack(side="right", padx=10, pady=10)
        return task_frame
        
    def toggle_task_done(self, index):
        mode = self.controller.current_mode.get()
        self.controller.app_data['tasks'][mode][index]['done'] = not self.controller.app_data['tasks'][mode][index]['done']
        self.refresh_task_list()
        
    def delete_task(self, index):
        mode = self.controller.current_mode.get()
        self.controller.app_data['tasks'][mode].pop(index)
        self.refresh_task_list()

    def update_theme(self):
        theme = self.controller.theme
        self.tab_view.configure(segmented_button_selected_color=theme["primary"], segmented_button_selected_hover_color=theme["secondary"])
        self.task_list_frame.configure(label_text_color=theme["primary"])
        self.add_task_button.configure(fg_color=theme["primary"], hover_color=theme["secondary"])
        self.add_event_button.configure(fg_color=theme["primary"], hover_color=theme["secondary"])
        self.refresh_task_list()

    def on_show(self):
        self.update_theme()