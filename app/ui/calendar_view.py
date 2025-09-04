# app/ui/calendar_view.py
import tkinter as tk
from tkinter import ttk
import datetime

class CalendarViewFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # --- Header and Controls ---
        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        ttk.Label(header_frame, text="Weekly Agenda", style="Header.TLabel").pack(side=tk.LEFT)
        self.sync_button = ttk.Button(header_frame, text="🔄 Sync with Google Calendar", command=self.sync_calendar)
        self.sync_button.pack(side=tk.RIGHT)

        # --- Agenda Display ---
        self.agenda_text = tk.Text(self, font=("Helvetica", 11), state=tk.DISABLED, relief=tk.FLAT)
        self.agenda_text.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

    def sync_calendar(self):
        """Fetch events and rebuild the agenda view."""
        self.sync_button.config(text="Syncing...")
        self.update() # Force UI update
        
        # Fetch events from Google Calendar
        events = self.controller.gcal_service.get_upcoming_events()
        
        self.update_agenda_display(events)
        
        self.sync_button.config(text="🔄 Sync with Google Calendar")

    def update_agenda_display(self, gcal_events=[]):
        """Populates the text widget with tasks and calendar events."""
        self.agenda_text.config(state=tk.NORMAL)
        self.agenda_text.delete("1.0", tk.END)

        today = datetime.date.today()
        
        for i in range(7): # Display for the next 7 days
            current_day = today + datetime.timedelta(days=i)
            day_str = current_day.strftime('%A, %B %d')
            self.agenda_text.insert(tk.END, f"--- {day_str} ---\n", ('day_header',))
            
            # TODO: Add local tasks from planner frame here if they have due dates
            
            # Add Google Calendar events
            day_has_event = False
            for event in gcal_events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                event_date = datetime.datetime.fromisoformat(start.replace('Z', '+00:00')).date()
                
                if event_date == current_day:
                    event_time = datetime.datetime.fromisoformat(start.replace('Z', '+00:00')).strftime('%I:%M %p') if 'T' in start else 'All-day'
                    summary = event['summary']
                    self.agenda_text.insert(tk.END, f"   GCal: {summary} ({event_time})\n")
                    day_has_event = True

            if not day_has_event:
                 self.agenda_text.insert(tk.END, "  No scheduled events.\n", ('no_event',))

            self.agenda_text.insert(tk.END, "\n")
        
        # --- Styling ---
        self.agenda_text.tag_configure('day_header', font=('Helvetica', 14, 'bold'), foreground=self.controller.theme["accent"])
        self.agenda_text.tag_configure('no_event', foreground="gray")
        self.agenda_text.config(state=tk.DISABLED, bg=self.controller.theme["bg"], fg=self.controller.theme["fg"])