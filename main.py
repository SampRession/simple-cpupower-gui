import tkinter as tk
from tkinter import ttk

# TODO: input field to type a number between 6 and 45
# TODO: Button to validate
# TODO: launch script to set the maximum value (f-string) -> 
#           Command : sudo cpupower frequency-set -u 4.5GHz
#                     f"sudo cpupower frequency-set -u {max_freq}"
# TODO: success dialog (with returned line from terminal ?)


class MainWindow:
    def __init__(self, root):
        root.title("CPU clock speed limiter")
        root.geometry("650x400")
        root.resizable(False, False)
        
        main_frame = ttk.Frame(root)
        main_frame.pack()
        
        # Variables
        self.min_clock_speed = tk.DoubleVar(value=0.8)
        self.max_clock_speed = tk.DoubleVar(value=4.5)
        self.governor_policy = tk.StringVar(value="powersave")
        
        # Governor policy
        gov_frame = ttk.Frame(main_frame, padding=(5, 10))
        gov_label = ttk.Label(gov_frame, text="Set governor policy")
        gov_label.pack()
        powersave_policy = ttk.Radiobutton(gov_frame,
                                           text="Powersave",
                                           variable=self.governor_policy,
                                           value="powersave",
                                           command=self.set_governor)
        powersave_policy.pack()
        performance_policy = ttk.Radiobutton(gov_frame,
                                           text="Performance",
                                           variable=self.governor_policy,
                                           value="performance",
                                           command=self.set_governor)
        performance_policy.pack()
        gov_frame.pack()
        
        
        # Sliders
        sliders_frame = ttk.Frame(main_frame, padding=(5, 10))
        sliders_label = ttk.Label(sliders_frame, 
                                  text="Set minimum and maximum clock speed")
        sliders_label.pack()
        min_speed_scale = ttk.Scale(master=sliders_frame,
                                    length=200,
                                    from_=0.8,
                                    to=4.5,
                                    variable=self.min_clock_speed)
        min_speed_scale.pack()
        max_speed_scale = ttk.Scale(master=sliders_frame,
                                    length=200,
                                    from_=0.8,
                                    to=4.5,
                                    variable=self.max_clock_speed)
        sliders_frame.grid_columnconfigure()
        min_speed_scale.pack()
        max_speed_scale.pack()
        sliders_frame.pack()
        
        # Confirm button
        confirm_frame = ttk.Frame(main_frame, padding=(5, 10))
        confirm_button = ttk.Button(master=confirm_frame, 
                                    text="Confirm",
                                    command=self.validate_settings)
        confirm_button.pack()
        confirm_frame.pack()

    def set_governor(self):
        governor_policy = self.governor_policy.get()
        return governor_policy
        
    def set_min_speed(self):
        min_speed = self.min_clock_speed.get()
        min_speed = round(min_speed, 1)
        return min_speed
    
    def set_max_speed(self):
        max_speed = self.max_clock_speed.get()
        max_speed = round(max_speed, 1)
        return max_speed
        
    # Provisoire
    def validate_settings(self):
        governor_policy = self.set_governor()
        min_speed = self.set_min_speed()
        max_speed = self.set_max_speed()   
        print(f"Current speed scale is: {min_speed}<-->{max_speed}\n"
              f"Current governor policy is: {governor_policy}")
    


def main():
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()