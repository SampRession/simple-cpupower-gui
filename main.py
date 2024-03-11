import subprocess
import tkinter as tk
from tkinter import ttk
from ttkwidgets import TickScale


class MainWindow:
    def __init__(self, root):
        self.root = root
        root.title("CPU clock speed limiter")
        root.geometry("765x280")
        # root.resizable(False, False)
        
        main_frame = ttk.Frame(root)
        
        # Variables
        self.min_clock_speed = tk.DoubleVar(value=None)
        self.max_clock_speed = tk.DoubleVar(value=None)
        self.governor_policy = tk.StringVar(value=None)
        
        # Governor policy
        gov_frame = ttk.Frame(main_frame, padding=(5, 15, 100, 5))
        gov_label = ttk.Label(gov_frame, text="Set governor policy",
                              padding=(0, 0, 0, 5))
        gov_label["font"] = "Helvetica 14"
        powersave_policy = ttk.Radiobutton(gov_frame,
                                           text="Powersave",
                                           variable=self.governor_policy,
                                           value="powersave")
        # powersave_policy.configure(style=)
        performance_policy = ttk.Radiobutton(gov_frame,
                                           text="Performance",
                                           variable=self.governor_policy,
                                           value="performance")
        gov_label.grid(column=0, row=0, sticky="W")
        powersave_policy.grid(column=0, row=1)
        performance_policy.grid(column=0, row=2)
        gov_frame.grid(column=0, row=3)
        
        
        # Sliders
        sliders_frame = ttk.Frame(main_frame, padding=5)
        sliders_label = ttk.Label(sliders_frame, 
                                  text="Set clock speed scale (GHz)",
                                  padding=(0, 0, 0, 5))
        sliders_label["font"] = "Helvetica 14"
        
        min_speed_label = ttk.Label(sliders_frame,
                                    text="Min speed")
        min_speed_slider = TickScale(master=sliders_frame,
                                    length=175,
                                    from_=0.8,
                                    to=4.5,
                                    digits=1,
                                    variable=self.min_clock_speed)
        
        max_speed_label = ttk.Label(sliders_frame,
                                    text="Max speed")
        max_speed_slider = TickScale(master=sliders_frame,
                                    length=175,
                                    from_=0.8,
                                    to=4.5,
                                    digits=1,
                                    variable=self.max_clock_speed)
        
        sliders_label.grid(column=0, row=0, columnspan=3, sticky="w")
        min_speed_label.grid(column=0, row=1, padx=5)
        min_speed_slider.grid(column=1, row=1, pady=0)
        max_speed_label.grid(column=0, row=2, padx=5)
        max_speed_slider.grid(column=1, row=2, pady=0)
        
        # Confirm button
        confirm_frame = ttk.Frame(main_frame)
        confirm_button = ttk.Button(master=confirm_frame, 
                                    text="Confirm",
                                    command=self.validate_settings)
        confirm_button.pack(anchor="center")
        
        # Output Label Frame
        output_frame = ttk.Labelframe(main_frame, text="Terminal Output",
                                      width=470, height=260, padding=(5))
        self.terminal_text = tk.Text(output_frame, state="normal", 
                                width=65, height=12)
        self.terminal_text.pack()
        
        # Main Grid layout
        main_frame.grid(column=0, row=0)
        gov_frame.grid(column=0, row=0)
        sliders_frame.grid(column=0, row=1)
        output_frame.grid(column=1, row=0, rowspan=3, padx=15, sticky="E")
        confirm_frame.grid(column=0, row=2, columnspan=1, pady=15)
        
    def set_governor(self):
        governor_policy = self.governor_policy.get()
        command = ["cpupower", "frequency-set", "-g", governor_policy]
        # command = ["echo", f"governor: {governor_policy}"]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)
        output, error = process.communicate()
        output = output.decode()
        error = error.decode()
        return output, error
        
    def set_min_speed(self):
        min_speed = self.min_clock_speed.get()
        min_speed = round(min_speed, 1)
        command = ["echo", f"min speed: {min_speed}"]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)
        output, error = process.communicate()
        output = output.decode()
        error = error.decode()
        return output, error
    
    def set_max_speed(self):
        max_speed = self.max_clock_speed.get()
        max_speed = round(max_speed, 1)
        command = ["echo", f"max speed: {max_speed}"]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)
        output, error = process.communicate()
        output = output.decode()
        error = error.decode()
        return output, error

    def validate_settings(self):
        self.gov_output, self.gov_error = self.set_governor()
        self.min_output, self.min_error = self.set_min_speed()
        self.max_output, self.max_error = self.set_max_speed()  
        message = self.construct_message()
        if self.terminal_text.get("1.0", "end"):
            self.terminal_text.replace("1.0", "end", chars=message)
        else:
            self.terminal_text.insert("1.0", message)
            
    def construct_message(self):
        if self.gov_output or self.gov_error:
            if self.gov_error:
                gov_msg = f"Error (set governor policy):\n{self.gov_error}"
            else:
                gov_msg = (
            f"Governor policy is now set to: "
            f"{self.governor_policy.get().title()}"
            f"Command output:\n{self.gov_output}"
            )

        if self.min_output or self.min_error:
            if self.min_error:
                min_msg = f"Error (set min clock speed):\n{self.min_error}"
            else:
                min_msg = (
            f"Minimum clock speed is now set to: "
            f"{self.min_clock_speed.get()}GHz\n"
            f"Command output:\n{self.min_output}"
            )

        if self.max_output or self.max_error:
            if self.max_error:
                max_msg = f"Error (set max clock speed):\n{self.max_error}"
            else:
                max_msg = (
            f"Maximum clock speed is now set to: "
            f"{self.max_clock_speed.get()}GHz\n"
            f"Command output:\n{self.max_output}"
            )
        message = f"{gov_msg}\n\n{min_msg}\n\n{max_msg}"
        return message
        
            

def main():
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()