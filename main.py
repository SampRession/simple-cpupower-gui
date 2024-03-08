import tkinter as tk
from tkinter import ttk


class MainWindow:
    def __init__(self, root):
        root.title("CPU clock speed limiter")
        root.geometry("650x400")


def main():
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()