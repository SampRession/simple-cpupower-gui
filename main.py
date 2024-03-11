import subprocess
import tkinter as tk
from tkinter import ttk
from ttkwidgets import TickScale

# FIXME: make command asks password only once 
 

class MainWindow:
    def __init__(self, root):
        self.root = root
        root.title("CPU clock speed limiter")
        root.geometry("765x290")
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
        
        # Confirm buttons
        confirm_frame = ttk.Frame(main_frame)
        confirm_governor_button = ttk.Button(
            master=confirm_frame,
            text="Confirm governor",
            command=lambda: self.validate_settings("gov")
        )
        confirm_speed_button = ttk.Button(
            master=confirm_frame,
            text="Confirm speed",
            command=lambda: self.validate_settings("speed")
        )
        confirm_all_button = ttk.Button(
            master=confirm_frame, 
            text="Confirm",
            command=lambda: self.validate_settings("all")
        )
        
        confirm_governor_button.grid(column=0, row=0, padx=5)
        confirm_speed_button.grid(column=1, row=0, padx=5)
        confirm_all_button.grid(column=0, row=1, columnspan=2, pady=5)
        
        # Output Label Frame
        output_frame = ttk.Labelframe(main_frame, text="Terminal Output",
                                      width=470, height=260, padding=(5))
        self.terminal_text = tk.Text(output_frame, state="normal", 
                                width=65, height=14)
        scrollbar = ttk.Scrollbar(output_frame, orient="vertical",
                                  command=self.terminal_text.yview)
        
        self.terminal_text.configure(yscrollcommand=scrollbar.set)
        self.terminal_text.grid(column=0, row=0, sticky="NES")
        scrollbar.grid(column=1, row=0, sticky="NS")
        
        
        # Main Grid layout
        main_frame.grid(column=0, row=0)
        gov_frame.grid(column=0, row=0)
        sliders_frame.grid(column=0, row=1)
        output_frame.grid(column=1, row=0, rowspan=3, padx=15, pady=5, 
                          sticky="NE")
        confirm_frame.grid(column=0, row=2, columnspan=1, pady=10)
        
    def set_governor(self):
        governor_policy = self.governor_policy.get()
        command = ["pkexec", "cpupower", "frequency-set", "-g", 
                   governor_policy]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)
        output, error = process.communicate()
        output = output.decode()
        error = error.decode()
        return output, error
        
    def set_min_speed(self):
        min_speed = self.min_clock_speed.get()
        min_speed = round(min_speed, 1)
        command = ["pkexec", "cpupower", "frequency-set", 
                   "-d", f"{min_speed}Ghz"]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)
        output, error = process.communicate()
        output = output.decode()
        error = error.decode()
        return output, error
    
    def set_max_speed(self):
        max_speed = self.max_clock_speed.get()
        max_speed = round(max_speed, 1)
        command = ["pkexec", "cpupower", "frequency-set", 
                   "-u", f"{max_speed}Ghz"]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)
        output, error = process.communicate()
        output = output.decode()
        error = error.decode()
        return output, error

    def validate_settings(self, button_id):
        gov_policy = self.governor_policy.get().title()
        min_speed = round(self.min_clock_speed.get(), 1)
        max_speed = round(self.max_clock_speed.get(), 1)
        
        if button_id == "all":
            gov_output, gov_error = self.set_governor()
            min_output, min_error = self.set_min_speed()
            max_output, max_error = self.set_max_speed()  
            message = OutputMessage(gov_policy=gov_policy,
                                    min_speed=min_speed,
                                    max_speed=max_speed,
                                    gov_output=gov_output, 
                                    gov_error=gov_error,
                                    min_output=min_output,
                                    min_error=min_error,
                                    max_output=max_output,
                                    max_error=max_error).construct_message()
        elif button_id=="speed":
            min_output, min_error = self.set_min_speed()
            max_output, max_error = self.set_max_speed() 
            message = OutputMessage(min_speed=min_speed,
                                    max_speed=max_speed,
                                    min_output=min_output,
                                    min_error=min_error,
                                    max_output=max_output,
                                    max_error=max_error).construct_message()
        else:
            gov_output, gov_error = self.set_governor()
            message = OutputMessage(gov_policy=gov_policy,
                                    gov_output=gov_output, 
                                    gov_error=gov_error).construct_message()
        
        if self.terminal_text.get("1.0", "end"):
            self.terminal_text.replace("1.0", "end", chars=message)
        else:
            self.terminal_text.insert("1.0", message)


class OutputMessage():
    def __init__(self, **kwargs):
        self.gov_policy = kwargs.get("gov_policy", None)
        self.min_speed = kwargs.get("min_speed", None)
        self.max_speed = kwargs.get("max_speed", None)
        self.gov_output = kwargs.get("gov_output", None)
        self.gov_error = kwargs.get("gov_error", None)
        self.min_output = kwargs.get("min_output", None)
        self.min_error = kwargs.get("min_error", None)
        self.max_output = kwargs.get("max_output", None)
        self.max_error = kwargs.get("max_error", None)
    
    def construct_message(self):
        gov_msg = ""
        min_msg = ""
        max_msg = ""
        
        if self.gov_output or self.gov_error:
            if self.gov_error:
                gov_msg = f"Error (set governor policy):\n{self.gov_error}\n\n"
            else:
                gov_msg = (
            f"Governor policy is now set to: "
            f"{self.gov_policy}\n"
            f"Command output:\n{self.gov_output}\n\n"
            )

        if self.min_output or self.min_error:
            if self.min_error:
                min_msg = f"Error (set min clock speed):\n{self.min_error}\n"
            else:
                min_msg = (
            f"Minimum clock speed is now set to: "
            f"{self.min_speed}GHz\n"
            f"Command output:\n{self.min_output}\n"
            )

        if self.max_output or self.max_error:
            if self.max_error:
                max_msg = f"Error (set max clock speed):\n{self.max_error}"
            else:
                max_msg = (
            f"Maximum clock speed is now set to: "
            f"{self.max_speed}GHz\n"
            f"Command output:\n{self.max_output}"
            )
        
        message = f"{gov_msg}{min_msg}{max_msg}"
        return message
        

def main():
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()
    