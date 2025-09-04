# app/ui/timer_frame.py
import customtkinter as ctk
from tkinter import messagebox
from config import settings
from app.ui.breathing_frame import BreathingToplevel

class TimerFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Timer state
        self.timer_running = False
        self.time_left = self.get_focus_duration_seconds() # Use new method to get duration
        self.current_session_type = "Focus"
        self._timer_job = None

        self._setup_widgets()
        self.update_timer_display()

    def _setup_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.mode_indicator = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=16, slant="italic"))
        self.mode_indicator.grid(row=0, column=0, pady=(20, 0))
        
        self.timer_label = ctk.CTkLabel(self, text="25:00", font=ctk.CTkFont(size=120, weight="bold"))
        self.timer_label.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        # --- Session Labeling (remains the same) ---
        self.session_label_entry = ctk.CTkEntry(self, placeholder_text="Label your session...", width=300)
        self.session_label_entry.grid(row=2, column=0, pady=10)

        # --- Timer Type Selection Buttons ---
        timer_type_frame = ctk.CTkFrame(self, fg_color="transparent")
        timer_type_frame.grid(row=3, column=0, pady=10)

        self.focus_button = ctk.CTkButton(timer_type_frame, text="Focus", command=lambda: self.set_timer("Focus"))
        self.focus_button.pack(side="left", padx=5)

        self.short_break_button = ctk.CTkButton(timer_type_frame, text="Short Break", command=lambda: self.set_timer("Short Break"))
        self.short_break_button.pack(side="left", padx=5)

        self.long_break_button = ctk.CTkButton(timer_type_frame, text="Long Break", command=lambda: self.set_timer("Long Break"))
        self.long_break_button.pack(side="left", padx=5)

        # --- NEW: Button to edit the focus timer ---
        self.edit_timer_button = ctk.CTkButton(timer_type_frame, text="✏️ Edit", width=50, command=self.set_custom_focus_time)
        self.edit_timer_button.pack(side="left", padx=10)

        # --- Main Controls ---
        controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        controls_frame.grid(row=4, column=0, pady=10)

        self.start_button = ctk.CTkButton(controls_frame, text="Start", command=self.start_timer, width=100, height=40)
        self.start_button.pack(side="left", padx=10)

        self.stop_button = ctk.CTkButton(controls_frame, text="Stop", command=self.stop_timer, state="disabled", width=100, height=40)
        self.stop_button.pack(side="left", padx=10)

        self.reset_button = ctk.CTkButton(controls_frame, text="Reset", command=self.reset_timer, width=100, height=40)
        self.reset_button.pack(side="left", padx=10)
        
        self.breathing_button = ctk.CTkButton(self, text="🌬️ Take a Breathing Break", command=self.open_breathing_exercise, fg_color="grey")
        self.breathing_button.grid(row=5, column=0, pady=(10, 20))
        
        self.update_theme()

    # <<< NEW: Method to get the focus duration >>>
    def get_focus_duration_seconds(self):
        # Check for user-defined setting, otherwise use default from config
        minutes = self.controller.app_data.get('custom_pomodoro_minutes', settings.CUSTOM_POMODORO_DEFAULT_MINUTES)
        return minutes * 60
    
    # <<< NEW: Method to open the dialog and set the custom timer >>>
    def set_custom_focus_time(self):
        dialog = ctk.CTkInputDialog(text="Enter new focus duration in minutes:", title="Set Custom Timer")
        input_value = dialog.get_input()

        if input_value:
            try:
                minutes = int(input_value)
                if minutes <= 0:
                    raise ValueError("Duration must be positive.")
                
                # Save the new setting persistently
                self.controller.app_data['custom_pomodoro_minutes'] = minutes
                messagebox.showinfo("Success", f"Focus timer updated to {minutes} minutes.")

                # If the current session is a Focus session, update the timer immediately
                if self.current_session_type == "Focus" and not self.timer_running:
                    self.set_timer("Focus")

            except (ValueError, TypeError):
                messagebox.showerror("Invalid Input", "Please enter a valid positive number for the minutes.")

    def set_timer(self, session_type):
        if self.timer_running: return # Don't allow changes while timer is running
        
        self.current_session_type = session_type
        
        if session_type == "Focus":
            self.time_left = self.get_focus_duration_seconds()
        else: # For breaks, use the fixed settings
            self.time_left = settings.POMODORO_SETTINGS[session_type]
            
        self.update_timer_display()

    # --- OTHER METHODS (start, stop, etc.) remain mostly unchanged ---
    def open_breathing_exercise(self):
        # ... (no change)
        if not hasattr(self, 'breathing_window') or not self.breathing_window.winfo_exists():
            self.breathing_window = BreathingToplevel(self)
        self.breathing_window.focus()

    def start_timer(self):
        # ... (no change)
        if self.timer_running: return
        self.timer_running = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.tick()

    def stop_timer(self):
        # ... (no change)
        if not self.timer_running: return
        self.timer_running = False
        if self._timer_job:
            self.after_cancel(self._timer_job)
            self._timer_job = None
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")

    def reset_timer(self):
        self.stop_timer()
        self.set_timer(self.current_session_type)

    def tick(self):
        if self.timer_running and self.time_left > 0:
            self.time_left -= 1
            self.update_timer_display()
            self._timer_job = self.after(1000, self.tick)
        elif self.time_left == 0:
            self.timer_finished()

    def update_timer_display(self):
        minutes, seconds = divmod(self.time_left, 60)
        self.timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")

    def timer_finished(self):
        self.stop_timer()
        session_label = self.session_label_entry.get().strip() or "Unlabeled Session"
        
        if self.current_session_type == "Focus":
            # Log the actual duration used for the session
            duration = self.get_focus_duration_seconds()
            self.controller.log_session(session_label, duration)
            message = f"Focus session '{session_label}' completed! Time for a break."
        else:
            message = "Break finished! Ready for the next focus session?"
            self.wellness_reminder()

        messagebox.showinfo("Session Complete", message)
        self.set_timer("Short Break" if self.current_session_type == "Focus" else "Focus")

    def wellness_reminder(self):
        reminders = [ "💧 Hydrate now!", "👀 Take a 5-min eye break!", "🧘 Stretch your neck" ]
        import random
        messagebox.showinfo("Wellness Reminder", random.choice(reminders))
        
    def update_theme(self):
        theme = self.controller.theme
        self.timer_label.configure(text_color=theme["primary"])
        self.start_button.configure(fg_color=theme["primary"], hover_color=theme["secondary"])
        self.mode = self.controller.current_mode.get()
        self.mode_indicator.configure(text=f"{'🧑‍💻' if self.mode == 'Work' else '📖'} {self.mode} Mode")

    def on_show(self):
        self.update_theme()