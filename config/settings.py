# config/settings.py

import customtkinter  # <<< ADD THIS LINE

# --- Application Configuration ---
APP_NAME = "TimeSplit - Modern Productivity Manager"
GEOMETRY = "1200x800"
DATA_FILE_PATH = "data/app_data.json"

# --- Google Calendar API ---
CREDENTIALS_PATH = 'credentials/credentials.json'
TOKEN_PATH = 'credentials/token.json'
API_SCOPES = ['https://www.googleapis.com/auth/calendar']

# --- UI Themes (Modern Color Palette) ---
customtkinter.set_appearance_mode("Dark") # This will now work correctly

THEMES = {
    "Work": {
        "primary": "#3498db",      # Bright Blue
        "secondary": "#2980b9",    # Darker Blue
        "fg_color": ("#F9F9FA", "#2B2B2B"), # Light/Dark mode background colors
        "text": "#ecf0f1",
        "bg": "#2c3e50"
    },
    "Study": {
        "primary": "#2ecc71",      # Bright Green
        "secondary": "#27ae60",    # Darker Green
        "fg_color": ("#F9F9FA", "#243B34"),
        "text": "#ecf0f1",
        "bg": "#16a085"
    },
}

# --- Pomodoro Settings (in seconds) ---
POMODORO_SETTINGS = {
    "Short Break": 5 * 60,
    "Long Break": 15 * 60,
}

CUSTOM_POMODORO_DEFAULT_MINUTES = 25