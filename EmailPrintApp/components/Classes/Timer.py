import tkinter as tk
import time

#_________________________________________________________ Timer Widget _________________________________________________________ #

class Timer:
    '''
    Crates a Timer used for the program's main script. Uses dynamic tkinter label.
    '''
    def __init__(self, parent_frame: tk.Frame) -> None:
        
        self.parent_frame = parent_frame
        self.timer_label = tk.Label(parent_frame, font=('calibri', 40, 'bold'), background='purple', foreground='white')
        self.timer_label.pack()
        
        self.start_time = None
        self.running = False

    def update_timer(self) -> None:

        if self.running:
            elapsed_time = int(time.time() - self.start_time)
            hours, remainder = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.timer_label.config(text=f'{hours:04}:{minutes:02}:{seconds:02}')
            self.parent_frame.after(1000, self.update_timer)  # Update every second (1000ms)

    def start_timer(self) -> None:

        if not self.running:
            self.start_time = time.time()
            self.running = True
            self.update_timer()

    def stop_timer(self) -> None:

        if self.running:
            self.running = False

    def reset_timer(self) -> None:

        self.stop_timer()
        self.start_time = None
        self.timer_label.config(text='00:00:00')
