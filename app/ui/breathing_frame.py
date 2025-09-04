# app/ui/breathing_frame.py
import customtkinter as ctk
import math

class BreathingToplevel(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x450")
        self.title("Breathing Exercise")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.animating = True
        self.radius = 50
        self.max_radius = 120
        self.min_radius = 40
        self.direction = 1  # 1 for expand, -1 for shrink
        
        self.instruction_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=24, weight="bold"))
        self.instruction_label.grid(row=0, column=0, pady=30)
        
        self.canvas = ctk.CTkCanvas(self, width=300, height=300, bg="#2B2B2B", highlightthickness=0)
        self.canvas.grid(row=1, column=0, pady=20)
        
        self.after(50, self.start_animation)

    def start_animation(self):
        self.animate()

    def animate(self):
        if not self.animating: return
        
        if self.direction == 1:
            self.instruction_label.configure(text="Breathe In...")
            self.radius += 0.5
            if self.radius >= self.max_radius:
                self.direction = -1
        else:
            self.instruction_label.configure(text="Breathe Out...")
            self.radius -= 0.5
            if self.radius <= self.min_radius:
                self.direction = 1
        
        self.draw_circle()
        self.after(25, self.animate)

    def draw_circle(self):
        self.canvas.delete("all")
        x0 = 150 - self.radius
        y0 = 150 - self.radius
        x1 = 150 + self.radius
        y1 = 150 + self.radius
        self.canvas.create_oval(x0, y0, x1, y1, fill="#3498db", outline="")
        
    def on_close(self):
        self.animating = False
        self.destroy()