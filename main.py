import subprocess
import tkinter as tk
from tkinter import ttk
from ttkwidgets import TickScale


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
        gov_label = ttk.Label(
            gov_frame, text="Set governor policy", padding=(0, 0, 0, 5)
        )
        gov_label["font"] = "Helvetica 14"
        powersave_policy = ttk.Radiobutton(
            gov_frame,
            text="Powersave",
            variable=self.governor_policy,
            value="powersave",
        )
        # powersave_policy.configure(style=)
        performance_policy = ttk.Radiobutton(
            gov_frame,
            text="Performance",
            variable=self.governor_policy,
            value="performance",
        )
        gov_label.grid(column=0, row=0, sticky="W")
        powersave_policy.grid(column=0, row=1)
        performance_policy.grid(column=0, row=2)
        gov_frame.grid(column=0, row=3)

        # Sliders
        sliders_frame = ttk.Frame(main_frame, padding=5)
        sliders_label = ttk.Label(
            sliders_frame,
            text="Set clock speed scale (GHz)",
            padding=(0, 0, 0, 5),
        )
        sliders_label["font"] = "Helvetica 14"

        min_speed_label = ttk.Label(sliders_frame, text="Min speed")
        min_speed_slider = TickScale(
            master=sliders_frame,
            length=175,
            from_=0.8,
            to=4.5,
            digits=1,
            variable=self.min_clock_speed,
        )

        max_speed_label = ttk.Label(sliders_frame, text="Max speed")
        max_speed_slider = TickScale(
            master=sliders_frame,
            length=175,
            from_=0.8,
            to=4.5,
            digits=1,
            variable=self.max_clock_speed,
        )

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
            command=self.set_governor,
        )
        confirm_speed_button = ttk.Button(
            master=confirm_frame, text="Confirm speed", command=self.set_speeds
        )
        confirm_all_button = ttk.Button(
            master=confirm_frame, text="Confirm all", command=self.set_all
        )

        confirm_governor_button.grid(column=0, row=0, padx=5)
        confirm_speed_button.grid(column=1, row=0, padx=5)
        confirm_all_button.grid(column=0, row=1, columnspan=2, pady=5)

        # Output Label Frame
        output_frame = ttk.Labelframe(
            main_frame,
            text="Terminal Output",
            width=470,
            height=260,
            padding=(5),
        )
        self.terminal_text = tk.Text(
            output_frame, state="normal", width=65, height=14
        )
        scrollbar = ttk.Scrollbar(
            output_frame, orient="vertical", command=self.terminal_text.yview
        )

        self.terminal_text.configure(yscrollcommand=scrollbar.set)
        self.terminal_text.grid(column=0, row=0, sticky="NES")
        scrollbar.grid(column=1, row=0, sticky="NS")

        # Main Grid layout
        main_frame.grid(column=0, row=0)
        gov_frame.grid(column=0, row=0)
        sliders_frame.grid(column=0, row=1)
        output_frame.grid(
            column=1, row=0, rowspan=3, padx=15, pady=5, sticky="NE"
        )
        confirm_frame.grid(column=0, row=2, columnspan=1, pady=10)

    def set_governor(self):
        governor_policy = self.governor_policy.get()
        command = [
            "pkexec",
            "cpupower",
            "frequency-set",
            "-g",
            governor_policy,
        ]
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output, error = process.communicate()
        output = output.decode()
        error = error.decode()

        freq_info_output, freq_info_error = self.frequency_info()

        message = OutputMessage(
            governor_policy=governor_policy,
            governor_output=output,
            governor_error=error,
            freq_info_output=freq_info_output,
            freq_info_error=freq_info_error,
        ).construct_message()

        self.write_output(message)

    def set_speeds(self):
        min_speed = self.min_clock_speed.get()
        min_speed = round(min_speed, 1)
        max_speed = self.max_clock_speed.get()
        max_speed = round(max_speed, 1)

        command = [
            "pkexec",
            "cpupower",
            "frequency-set",
            "-d",
            f"{min_speed}Ghz",
            "-u",
            f"{max_speed}Ghz",
        ]
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output, error = process.communicate()
        output = output.decode()
        error = error.decode()
        
        freq_info_output, freq_info_error = self.frequency_info()

        message = OutputMessage(
            min_speed=min_speed,
            max_speed=max_speed,
            speed_output=output,
            speed_error=error,
            freq_info_output=freq_info_output,
            freq_info_error=freq_info_error,
        ).construct_message()

        self.write_output(message)

    def set_all(self):
        governor_policy = self.governor_policy.get()
        min_speed = self.min_clock_speed.get()
        min_speed = round(min_speed, 1)
        max_speed = self.max_clock_speed.get()
        max_speed = round(max_speed, 1)
        command = [
            "pkexec",
            "cpupower",
            "frequency-set",
            "-g",
            f"{governor_policy}",
            "-d",
            f"{min_speed}Ghz",
            "-u",
            f"{max_speed}Ghz",
        ]
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output, error = process.communicate()
        output = output.decode()
        error = error.decode()

        freq_info_output, freq_info_error = self.frequency_info()

        message = OutputMessage(
            governor_policy=governor_policy,
            min_speed=min_speed,
            max_speed=max_speed,
            all_output=output,
            all_error=error,
            freq_info_output=freq_info_output,
            freq_info_error=freq_info_error,
        ).construct_message()

        self.write_output(message)

    def frequency_info(self):
        command = ["cpupower", "frequency-info"]
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output, error = process.communicate()
        freq_info_output = output.decode()
        freq_info_output = freq_info_output.replace("Ã©", "é")
        freq_info_output = freq_info_output.replace("Ãª", "ê")
        freq_info_error = error.decode()
        return (freq_info_output, freq_info_error)

    def write_output(self, message):
        if self.terminal_text.get("1.0", "end"):
            self.terminal_text.replace("1.0", "end", chars=message)
        else:
            self.terminal_text.insert("1.0", message)


