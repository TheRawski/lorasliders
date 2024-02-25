import tkinter as tk
from tkinter import ttk
import customtkinter
import re
import tkinter.messagebox as messagebox
import pyperclip

class StringAdjusterApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Lora Sliders")
        self.master.geometry("1080x720")

        self.original_text_var = tk.StringVar()
        self.original_text_var.set("<lora:test_v1:0.5> test, example\n<lora:test_v2:0.8> test, example")

        # Entry widgets for slider range
        self.min_range_var = tk.DoubleVar(value=0.0)
        self.max_range_var = tk.DoubleVar(value=1.0)

        self.current_values = {}  # Store current values for sliders
        self.sliders = {}  # Store slider widgets
        self.labels = {}  # Store label widgets
        self.value_labels = {}  # Store labels to display slider values

        self.initialize_ui()

    def initialize_ui(self):

        # Text box for the original text
        text_label = customtkinter.CTkLabel(self.master, text="<LORA SLIDERS>", font=customtkinter.CTkFont(family="Courier", size=20, weight="bold"))
        text_label.grid(row=0, column=0, columnspan=10, pady=5, padx=10, sticky="nwe")

        self.text_box = customtkinter.CTkTextbox(self.master, height=150, width=900)
        self.text_box.insert(tk.END, self.original_text_var.get())
        self.text_box.grid(row=1, column=0, columnspan=10, rowspan=3, pady=5, padx=10, sticky="nsew")
        self.text_box.configure(wrap="word")

        # Button to paste from clipboard
        paste_button = customtkinter.CTkButton(self.master, text="Paste from Clipboard", command=self.paste_from_clipboard, font=customtkinter.CTkFont(weight="bold"))
        paste_button.grid(row=1, column=11, pady=5, padx=10, sticky="w")

        # Button to copy to clipboard
        copy_button = customtkinter.CTkButton(self.master, text="Copy to Clipboard", command=self.copy_to_clipboard, font=customtkinter.CTkFont(weight="bold"))
        copy_button.grid(row=2, column=11, pady=5, padx=10, sticky="w")

        # Entry widgets for slider range
        min_range_label = customtkinter.CTkLabel(self.master, text="Range:")
        min_range_label.grid(row=4, column=0, pady=5, padx=10, sticky="w")
        min_range_entry = customtkinter.CTkEntry(self.master, textvariable=self.min_range_var, validate="key", validatecommand=(self.validate, '%P'), width=40)
        min_range_entry.grid(row=4, column=1, pady=5, padx=10, sticky="w")

        max_range_label = customtkinter.CTkLabel(self.master, text="---")
        max_range_label.grid(row=4, column=2, pady=5, padx=10, sticky="w")
        max_range_entry = customtkinter.CTkEntry(self.master, textvariable=self.max_range_var, validate="key", validatecommand=(self.validate, '%P'), width=40)
        max_range_entry.grid(row=4, column=3, pady=5, padx=10, sticky="w")

        # Button to update sliders
        update_button = customtkinter.CTkButton(self.master, text="Update Sliders", command=self.initialize_sliders)
        update_button.grid(row=4, column=5, pady=5, padx=10, sticky="w")

        # Initialize sliders based on original text
        self.initialize_sliders()


    def validate(self, new_value):
        try:
            float(new_value)
            return True
        except ValueError:
            return False


    def initialize_sliders(self):
        # Clear existing sliders and labels
        for slider in self.sliders.values():
            slider.destroy()

        for label in self.labels.values():
            label.destroy()

        for value_label in self.value_labels.values():
            value_label.destroy()

        self.sliders = {}
        self.labels = {}
        self.current_values = {}
        self.value_labels = {}

        # Find instances of <lora:example_v2:1> in the text
        #matches = re.findall(r'<lora:\w+:\d+\.?\d*>', self.text_box.get(1.0, tk.END)) did not account for hypens, below fixes issue
        matches = re.findall(r'<lora:[\w\-]+:\d+\.?\d*>', self.text_box.get(1.0, tk.END))

        # Create sliders and labels for each match
        for index, match in enumerate(matches):
            parts = match.split(":")
            name = parts[1]  # Extract the name from the match

            label = customtkinter.CTkLabel(self.master, text=f"{name}:")
            label.grid(row=index + 8, column=0, pady=5, padx=10, sticky="w")
            self.labels[name] = label  # Store the label for association

            current_value = float(parts[-1][:-1]) if '.' in parts[-1] else int(parts[-1][:-1])
            value = tk.DoubleVar(value=current_value)
            self.current_values[name] = value

            slider = customtkinter.CTkSlider(self.master, from_=self.min_range_var.get(), to=self.max_range_var.get(), orientation="horizontal", variable=value,
                               command=lambda val, name=name: self.update_text(name))
            slider.set(current_value)
            slider.grid(row=index + 8, column=1, columnspan=2, pady=5, padx=10, sticky="w")
            self.sliders[name] = slider  # Store the slider for association

            value_label = customtkinter.CTkLabel(self.master, text=f"{value.get():.2f}")
            value_label.grid(row=index + 8, column=3, pady=5, padx=10, sticky="w")
            self.value_labels[name] = value_label  # Store the label for association

    def update_text(self, name):
        # Update the text box with the adjusted values from sliders
        adjusted_text = self.text_box.get(1.0, tk.END).strip()

        for slider_name, value in self.current_values.items():
            # The pattern to match in the text box
            pattern = f'<lora:{slider_name}:[\d\.]+>'

            # Format the value based on whether it's a whole number or not
            formatted_value = int(value.get()) if value.get().is_integer() else round(value.get(), 2)

            # Replace the pattern with the updated value
            adjusted_text = re.sub(pattern, f'<lora:{slider_name}:{formatted_value}>', adjusted_text)

            # Update the value label
            self.value_labels[slider_name].configure(text=f"{formatted_value:.2f}")

        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(tk.END, adjusted_text)

    def paste_from_clipboard(self):
        # Paste text from clipboard to text box
        try:
            text = pyperclip.paste()
            if text:
                self.text_box.delete(1.0, tk.END)
                self.text_box.insert(tk.END, text)
                # Update sliders based on the new text
                self.initialize_sliders()
        except Exception as e:
            messagebox.showerror("Error", f"Error pasting from clipboard: {e}")

    def copy_to_clipboard(self):
        adjusted_text = self.text_box.get(1.0, tk.END).strip()
        pyperclip.copy(adjusted_text)

if __name__ == "__main__":
    customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
    root = customtkinter.CTk()
    app = StringAdjusterApp(root)
    root.mainloop()
