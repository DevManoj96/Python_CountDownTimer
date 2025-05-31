import tkinter as tk
from tkinter import messagebox


class CountdownTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("--- Python CountDown Timer ---")
        self.root.geometry('640x480')

        self.total_seconds = 0
        self.remaining_seconds = 0
        self.running = False
        self.timer_job = None
        self.is_dark = False

        self.menubar = tk.Menu(root)
        self.root.config(menu=self.menubar)

        self.options_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Options", menu=self.options_menu)
        self.options_menu.add_command(label="Toggle Theme", command=self.toggle_theme)

        self.input_frame = tk.Frame(root)
        self.input_frame.pack(pady=20)

        self.heading1 = tk.Label(self.input_frame, text="Set Timer:", font=("Arial", 12))
        self.heading1.pack()

        self.time_frame = tk.Frame(self.input_frame)
        self.time_frame.pack(pady=10)

        self.hours_label = tk.Label(self.time_frame, text="Hours: ")
        self.hours_label.grid(row=0, column=0, padx=5)

        self.hours_var = tk.StringVar(value="0")
        self.hours_entry = tk.Entry(self.time_frame, textvariable=self.hours_var, width=5)
        self.hours_entry.grid(row=0, column=1, padx=5)

        self.minutes_label = tk.Label(self.time_frame, text="Minutes: ")
        self.minutes_label.grid(row=0, column=2, padx=5)

        self.minutes_var = tk.StringVar(value="5")
        self.minutes_entry = tk.Entry(self.time_frame, textvariable=self.minutes_var, width=5)
        self.minutes_entry.grid(row=0, column=3, padx=5)

        self.seconds_label = tk.Label(self.time_frame, text="Seconds: ")
        self.seconds_label.grid(row=0, column=4, padx=5)

        self.seconds_var = tk.StringVar(value="0")
        self.seconds_entry = tk.Entry(self.time_frame, textvariable=self.seconds_var, width=5)
        self.seconds_entry.grid(row=0, column=5, padx=5)

        self.time_label = tk.Label(root, text="00:05:00", font=("Arial", 24, "bold"))
        self.time_label.pack(pady=10)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        self.set_timer_button = tk.Button(self.button_frame, text="Set Timer", command=self.set_timer)
        self.set_timer_button.pack(side=tk.LEFT, padx=5)

        self.start_button = tk.Button(self.button_frame, text="Start", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = tk.Button(self.button_frame, text="Pause", command=self.pause_timer)
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(self.button_frame, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        self.exit_button = tk.Button(self.button_frame, text="Exit", command=self.root.quit)
        self.exit_button.pack(pady=5)

        self.set_timer()

    def toggle_theme(self):
        if not self.is_dark:
            # Switch to dark theme
            bg_color = "#222222"
            fg_color = "white"
            entry_bg = "#333333"
            entry_fg = "white"
            button_bg = "#444444"
            button_fg = "white"
        else:
            # Switch to light theme
            bg_color = "white"
            fg_color = "black"
            entry_bg = "white"
            entry_fg = "black"
            button_bg = "#f0f0f0"
            button_fg = "black"

        # Update root window
        self.root.configure(bg=bg_color)
        
        # Update frames
        frames = [self.input_frame, self.time_frame, self.button_frame]
        for frame in frames:
            frame.configure(bg=bg_color)

        # Update labels
        labels = [self.heading1, self.hours_label, self.minutes_label, 
                 self.seconds_label, self.time_label]
        for label in labels:
            label.configure(bg=bg_color, fg=fg_color)

        # Update entry widgets
        entries = [self.hours_entry, self.minutes_entry, self.seconds_entry]
        for entry in entries:
            entry.configure(bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)

        # Update buttons
        buttons = [self.set_timer_button, self.start_button, self.pause_button,
                  self.reset_button, self.exit_button]
        for button in buttons:
            button.configure(bg=button_bg, fg=button_fg, activebackground=bg_color)

        self.is_dark = not self.is_dark
        
   
        self.update_display()

    def set_timer(self):
        try:
            hours = int(self.hours_var.get() or 0)
            minutes = int(self.minutes_var.get() or 0)
            seconds = int(self.seconds_var.get() or 0)

            self.total_seconds = hours * 3600 + minutes * 60 + seconds
            self.remaining_seconds = self.total_seconds

            if self.total_seconds <= 0:
                messagebox.showerror("Error", "Please set a time greater than 0!")
                return

            self.update_display()
            self.running = False
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")

    def start_timer(self):
        if self.remaining_seconds > 0 and not self.running:
            self.running = True
            self.countdown()

    def pause_timer(self):
        self.running = False
        if self.timer_job:
            self.root.after_cancel(self.timer_job)

    def reset_timer(self):
        self.running = False
        if self.timer_job:
            self.root.after_cancel(self.timer_job)

        self.remaining_seconds = self.total_seconds
        self.update_display()

    def countdown(self):
        if self.running and self.remaining_seconds > 0:
            self.update_display()
            self.remaining_seconds -= 1
            self.timer_job = self.root.after(1000, self.countdown)
        elif self.remaining_seconds <= 0:
            self.running = False
            self.time_finished()

    def update_display(self):
        hours = self.remaining_seconds // 3600
        minutes = (self.remaining_seconds % 3600) // 60
        seconds = self.remaining_seconds % 60

        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.time_label.config(text=time_str)

        
        if self.remaining_seconds <= 10:
            color = "#ff4444" if self.is_dark else "red"
        elif self.remaining_seconds <= 60:
            color = "#ffaa00" if self.is_dark else "orange"
        else:
            color = "white" if self.is_dark else "black"
        
        self.time_label.config(fg=color)

    def time_finished(self):
        finish_color = "#ff4444" if self.is_dark else "red"
        self.time_label.config(text="00:00:00", fg=finish_color)
        messagebox.showinfo("Time's Up!", "The countdown timer has finished!")


if __name__ == '__main__':
    root = tk.Tk()
    app = CountdownTimer(root)
    root.mainloop()