class OutputMessage:
    def __init__(self, **kwargs):
        self.governor_policy = kwargs.get("governor_policy", None)
        self.min_speed = kwargs.get("min_speed", None)
        self.max_speed = kwargs.get("max_speed", None)
        self.governor_output = kwargs.get("governor_output", None)
        self.governor_error = kwargs.get("governor_error", None)
        self.speed_output = kwargs.get("speed_output", None)
        self.speed_error = kwargs.get("speed_error", None)
        self.all_output = kwargs.get("all_output", None)
        self.all_error = kwargs.get("all_error", None)
        self.freq_info_output = kwargs.get("freq_info_output", None)
        self.freq_info_error = kwargs.get("freq_info_error", None)

    def construct_message(self):
        gov_msg = ""
        speed_msg = ""
        all_msg = ""

        if self.governor_output or self.governor_error:
            if self.governor_error:
                gov_msg = (
                    f"Error (set governor policy):\n"
                    f"{self.governor_error}\n\n"
                )
            else:
                gov_msg = (
                    f"Governor policy is now set to: "
                    f"{self.governor_policy}\n"
                    f"Command output:\n{self.governor_output}\n\n"
                    f"Frequency information:\n{self.freq_info_output}"
                )

        if self.speed_output or self.speed_error:
            if self.speed_error:
                speed_msg = f"Error (set clock speed):\n{self.speed_error}\n"
            else:
                speed_msg = (
                    f"Clock speed scale is now set from "
                    f"{self.min_speed}GHz to {self.max_speed}GHz\n"
                    f"Command output:\n{self.speed_output}\n\n"
                    f"Frequency information:\n{self.freq_info_output}"
                )

        if self.all_output or self.all_error:
            if self.all_error:
                all_msg = f"Error:\n{self.all_error}"
            else:
                all_msg = (
                    f"Governor policy is now set to: "
                    f"{self.governor_policy}\n"
                    f"Clock speed scale is now set from "
                    f"{self.min_speed}GHz to {self.max_speed}GHz\n"
                    f"Command output:\n{self.all_output}\n\n"
                    f"Frequency information:\n{self.freq_info_output}"
                )

        message = f"{gov_msg}{speed_msg}{all_msg}"
        return message


def main():
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
