import tkinter as tk

# Placeholder
def on_button_press():
    print("Button pressed")


window = tk.Tk()
window.title("Temperatur og luftfugtighed")
window.geometry("426x380")

# Data entry frame

target_entry_frame = tk.Frame(window)
target_entry_frame.grid(row=0, column=0, padx=90, pady=10, sticky="nw")

# Target temperature entry
tk.Label(target_entry_frame, text="Ønsket temperatur:").grid(row=0, column=0, sticky="w")
target_temperature_textentry = tk.Entry(target_entry_frame, width=7)
target_temperature_textentry.grid(row=0, column=1, padx=(12, 0))
tk.Label(target_entry_frame, text="°C").grid(row=0, column=2, sticky="w", padx=(5, 0))

# Target humidity entry
tk.Label(target_entry_frame, text="Ønsket luftfugtighed:").grid(row=1, column=0, sticky="w")
target_humidity_textentry = tk.Entry(target_entry_frame, width=7)
target_humidity_textentry.grid(row=1, column=1, padx=(12, 0))
tk.Label(target_entry_frame, text="%").grid(row=1, column=2, sticky="w", padx=(5, 0))

# Running time entry
tk.Label(target_entry_frame, text="Behandlingstid:").grid(row=2, column=0, sticky="w")
running_time_textentry = tk.Entry(target_entry_frame, width=7)
running_time_textentry.grid(row=2, column=1, padx=(12, 0))
tk.Label(target_entry_frame, text="min.").grid(row=2, column=2, sticky="w", padx=(5, 0))


# Data display frame

data_display_frame = tk.Frame(window, borderwidth=1, relief="sunken")
data_display_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

# Temperature
tk.Label(data_display_frame, text="Ønsket temperatur:").grid(row=0, column=0, sticky="w", padx=(5, 0), pady=(5, 0))
target_temperature_label = tk.Label(data_display_frame, text="N/A", width=5)
target_temperature_label.grid(row=0, column=1, sticky="w", padx=(0, 20), pady=(5, 0))

tk.Label(data_display_frame, text="Faktisk temperatur:").grid(row=0, column=2, sticky="w", pady=(5, 0))
actual_temperature_label = tk.Label(data_display_frame, text="N/A", width=5)
actual_temperature_label.grid(row=0, column=3, sticky="w", padx=(0, 5),  pady=(5, 0))

# Humidity
tk.Label(data_display_frame, text="Ønsket luftfugtighed:").grid(row=1, column=0, sticky="w", padx=(5, 0))
target_humidity_label = tk.Label(data_display_frame, text="N/A", width=5)
target_humidity_label.grid(row=1, column=1, sticky="w", padx=(0, 20))

tk.Label(data_display_frame, text="Faktisk luftfugtighed:").grid(row=1, column=2, sticky="w")
actual_humidity_label = tk.Label(data_display_frame, text="N/A", width=5)
actual_humidity_label.grid(row=1, column=3, sticky="w", padx=(0, 5))

# Fan and heater
tk.Label(data_display_frame, text="Ventilator:").grid(row=2, column=0, sticky="w", padx=(5, 0), pady=(10, 0))
ventilator_label = tk.Label(data_display_frame, text="N/A", width=5)
ventilator_label.grid(row=2, column=1, sticky="w", padx=(0, 20), pady=(10, 0))

tk.Label(data_display_frame, text="Varmer:").grid(row=2, column=2, sticky="w", pady=(10, 0))
varmer_label = tk.Label(data_display_frame, text="N/A", width=5)
varmer_label.grid(row=2, column=3, sticky="w", padx=(0, 5), pady=(10, 0))

# Dehumidifier and steam generator
tk.Label(data_display_frame, text="Affugter:").grid(row=3, column=0, sticky="w", padx=(5, 0))
affugter_label = tk.Label(data_display_frame, text="N/A", width=5)
affugter_label.grid(row=3, column=1, sticky="w", padx=(0, 20))

tk.Label(data_display_frame, text="Damp Generator:").grid(row=3, column=2, sticky="w")
damp_label = tk.Label(data_display_frame, text="N/A", width=5)
damp_label.grid(row=3, column=3, sticky="w", padx=(0, 5))

# Time remaining
tk.Label(data_display_frame, text="Resterende tid:").grid(row=4, column=0, sticky="w", padx=(5, 0), pady=(10, 5))
remaining_time_label = tk.Label(data_display_frame, text="N/A", width=5)
remaining_time_label.grid(row=4, column=1, sticky="w", pady=(10, 5))


# Button frame

button_frame = tk.Frame(window)
button_frame.grid(row=2, column=0, padx=90, pady=10, sticky="nw")

# Left spacer
tk.Label(button_frame, text="").grid(row=0, column=0)

# Start button
start_button = tk.Button(button_frame, text="Start", width=8, command=on_button_press)
start_button.grid(row=0, column=1)

# Middle spacer
tk.Label(button_frame, text="").grid(row=0, column=2, padx=20)

# Cancel button
cancel_button = tk.Button(button_frame, text="Afbryd", width=8, command=on_button_press)
cancel_button.grid(row=0, column=3)

# Right spacer
tk.Label(button_frame, text="").grid(row=0, column=4)


# Status frame

status_frame = tk.Frame(window)
status_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nw")
status_frame.grid_columnconfigure(0, weight=0)
status_frame.grid_columnconfigure(1, weight=1)

# Current operating status
tk.Label(status_frame, text="Status:").grid(row=0, column=0, sticky="w")
status_label = tk.Label(status_frame, text="Stoppet")
status_label.grid(row=0, column=1, sticky="w")

# Error message, if any
error_label = tk.Label(status_frame, fg="red", text="This is a sample error message")
error_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=(0, 20), pady=(10, 0))


# Main Tk loop
target_temperature_textentry.focus_set()
window.mainloop()
