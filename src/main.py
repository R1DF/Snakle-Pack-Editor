# Imports
from tkinter import Tk

# Application
class App(Tk):
    def __init__(self):
        # Initialization
        super().__init__()
        self.title("Pack Editor")
        self.geometry("400x500")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.handle_exit)

    def handle_exit(self):
        self.quit()

# Creating application
app = App()
app.mainloop()
