import tkinter as tk
from tkinter import ttk
import re

class StringAdjusterApp:
    def __init__(self, master):
        self.master = master
        self.master.title("String Adjuster")

        self.original_text_var = tk.StringVar()
        self.original_text_var.set("<lora:test_v1:0.5> test, example\n<lora:test_v2:0.8> test, example")

        # Entry widgets for slider range
        self.min_range_var = tk.DoubleVar(value=0.0)
        self.max_range_var = tk.DoubleVar(value=2.0)

        self.current_values = {}  # Store current values for sliders
        self.sliders = {}  # Store slider widgets
        self.labels = {}  # Store label widgets

        self.initialize_ui()

    def initialize_ui(self):
        # Text box for the original text
        text_label = tk.Label(self.master, text="Prompt:")
        text_label.grid(row=0, column=0, pady=5, padx=10, sticky="w")

        self.text_box = tk.Text(self.master, height=10, width=50)
        self.text_box.insert(tk.END, self.original_text_var.get())
        self.text_box.grid(row=0, column=1, columnspan=3, pady=5, padx=10, sticky="w")

        # Entry widgets for slider range
        min_range_label = tk.Label(self.master, text="Min Range:")
        min_range_label.grid(row=1, column=0, pady=5, padx=10, sticky="w")
        min_range_entry = tk.Entry(self.master, textvariable=self.min_range_var)
        min_range_entry.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        max_range_label = tk.Label(self.master, text="Max Range:")
        max_range_label.grid(row=1, column=2, pady=5, padx=10, sticky="w")
        max_range_entry = tk.Entry(self.master, textvariable=self.max_range_var)
        max_range_entry.grid(row=1, column=3, pady=5, padx=10, sticky="w")

        # Button to update sliders
        update_button = tk.Button(self.master, text="Update Sliders", command=self.initialize_sliders)
        update_button.grid(row=2, column=0, pady=5, padx=10, sticky="w")

        # Initialize sliders based on original text
        self.initialize_sliders()

    def initialize_sliders(self):
        # Clear existing sliders and labels
        for slider in self.sliders.values():
            slider.destroy()

        for label in self.labels.values():
            label.destroy()

        self.sliders = {}
        self.labels = {}
        self.current_values = {}

        # Find instances of <lora:example_v2:1> in the text
        matches = re.findall(r'<lora:\w+:\d+\.?\d*>', self.text_box.get(1.0, tk.END))

        # Create sliders and labels for each match
        for index, match in enumerate(matches):
            parts = match.split(":")
            name = parts[1]  # Extract the name from the match

            label = tk.Label(self.master, text=f"{name}:")
            label.grid(row=index + 3, column=0, pady=5, padx=10, sticky="w")
            self.labels[name] = label  # Store the label for association

            current_value = float(parts[-1][:-1]) if '.' in parts[-1] else int(parts[-1][:-1])
            value = tk.DoubleVar(value=current_value)
            self.current_values[name] = value

            slider = ttk.Scale(self.master, from_=self.min_range_var.get(), to=self.max_range_var.get(), orient="horizontal", variable=value,
                               command=lambda val, name=name: self.update_text(name))
            slider.set(current_value)
            slider.grid(row=index + 3, column=1, columnspan=2, pady=5, padx=10, sticky="w")
            self.sliders[name] = slider  # Store the slider for association

    def update_text(self, name):
        # Update the text box with the adjusted values from sliders
        adjusted_text = self.text_box.get(1.0, tk.END)

        for slider_name, value in self.current_values.items():
            # The pattern to match in the text box
            pattern = f'<lora:{slider_name}:[\d\.]+>'

            # Format the value based on whether it's a whole number or not
            formatted_value = int(value.get()) if value.get().is_integer() else round(value.get(), 2)

            # Replace the pattern with the updated value
            adjusted_text = re.sub(pattern, f'<lora:{slider_name}:{formatted_value}>', adjusted_text)

        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(tk.END, adjusted_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = StringAdjusterApp(root)
    root.mainloop()
