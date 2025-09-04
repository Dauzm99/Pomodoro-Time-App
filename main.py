# main.py
import matplotlib
matplotlib.use('TkAgg') # Add this line right at the top

from app.app_logic import TimeSplitApp

if __name__ == "__main__":
    app = TimeSplitApp()
    app.mainloop()