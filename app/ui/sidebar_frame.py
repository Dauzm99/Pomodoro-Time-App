# app/ui/sidebar_frame.py
import customtkinter as ctk
from config import settings

class SidebarFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=10)
        self.controller = controller

        self.grid_rowconfigure(4, weight=1) # Add weight to a spacer row

        # --- Logo/Title ---
        self.logo_label = ctk.CTkLabel(self, text="TimeSplit", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # --- Navigation Buttons ---
        self.timer_button = ctk.CTkButton(self, text="Timer", command=lambda: controller.show_frame("TimerFrame"))
        self.timer_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.planner_button = ctk.CTkButton(self, text="Planner", command=lambda: controller.show_frame("PlannerFrame"))
        self.planner_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.analytics_button = ctk.CTkButton(self, text="Analytics", command=lambda: controller.show_frame("AnalyticsFrame"))
        self.analytics_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        # --- <<< NEW: Reminder Section >>> ---
        self.reminder_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.reminder_frame.grid(row=5, column=0, padx=20, pady=10, sticky="s")
        
        reminder_title = ctk.CTkLabel(self.reminder_frame, text="Next Reminder", font=ctk.CTkFont(weight="bold"))
        reminder_title.pack()

        self.hydration_label = ctk.CTkLabel(self.reminder_frame, text="💧 Water: 20:00")
        self.hydration_label.pack()

        # --- Mode Switcher (Bottom) ---
        self.mode_label = ctk.CTkLabel(self, text="Mode Switch", anchor="w")
        self.mode_label.grid(row=6, column=0, padx=20, pady=(10, 0), sticky="s")
        self.mode_switch = ctk.CTkSwitch(self, text="Work 🧑‍💻 / Study 📖", command=self.toggle_mode, progress_color=settings.THEMES["Study"]["primary"])
        self.mode_switch.grid(row=7, column=0, padx=20, pady=10, sticky="s")

    # <<< NEW: Method to update the label's text >>>
    def update_hydration_label(self, seconds_left):
        minutes, seconds = divmod(seconds_left, 60)
        self.hydration_label.configure(text=f"💧 Water: {minutes:02d}:{seconds:02d}")

    def toggle_mode(self):
        new_mode = "Study" if self.mode_switch.get() == 1 else "Work"
        self.controller.current_mode.set(new_mode)

    def update_theme(self):
        theme = self.controller.theme
        self.logo_label.configure(text_color=theme["primary"])
        self.mode_switch.configure(progress_color=theme["secondary"])