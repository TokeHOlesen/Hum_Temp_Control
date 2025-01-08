import tkinter as tk

def on_button_press():
    print("Button pressed")

# Create main window
window = tk.Tk()
window.title("Temperatur og luftfugtighed")
window.geometry("700x400")

# ------------------------------------------------------------------
# Upper Frame: 3 rows, each with a Label + Entry
# ------------------------------------------------------------------
target_entry_frame = tk.Frame(window)
target_entry_frame.grid(row=0, column=0, padx=60, pady=10, sticky="nw")

# Row 1
tk.Label(target_entry_frame, text="Ønsket temperatur:").grid(row=0, column=0, sticky="w")
target_temperature_textentry = tk.Entry(target_entry_frame, width=7)
target_temperature_textentry.grid(row=0, column=1, padx=(12, 0))
tk.Label(target_entry_frame, text="°C").grid(row=0, column=2, sticky="w", padx=(5, 0))

# Row 2
tk.Label(target_entry_frame, text="Ønsket luftfugtighed:").grid(row=1, column=0, sticky="w")
target_humidity_textentry = tk.Entry(target_entry_frame, width=7)
target_humidity_textentry.grid(row=1, column=1, padx=(12, 0))
tk.Label(target_entry_frame, text="%").grid(row=1, column=2, sticky="w", padx=(5, 0))

# Row 3
tk.Label(target_entry_frame, text="Behandlingstid:").grid(row=2, column=0, sticky="w")
running_time_textentry = tk.Entry(target_entry_frame, width=7)
running_time_textentry.grid(row=2, column=1, padx=(12, 0))
tk.Label(target_entry_frame, text="min.").grid(row=2, column=2, sticky="w", padx=(5, 0))

# ------------------------------------------------------------------
# Middle Frame: 3 rows, each containing labels for display
# ------------------------------------------------------------------
data_display_frame = tk.Frame(window)
data_display_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

# Row 1
tk.Label(data_display_frame, text="Ønsket temperatur:").grid(row=0, column=0, sticky="w")
target_temperature_label = tk.Label(data_display_frame, text="N/A")
target_temperature_label.grid(row=0, column=1, sticky="w", padx=(0, 20))

tk.Label(data_display_frame, text="Faktisk temperatur:").grid(row=0, column=2, sticky="w")
actual_temperature_label = tk.Label(data_display_frame, text="N/A")
actual_temperature_label.grid(row=0, column=3, sticky="w")

# Row 2
tk.Label(data_display_frame, text="Ønsket luftfugtighed:").grid(row=1, column=0, sticky="w")
target_humidity_label = tk.Label(data_display_frame, text="N/A")
target_humidity_label.grid(row=1, column=1, sticky="w", padx=(0, 20))

tk.Label(data_display_frame, text="Faktisk luftfugtighed:").grid(row=1, column=2, sticky="w")
actual_humidity_label = tk.Label(data_display_frame, text="N/A")
actual_humidity_label.grid(row=1, column=3, sticky="w")

# Row 3
tk.Label(data_display_frame, text="Resterende tid:").grid(row=2, column=0, sticky="w")
remaining_time_label = tk.Label(data_display_frame, text="N/A")
remaining_time_label.grid(row=2, column=1, sticky="w")

# ------------------------------------------------------------------
# Bottom Frame: two "Submit" buttons, with spacers on the sides
# ------------------------------------------------------------------
button_frame = tk.Frame(window)
button_frame.grid(row=2, column=0, padx=60, pady=10, sticky="nw")

# Left spacer
tk.Label(button_frame, text="").grid(row=0, column=0)

start_button = tk.Button(button_frame, text="Start", width=8, command=on_button_press)
start_button.grid(row=0, column=1)

# Middle spacer
tk.Label(button_frame, text="").grid(row=0, column=2, padx=20)

cancel_button = tk.Button(button_frame, text="Afbryd", width=8, command=on_button_press)
cancel_button.grid(row=0, column=3)

# Right spacer
tk.Label(button_frame, text="").grid(row=0, column=4)

# Start the Tk event loop
window.mainloop()
