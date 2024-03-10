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
        self.root = root
        root.title("CPU clock speed limiter")
        root.geometry("765x250")
        # root.resizable(False, False)
        
        main_frame = ttk.Frame(root)
        
        # Variables
        self.min_clock_speed = tk.DoubleVar(value=0.8)
        self.max_clock_speed = tk.DoubleVar(value=4.5)
        self.governor_policy = tk.StringVar(value="powersave")
        
        # Governor policy
        gov_frame = ttk.Frame(main_frame, padding=(5, 15, 100, 5))
        gov_label = ttk.Label(gov_frame, text="Set governor policy",
                              padding=(0, 0, 0, 5))
        gov_label["font"] = "Helvetica 14"
        powersave_policy = ttk.Radiobutton(gov_frame,
                                           text="Powersave",
                                           variable=self.governor_policy,
                                           value="powersave",
                                           command=self.set_governor)
        # powersave_policy.configure(style=)
        performance_policy = ttk.Radiobutton(gov_frame,
                                           text="Performance",
                                           variable=self.governor_policy,
                                           value="performance",
                                           command=self.set_governor)
        gov_label.grid(column=0, row=0, sticky="W")
        powersave_policy.grid(column=0, row=1)
        performance_policy.grid(column=0, row=2)
        gov_frame.grid(column=0, row=3)
        
        
        # Sliders
        sliders_frame = ttk.Frame(main_frame, padding=5)
        sliders_label = ttk.Label(sliders_frame, 
                                  text="Set clock speed scale",
                                  padding=(0, 0, 0, 5))
        sliders_label["font"] = "Helvetica 14"
        
        min_speed_label = ttk.Label(sliders_frame,
                                    text="Min speed")
        min_speed_slider = ttk.Scale(master=sliders_frame,
                                    length=175,
                                    from_=0.8,
                                    to=4.5,
                                    variable=self.min_clock_speed,
                                    command=self.set_min_speed)
        min_speed_value = ttk.Label(sliders_frame, 
                                    # text=f"{self.set_min_speed('value')}",
                                    textvariable=self.min_clock_speed)
        
        max_speed_label = ttk.Label(sliders_frame,
                                    text="Max speed")
        max_speed_slider = ttk.Scale(master=sliders_frame,
                                    length=175,
                                    from_=0.8,
                                    to=4.5,
                                    variable=self.max_clock_speed,
                                    command=self.set_max_speed)
        max_speed_value = ttk.Label(sliders_frame, 
                                    # text=f"{self.set_min_speed('value')}",
                                    textvariable=self.max_clock_speed)
        
        sliders_label.grid(column=0, row=0, columnspan=3, sticky="w")
        min_speed_label.grid(column=0, row=1, padx=5)
        min_speed_slider.grid(column=1, row=1, pady=5)
        min_speed_value.grid(column=2, row=1, pady=5)
        max_speed_label.grid(column=0, row=2, padx=5)
        max_speed_slider.grid(column=1, row=2, pady=5)
        max_speed_value.grid(column=2, row=2, pady=5)
        
        # Confirm button
        confirm_frame = ttk.Frame(main_frame)
        confirm_button = ttk.Button(master=confirm_frame, 
                                    text="Confirm",
                                    command=self.validate_settings)
        confirm_button.pack()
        
        # Output Label Frame
        output_frame = ttk.Labelframe(main_frame, text="Terminal Output",
                                      width=400, height=200)
        
        # Main Grid layout
        main_frame.grid(column=0, row=0)
        gov_frame.grid(column=0, row=0)
        sliders_frame.grid(column=0, row=1)
        output_frame.grid(column=1, row=0, rowspan=2,padx=15, sticky="E")
        confirm_frame.grid(column=0, row=2, columnspan=2, pady=15)
        
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
        print(max_speed)
        return max_speed
        
    # Provisoire
    def validate_settings(self):
        governor_policy = self.set_governor()
        min_speed = self.set_min_speed()
        max_speed = self.set_max_speed()   
        print(f"Current speed scale is: {min_speed}<-->{max_speed}\n"
              f"Current governor policy is: {governor_policy}")
    
    def round_min_value(self):
        min_value = self.min_clock_speed.get()
        round_min_value = round(min_value, 1)
        return round_min_value


def main():
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()