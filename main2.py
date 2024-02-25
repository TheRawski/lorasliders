import tkinter as tk
from tkinter import ttk
import re
import tkinter.messagebox as messagebox
import pyperclip


class StringAdjusterApp:
    def __init__(self, master):
        self.master = master
        self.master.title("String Adjuster")

        self.original_text_var = tk.StringVar()
        self.original_text_var.set("<lora:test_v1:0.5> test, example\n<lora:test_v2:0.8> test, example")

        self.current_values = []  # Store current values for sliders
        self.labels = []  # New variable to keep track of labels
        self.initialize_ui()

    def initialize_ui(self):
        # Text box for the original text
        text_label = tk.Label(self.master, text="Original Text:")
        text_label.grid(row=0, column=0, pady=5, padx=10, sticky="w")

        self.text_box = tk.Text(self.master, height=10, width=50)
        self.text_box.insert(tk.END, self.original_text_var.get())
        self.text_box.grid(row=0, column=1, columnspan=3, pady=5, padx=10, sticky="w")

        # Button to paste from clipboard
        paste_button = tk.Button(self.master, text="Paste from Clipboard", command=self.paste_from_clipboard)
        paste_button.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        # Button to copy to clipboard
        copy_button = tk.Button(self.master, text="Copy to Clipboard", command=self.copy_to_clipboard)
        copy_button.grid(row=1, column=2, pady=5, padx=10, sticky="w")

        # Button to update sliders
        update_button = tk.Button(self.master, text="Update Sliders", command=self.initialize_sliders)
        update_button.grid(row=1, column=3, pady=5, padx=10, sticky="w")

        # Initialize sliders based on original text
        self.initialize_sliders()

    def initialize_sliders(self):
        # Remove existing sliders and labels
        for label in self.labels:
            label.destroy()
        self.labels = []  # Clear the labels list

        # Find instances of <lora:example_v2:1> in the text
        matches = re.findall(r'<lora:\w+:\d+\.\d+>', self.text_box.get(1.0, tk.END))

        # Create sliders and labels for each match
        for index, match in enumerate(matches):
            parts = match.split(":")
            name = parts[1]  # Extract the name from the match

            label = tk.Label(self.master, text=f"{name}:")
            label.grid(row=index + 2, column=0, pady=5, padx=10, sticky="w")
            self.labels.append(label)  # Store the label for association

            current_value = float(parts[-1][:-1])
            value = tk.DoubleVar(value=current_value)
            self.current_values.append(value)

            slider = ttk.Scale(self.master, from_=2.0, to=0.0, orient="horizontal", variable=value,
                               command=lambda val, index=index: self.update_text(index))
            slider.set(current_value)  # Set the initial value
            slider.grid(row=index + 2, column=1, columnspan=2, pady=5, padx=10, sticky="w")

    def update_text(self, index):
        # Update the text box with the adjusted values from sliders
        adjusted_text = self.text_box.get(1.0, tk.END)
        matches = re.findall(r'(<lora:\w+:\d+\.\d+>)', adjusted_text)

        for i, match in enumerate(matches):
            current_value = self.current_values[i].get()
            adjusted_text = adjusted_text.replace(match, '{}{:.2f}>'.format(match[:-3], current_value), 1)

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
    root = tk.Tk()
    app = StringAdjusterApp(root)
    root.mainloop()
