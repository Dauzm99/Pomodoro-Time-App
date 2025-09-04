# app/app_logic.py
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

from config import settings
from data import persistence
from services.google_calendar import GoogleCalendarService
from app.ui.sidebar_frame import SidebarFrame
from app.ui.timer_frame import TimerFrame
from app.ui.planner_frame import PlannerFrame
from app.ui.analytics_frame import AnalyticsFrame

class TimeSplitApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Load Data and Services ---
        self.app_data = persistence.load_data()
        self.gcal_service = GoogleCalendarService()

        # --- Core App State ---
        self.title(settings.APP_NAME)
        self.geometry(settings.GEOMETRY)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.current_mode = ctk.StringVar(value="Work")
        self.current_mode.trace_add("write", self.on_mode_change)
        
        self.theme = settings.THEMES[self.current_mode.get()]

        # <<< NEW: Hydration Reminder State >>>
        self.HYDRATION_INTERVAL_SEC = 20 * 60  # 20 minutes
        self.hydration_reminder_time_left = self.HYDRATION_INTERVAL_SEC

        self._setup_ui()
        self.on_mode_change()

        # <<< NEW: Start the global reminder loop >>>
        self._update_hydration_reminder()

    # <<< NEW: Global reminder loop that runs every second >>>
    def _update_hydration_reminder(self):
        self.hydration_reminder_time_left -= 1

        if self.hydration_reminder_time_left <= 0:
            messagebox.showinfo("Hydration Reminder", "Time for a cup of water! 💧")
            self.hydration_reminder_time_left = self.HYDRATION_INTERVAL_SEC
        
        # Update the label in the sidebar
        if hasattr(self, 'sidebar_frame'):
            self.sidebar_frame.update_hydration_label(self.hydration_reminder_time_left)

        # Schedule this function to run again after 1000ms (1 second)
        self.after(1000, self._update_hydration_reminder)

    def _setup_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = SidebarFrame(self, self)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsw", padx=10, pady=10)

        self.main_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (TimerFrame, PlannerFrame, AnalyticsFrame):
            frame = F(self.main_frame, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        self.show_frame("TimerFrame")

    def show_frame(self, page_name):
        # ... (no change to this function)
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, 'on_show'):
            frame.on_show()

    def on_mode_change(self, *args):
        # ... (no change to this function)
        mode = self.current_mode.get()
        self.theme = settings.THEMES[mode]
        self.sidebar_frame.update_theme()
        for frame in self.frames.values():
            if hasattr(frame, 'update_theme'):
                frame.update_theme()
        for name, frame in self.frames.items():
            if frame.winfo_viewable():
                self.show_frame(name)
                break

    def log_session(self, label, duration_seconds):
        # ... (no change to this function)
        timestamp = datetime.now().isoformat()
        mode = self.current_mode.get()
        if "logs_df" not in self.app_data:
            self.app_data['logs_df'] = []
        self.app_data['logs_df'].append({
            'timestamp': timestamp,
            'label': label,
            'duration_sec': duration_seconds,
            'mode': mode
        })

    def on_closing(self):
        # ... (no change to this function)
        persistence.save_data(self.app_data)
        self.destroy()