import tkinter as tk
from tkinter import ttk
import threading
import time

class VariableMonitorApp:
    def __init__(self, master):
        self.master = master
        master.title("Variable Monitor")

        self.my_variable = 0  # The variable to monitor

        # Label to display the variable's value
        self.variable_label = ttk.Label(master, text=f"Current Value: {self.my_variable}")
        self.variable_label.pack(pady=10)

        # Button to increment the variable
        self.increment_button = ttk.Button(master, text="Increment", command=self.increment_variable)
        self.increment_button.pack(pady=5)

        # Start a thread to update the label periodically
        self.update_thread = threading.Thread(target=self.update_label_periodically)
        self.update_thread.daemon = True  # Allow the thread to exit when the main program exits
        self.update_thread.start()

    def increment_variable(self):
        self.my_variable += 1
        # No direct update to label here, as the separate thread handles it

    def update_label_periodically(self):
        while True:
            # Update the label text with the current value of my_variable
            self.variable_label.config(text=f"Current Value: {self.my_variable}")
            time.sleep(0.5)  # Update every 0.5 seconds

if __name__ == "__main__":
    root = tk.Tk()
    app = VariableMonitorApp(root)
    root.mainloop()