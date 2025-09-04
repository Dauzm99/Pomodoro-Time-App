# app/ui/analytics_frame.py
import customtkinter as ctk
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
from config import settings # <<< THIS LINE WAS MISSING

# Define a consistent dark background color for charts
CHART_BG_COLOR = "#2B2B2B" 
CHART_FACE_COLOR = "#343638"
CHART_TEXT_COLOR = "#FFFFFF"

class AnalyticsFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self._setup_widgets()

    def _setup_widgets(self):
        self.title_label = ctk.CTkLabel(self, text="Analytics Dashboard", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        self.chart_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.chart_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.chart_frame.grid_columnconfigure((0, 1), weight=1)
        self.chart_frame.grid_rowconfigure(0, weight=1)

        self.summary_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14))
        self.summary_label.grid(row=2, column=0, padx=20, pady=20, sticky="w")

    def create_charts(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        try:
            if 'logs_df' not in self.controller.app_data or not self.controller.app_data['logs_df']:
                raise ValueError("No data to display.")
            
            df = pd.DataFrame(self.controller.app_data['logs_df'])
            if df.empty:
                raise ValueError("No data to display.")

            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            mode_data = df.groupby('mode')['duration_sec'].sum()
            if not mode_data.empty:
                self.pie_chart_canvas = self._create_pie_chart(mode_data)
                self.pie_chart_canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

            task_data = df.groupby('label')['duration_sec'].sum() / 60
            if not task_data.empty:
                self.bar_chart_canvas = self._create_bar_chart(task_data)
                self.bar_chart_canvas.get_tk_widget().grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

            self._generate_summary(df)

        except Exception as e:
            no_data_label = ctk.CTkLabel(self.chart_frame, text=f"{e}\nComplete a session to see analytics.", font=ctk.CTkFont(size=16))
            no_data_label.grid(row=0, column=0, columnspan=2, padx=20, pady=20)
            self.summary_label.configure(text="")

    def _create_pie_chart(self, data):
        fig = Figure(figsize=(5, 4), dpi=100, facecolor=CHART_BG_COLOR)
        ax = fig.add_subplot(111)
        pie_colors = [settings.THEMES[mode]['primary'] for mode in data.index if mode in settings.THEMES]
        
        ax.pie(data, labels=data.index, autopct='%1.1f%%', startangle=140,
               colors=pie_colors,
               textprops={'color': CHART_TEXT_COLOR, 'weight': 'bold'})
        ax.set_title("Work vs. Study Time", color=CHART_TEXT_COLOR)
        fig.tight_layout()
        return FigureCanvasTkAgg(fig, master=self.chart_frame)

    def _create_bar_chart(self, data):
        fig = Figure(figsize=(6, 4), dpi=100, facecolor=CHART_BG_COLOR)
        ax = fig.add_subplot(111)
        
        current_theme_color = self.controller.theme['primary']
        data.plot(kind='barh', ax=ax, color=current_theme_color)
        
        ax.set_title("Time per Task (Minutes)", color=CHART_TEXT_COLOR)
        ax.tick_params(axis='x', colors=CHART_TEXT_COLOR)
        ax.tick_params(axis='y', colors=CHART_TEXT_COLOR)
        ax.set_facecolor(CHART_FACE_COLOR)
        ax.spines['top'].set_color(CHART_TEXT_COLOR)
        ax.spines['bottom'].set_color(CHART_TEXT_COLOR)
        ax.spines['left'].set_color(CHART_TEXT_COLOR)
        ax.spines['right'].set_color(CHART_TEXT_COLOR)
        fig.tight_layout()
        return FigureCanvasTkAgg(fig, master=self.chart_frame)

    def _generate_summary(self, df):
        now = datetime.now()
        start_of_this_week = now - timedelta(days=now.weekday())
        start_of_last_week = start_of_this_week - timedelta(days=7)

        this_week_df = df[df['timestamp'] >= start_of_this_week]
        last_week_df = df[(df['timestamp'] >= start_of_last_week) & (df['timestamp'] < start_of_this_week)]

        study_time_this_week = this_week_df[this_week_df['mode'] == 'Study']['duration_sec'].sum()
        study_time_last_week = last_week_df[last_week_df['mode'] == 'Study']['duration_sec'].sum()

        summary_text = "💡 Keep up the great work logging your sessions!"
        if study_time_last_week > 0 and study_time_this_week < study_time_last_week:
            percent_less = (1 - (study_time_this_week / study_time_last_week)) * 100
            summary_text = f"💡 Suggestion: You studied {percent_less:.0f}% less than last week. Want to review?"

        self.summary_label.configure(text=summary_text)

    def update_theme(self):
        theme = self.controller.theme
        self.title_label.configure(text_color=theme["primary"])
        
    def on_show(self):
        self.update_theme()
        self.create_charts()