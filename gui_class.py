import tkinter as tk


class Gui:
    def __init__(self, relays, sensors, user_input, time_controller):
        self.window = tk.Tk()
        self.window.title("Temperatur- og luftfugtighedsstyring")
        self.window.geometry("428x380")
        
        self.relays = relays
        self.sensors = sensors
        self.user_input = user_input
        self.time_controller = time_controller

        # Data entry frame

        self.target_entry_frame = tk.Frame(self.window)
        self.target_entry_frame.grid(row=0, column=0, padx=90, pady=10, sticky="nw")

        # Target temperature entry
        tk.Label(self.target_entry_frame, text="Ønsket temperatur:").grid(row=0, column=0, sticky="w")
        self.target_temperature_textentry = tk.Entry(self.target_entry_frame, width=7)
        self.target_temperature_textentry.grid(row=0, column=1, padx=(12, 0))
        tk.Label(self.target_entry_frame, text="°C").grid(row=0, column=2, sticky="w", padx=(5, 0))

        # Target humidity entry
        tk.Label(self.target_entry_frame, text="Ønsket luftfugtighed:").grid(row=1, column=0, sticky="w")
        self.target_humidity_textentry = tk.Entry(self.target_entry_frame, width=7)
        self.target_humidity_textentry.grid(row=1, column=1, padx=(12, 0))
        tk.Label(self.target_entry_frame, text="%").grid(row=1, column=2, sticky="w", padx=(5, 0))

        # Running time entry
        tk.Label(self.target_entry_frame, text="Behandlingstid:").grid(row=2, column=0, sticky="w")
        self.running_time_textentry = tk.Entry(self.target_entry_frame, width=7)
        self.running_time_textentry.grid(row=2, column=1, padx=(12, 0))
        tk.Label(self.target_entry_frame, text="min.").grid(row=2, column=2, sticky="w", padx=(5, 0))

        # Data display frame
        
        self.data_display_frame = tk.Frame(self.window, borderwidth=1, relief="sunken")
        self.data_display_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

        # Temperature
        tk.Label(self.data_display_frame, text="Ønsket temperatur:").grid(row=0, column=0, sticky="w", padx=(5, 0), pady=(5, 0))
        self.target_temperature_label = tk.Label(self.data_display_frame, text="N/A", width=5)
        self.target_temperature_label.grid(row=0, column=1, sticky="w", padx=(0, 20), pady=(5, 0))

        tk.Label(self.data_display_frame, text="Faktisk temperatur:").grid(row=0, column=2, sticky="w", pady=(5, 0))
        self.actual_temperature_label = tk.Label(self.data_display_frame, text="N/A", width=5)
        self.actual_temperature_label.grid(row=0, column=3, sticky="w", padx=(0, 5),  pady=(5, 0))

        # Humidity
        tk.Label(self.data_display_frame, text="Ønsket luftfugtighed:").grid(row=1, column=0, sticky="w", padx=(5, 0))
        self.target_humidity_label = tk.Label(self.data_display_frame, text="N/A", width=5)
        self.target_humidity_label.grid(row=1, column=1, sticky="w", padx=(0, 20))

        tk.Label(self.data_display_frame, text="Faktisk luftfugtighed:").grid(row=1, column=2, sticky="w")
        self.actual_humidity_label = tk.Label(self.data_display_frame, text="N/A", width=5)
        self.actual_humidity_label.grid(row=1, column=3, sticky="w", padx=(0, 5))

        # Fan and heater
        tk.Label(self.data_display_frame, text="Ventilator:").grid(row=2, column=0, sticky="w", padx=(5, 0), pady=(10, 0))
        self.ventilator_label = tk.Label(self.data_display_frame, text="N/A", width=5)
        self.ventilator_label.grid(row=2, column=1, sticky="w", padx=(0, 20), pady=(10, 0))

        tk.Label(self.data_display_frame, text="Varmer:").grid(row=2, column=2, sticky="w", pady=(10, 0))
        self.varmer_label = tk.Label(self.data_display_frame, text="N/A", width=5)
        self.varmer_label.grid(row=2, column=3, sticky="w", padx=(0, 5), pady=(10, 0))

        # Dehumidifier and steam generator
        tk.Label(self.data_display_frame, text="Affugter:").grid(row=3, column=0, sticky="w", padx=(5, 0))
        self.affugter_label = tk.Label(self.data_display_frame, text="N/A", width=5)
        self.affugter_label.grid(row=3, column=1, sticky="w", padx=(0, 20))

        tk.Label(self.data_display_frame, text="Damp Generator:").grid(row=3, column=2, sticky="w")
        self.damp_label = tk.Label(self.data_display_frame, text="N/A", width=5)
        self.damp_label.grid(row=3, column=3, sticky="w", padx=(0, 5))

        # Time elapsed and remaining
        tk.Label(self.data_display_frame, text="Tid gået:").grid(row=4, column=0, sticky="w", padx=(5, 0), pady=(10, 5))
        self.elapsed_time_label = tk.Label(self.data_display_frame, text="N/A", width=5)
        self.elapsed_time_label.grid(row=4, column=1, sticky="w", pady=(10, 5))

        tk.Label(self.data_display_frame, text="Tid tilbage:").grid(row=4, column=2, sticky="w", pady=(10, 5))
        self.remaining_time_label = tk.Label(self.data_display_frame, text="N/A", width=5)
        self.remaining_time_label.grid(row=4, column=3, sticky="w", pady=(10, 5))

        # Button frame

        self.button_frame = tk.Frame(self.window)
        self.button_frame.grid(row=2, column=0, padx=90, pady=10, sticky="nw")

        # Left spacer
        tk.Label(self.button_frame, text="").grid(row=0, column=0)

        # Start button
        self.start_button = tk.Button(self.button_frame, text="Start", width=8, command=self.on_start_button_press)
        self.start_button.grid(row=0, column=1)

        # Middle spacer
        tk.Label(self.button_frame, text="").grid(row=0, column=2, padx=20)

        # Cancel button
        self.cancel_button = tk.Button(self.button_frame, text="Afbryd", width=8, command=self.on_cancel_button_press)
        self.cancel_button.grid(row=0, column=3)

        # Right spacer
        tk.Label(self.button_frame, text="").grid(row=0, column=4)

        # Status frame

        self.status_frame = tk.Frame(self.window)
        self.status_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nw")
        self.status_frame.grid_columnconfigure(0, weight=0)
        self.status_frame.grid_columnconfigure(1, weight=1)

        # Current operating status
        tk.Label(self.status_frame, text="Status:").grid(row=0, column=0, sticky="w")
        self.status_label = tk.Label(self.status_frame, text="Stoppet")
        self.status_label.grid(row=0, column=1, sticky="w")

        # Error message, if any
        self.error_label = tk.Label(self.status_frame, fg="red", text="This is a sample error message")
        self.error_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=(0, 20), pady=(10, 0))
        
    def update(self):
        if self.sensors.current_temp_dht is not None:
            self.actual_temperature_label.config(text=str(self.sensors.current_temp_dht) + "°C")
        if self.sensors.current_hum_dht is not None:
            self.actual_humidity_label.config(text=str(self.sensors.current_hum_dht) + "%")
            
        self.ventilator_label.config(text="ON", fg="Green") if self.relays.ventilator_ch1.is_lit else self.ventilator_label.config(text="OFF", fg="Red")
        self.varmer_label.config(text="ON", fg="Green") if self.relays.varmer_ch2.is_lit else self.varmer_label.config(text="OFF", fg="Red")
        self.affugter_label.config(text="ON", fg="Green") if self.relays.affugter_ch3.is_lit else self.affugter_label.config(text="OFF", fg="Red")
        self.damp_label.config(text="ON", fg="Green") if self.relays.damp_ch4.is_lit else self.damp_label.config(text="OFF", fg="Red")
        self.status_label.config(text="Kører.") if self.relays.running_ch5.is_lit else self.status_label.config(text="Stoppet.")
        self.error_label.config(text="Fejl", fg="Red") if self.relays.error_ch6.is_lit else self.error_label.config(text="Ingen fejl.", fg="Green")
        if self.time_controller.start is not None:
            self.elapsed_time_label.config(text=str(self.time_controller.get_elapsed() // 60) + " min.")
            self.remaining_time_label.config(text=str(self.time_controller.get_remaining() // 60) + " min.") if self.time_controller.get_remaining() > 0 else self.remaining_time_label.config(text="N/A")

    def clear_text_entry_fields(self):
        self.target_temperature_textentry.delete(0, tk.END)
        self.target_humidity_textentry.delete(0, tk.END)
        self.running_time_textentry.delete(0, tk.END)
        
    def on_start_button_press(self):
        self.user_input.read(self.target_temperature_textentry.get(),
                        self.target_humidity_textentry.get(),
                        self.running_time_textentry.get())
        if self.user_input.is_correct:
            self.relays.running_ch5.on()
            self.time_controller.start_timer()
            self.clear_text_entry_fields()
            self.target_temperature_label.config(text=str(self.user_input.target_temp) + "°C")
            self.target_humidity_label.config(text=str(self.user_input.target_humidity) + "%")
            self.target_temperature_textentry.focus_set()
        
    def on_cancel_button_press(self):
        self.relays.reset_all_channels()
        self.time_controller.reset()
        self.user_input.reset()
        self.target_temperature_label.config(text="N/A")
        self.target_humidity_label.config(text="N/A")
        self.elapsed_time_label.config(text="N/A")
        self.remaining_time_label.config(text="N/A")
        self.target_temperature_textentry.focus_set()