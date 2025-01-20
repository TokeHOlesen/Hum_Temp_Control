import tkinter as tk

from dialog_window_functions import askyesno_dialog


class Gui:
    def __init__(self, relays, sensors, user_input, time_controller, malfunctions) -> None:
        self.window = tk.Tk()
        self.window.title("Temperatur- og luftfugtighedsstyring")
        self.window.geometry("780x380")
        
        self.relays = relays
        self.sensors = sensors
        self.user_input = user_input
        self.time_controller = time_controller
        self.malfunctions = malfunctions

        # Data entry frame

        self.target_entry_frame = tk.Frame(self.window)
        self.target_entry_frame.grid(row=0, column=0, padx=70, pady=(10, 5), sticky="nw")
        
        self.data_entry_font = ("TkDefaultFont", 13)

        # Target temperature entry
        tk.Label(self.target_entry_frame, text="Ønsket temperatur:", font=self.data_entry_font).grid(row=0, column=0, sticky="w")
        self.target_temperature_textentry = tk.Entry(self.target_entry_frame, width=8, font=self.data_entry_font)
        self.target_temperature_textentry.grid(row=0, column=1, padx=(12, 0))
        self.target_temperature_textentry.bind("<Return>", lambda event: self.target_humidity_textentry.focus_set())
        self.target_temperature_textentry.bind("<KP_Enter>", lambda event: self.target_humidity_textentry.focus_set())
        self.target_temperature_textentry.bind("<Down>", lambda event: self.target_humidity_textentry.focus_set())
        tk.Label(self.target_entry_frame, text="°C", font=self.data_entry_font).grid(row=0, column=2, sticky="w", padx=(5, 0))

        # Target humidity entry
        tk.Label(self.target_entry_frame, text="Ønsket luftfugtighed:", font=self.data_entry_font).grid(row=1, column=0, sticky="w")
        self.target_humidity_textentry = tk.Entry(self.target_entry_frame, width=8, font=self.data_entry_font)
        self.target_humidity_textentry.grid(row=1, column=1, padx=(12, 0))
        self.target_humidity_textentry.bind("<Return>", lambda event: self.running_time_textentry.focus_set())
        self.target_humidity_textentry.bind("<KP_Enter>", lambda event: self.running_time_textentry.focus_set())
        self.target_humidity_textentry.bind("<Down>", lambda event: self.running_time_textentry.focus_set())
        self.target_humidity_textentry.bind("<Up>", lambda event: self.target_temperature_textentry.focus_set())
        tk.Label(self.target_entry_frame, text="%", font=self.data_entry_font).grid(row=1, column=2, sticky="w", padx=(5, 0))

        # Running time entry
        tk.Label(self.target_entry_frame, text="Behandlingstid:", font=self.data_entry_font).grid(row=2, column=0, sticky="w")
        self.running_time_textentry = tk.Entry(self.target_entry_frame, width=8, font=self.data_entry_font)
        self.running_time_textentry.grid(row=2, column=1, padx=(12, 0))
        self.running_time_textentry.bind("<Return>", lambda event: self.start_button.focus_set())
        self.running_time_textentry.bind("<KP_Enter>", lambda event: self.start_button.focus_set())
        self.running_time_textentry.bind("<Down>", lambda event: self.start_button.focus_set())
        self.running_time_textentry.bind("<Up>", lambda event: self.target_humidity_textentry.focus_set())
        tk.Label(self.target_entry_frame, text="min.", font=self.data_entry_font).grid(row=2, column=2, sticky="w", padx=(5, 0))

        # Data display frame
        
        self.data_display_frame = tk.Frame(self.window, borderwidth=1, relief="sunken")
        self.data_display_frame.grid(row=1, column=0, padx=(15, 10), pady=10, sticky="nw")

        # Temperature
        tk.Label(self.data_display_frame, text="Ønsket temperatur:").grid(row=0, column=0, sticky="w", padx=(5, 0), pady=(5, 0))
        self.target_temperature_label = tk.Label(self.data_display_frame, text="N/A", width=8)
        self.target_temperature_label.grid(row=0, column=1, sticky="w", padx=(0, 20), pady=(5, 0))

        tk.Label(self.data_display_frame, text="Faktisk temperatur:").grid(row=0, column=2, sticky="w", pady=(5, 0))
        self.actual_temperature_label = tk.Label(self.data_display_frame, text="N/A", width=8)
        self.actual_temperature_label.grid(row=0, column=3, sticky="w", padx=(0, 5),  pady=(5, 0))

        # Humidity
        tk.Label(self.data_display_frame, text="Ønsket luftfugtighed:").grid(row=1, column=0, sticky="w", padx=(5, 0))
        self.target_humidity_label = tk.Label(self.data_display_frame, text="N/A", width=8)
        self.target_humidity_label.grid(row=1, column=1, sticky="w", padx=(0, 20))

        tk.Label(self.data_display_frame, text="Faktisk luftfugtighed:").grid(row=1, column=2, sticky="w")
        self.actual_humidity_label = tk.Label(self.data_display_frame, text="N/A", width=8)
        self.actual_humidity_label.grid(row=1, column=3, sticky="w", padx=(0, 5))

        # Fan and heater
        tk.Label(self.data_display_frame, text="Ventilator:").grid(row=2, column=0, sticky="w", padx=(5, 0), pady=(10, 0))
        self.ventilator_label = tk.Label(self.data_display_frame, text="N/A", width=8)
        self.ventilator_label.grid(row=2, column=1, sticky="w", padx=(0, 20), pady=(10, 0))

        tk.Label(self.data_display_frame, text="Varmer:").grid(row=2, column=2, sticky="w", pady=(10, 0))
        self.varmer_label = tk.Label(self.data_display_frame, text="N/A", width=8)
        self.varmer_label.grid(row=2, column=3, sticky="w", padx=(0, 5), pady=(10, 0))

        # Dehumidifier and steam generator
        tk.Label(self.data_display_frame, text="Affugter:").grid(row=3, column=0, sticky="w", padx=(5, 0))
        self.affugter_label = tk.Label(self.data_display_frame, text="N/A", width=8)
        self.affugter_label.grid(row=3, column=1, sticky="w", padx=(0, 20))

        tk.Label(self.data_display_frame, text="Damp Generator:").grid(row=3, column=2, sticky="w")
        self.damp_label = tk.Label(self.data_display_frame, text="N/A", width=8)
        self.damp_label.grid(row=3, column=3, sticky="w", padx=(0, 5))

        # Time elapsed and remaining
        tk.Label(self.data_display_frame, text="Tid i drift:").grid(row=4, column=0, sticky="w", padx=(5, 0), pady=(10, 5))
        self.elapsed_time_label = tk.Label(self.data_display_frame, text="N/A", width=8)
        self.elapsed_time_label.grid(row=4, column=1, sticky="w", pady=(10, 5))

        tk.Label(self.data_display_frame, text="Tid tilbage:").grid(row=4, column=2, sticky="w", pady=(10, 5))
        self.remaining_time_label = tk.Label(self.data_display_frame, text="N/A", width=8)
        self.remaining_time_label.grid(row=4, column=3, sticky="w", pady=(10, 5))

        # Button frame

        self.button_frame = tk.Frame(self.window)
        self.button_frame.grid(row=2, column=0, padx=48, pady=5, sticky="nw")
        
        self.button_font = ("TkDefaultFont", 16)

        # Left spacer
        tk.Label(self.button_frame, text="").grid(row=0, column=0)

        # Start button
        self.start_button = tk.Button(self.button_frame, text="Start", font=self.button_font, width=10, command=self.on_start_button_press)
        self.start_button.grid(row=0, column=3)
        self.start_button.bind("<Return>", lambda event: self.on_start_button_press())
        self.start_button.bind("<KP_Enter>", lambda event: self.on_start_button_press())
        self.start_button.bind("<Left>", lambda event: self.cancel_button.focus_set())
        self.start_button.bind("<Up>", lambda event: self.running_time_textentry.focus_set())

        # Middle spacer
        tk.Label(self.button_frame, text="").grid(row=0, column=2, padx=20)

        # Cancel button
        self.cancel_button = tk.Button(self.button_frame, text="Afbryd", font=self.button_font, width=10, command=self.on_cancel_button_press)
        self.cancel_button.grid(row=0, column=1)
        self.cancel_button.bind("<Return>", lambda event: self.on_cancel_button_press())
        self.cancel_button.bind("<KP_Enter>", lambda event: self.on_cancel_button_press())
        self.cancel_button.bind("<Right>", lambda event: self.start_button.focus_set())
        self.cancel_button.bind("<Up>", lambda event: self.running_time_textentry.focus_set())

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
        self.error_label = tk.Label(self.status_frame)
        self.error_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=(0, 20), pady=(10, 0))
        
        # Numpad frame
        
        self.numpad_frame = tk.Frame(self.window)
        self.numpad_frame.grid(row=0, column=1, rowspan=4, padx=5, pady=(10, 0), sticky="n")

        # Button font settings
        self.numpad_button_font = ("TkDefaultFont", 16)

        # Top row (Backspace)
        tk.Label(self.numpad_frame, text="").grid(row=0, column=1)
        self.backspace_button = tk.Button(self.numpad_frame, text="Backspace", width=9, height=2, font=self.numpad_button_font, command=self.on_backspace_button_press)
        self.backspace_button.grid(row=0, column=1, columnspan=2, padx=(18, 0), pady=2)

        # Second row (7, 8, 9)
        self.num7_button = tk.Button(self.numpad_frame, text="7", width=4, height=2, font=self.numpad_button_font, command=lambda: self.on_number_button_press(7))
        self.num7_button.grid(row=1, column=0, padx=2, pady=2)
        self.num8_button = tk.Button(self.numpad_frame, text="8", width=4, height=2, font=self.numpad_button_font, command=lambda: self.on_number_button_press(8))
        self.num8_button.grid(row=1, column=1, padx=2, pady=2)
        self.num9_button = tk.Button(self.numpad_frame, text="9", width=4, height=2, font=self.numpad_button_font, command=lambda: self.on_number_button_press(9))
        self.num9_button.grid(row=1, column=2, padx=2, pady=2)

        # Third row (4, 5, 6)
        self.num4_button = tk.Button(self.numpad_frame, text="4", width=4, height=2, font=self.numpad_button_font, command=lambda: self.on_number_button_press(4))
        self.num4_button.grid(row=2, column=0, padx=2, pady=2)
        self.num5_button = tk.Button(self.numpad_frame, text="5", width=4, height=2, font=self.numpad_button_font, command=lambda: self.on_number_button_press(5))
        self.num5_button.grid(row=2, column=1, padx=2, pady=2)
        self.num6_button = tk.Button(self.numpad_frame, text="6", width=4, height=2, font=self.numpad_button_font, command=lambda: self.on_number_button_press(6))
        self.num6_button.grid(row=2, column=2, padx=2, pady=2)

        # Fourth row (1, 2, 3)
        self.num1_button = tk.Button(self.numpad_frame, text="1", width=4, height=2, font=self.numpad_button_font, command=lambda: self.on_number_button_press(1))
        self.num1_button.grid(row=3, column=0, padx=2, pady=2)
        self.num2_button = tk.Button(self.numpad_frame, text="2", width=4, height=2, font=self.numpad_button_font, command=lambda: self.on_number_button_press(2))
        self.num2_button.grid(row=3, column=1, padx=2, pady=2)
        self.num3_button = tk.Button(self.numpad_frame, text="3", width=4, height=2, font=self.numpad_button_font, command=lambda: self.on_number_button_press(3))
        self.num3_button.grid(row=3, column=2, padx=2, pady=2)

        # Fifth row (0 and Enter)
        self.num0_button = tk.Button(self.numpad_frame, text="0", width=4, height=2, font=self.numpad_button_font, command=lambda: self.on_number_button_press(0))
        self.num0_button.grid(row=4, column=0, padx=2, pady=2)
        self.enter_button = tk.Button(self.numpad_frame, text="Enter", width=9, height=2, font=self.numpad_button_font, command=self.on_enter_button_press)
        self.enter_button.grid(row=4, column=1, columnspan=2, padx=(18, 0), pady=2)


    def update(self) -> None:
        if self.sensors.current_temp_dht is not None:
            self.actual_temperature_label.config(text=str(self.sensors.current_temp_dht) + "°C")
        if self.sensors.current_hum_dht is not None:
            self.actual_humidity_label.config(text=str(self.sensors.current_hum_dht) + "%")
            
        self.ventilator_label.config(text="ON", fg="Green") if self.relays.ventilator_ch1.is_lit else self.ventilator_label.config(text="OFF", fg="Red")
        self.varmer_label.config(text="ON", fg="Green") if self.relays.varmer_ch2.is_lit else self.varmer_label.config(text="OFF", fg="Red")
        self.affugter_label.config(text="ON", fg="Green") if self.relays.affugter_ch3.is_lit else self.affugter_label.config(text="OFF", fg="Red")
        self.damp_label.config(text="ON", fg="Green") if self.relays.damp_ch4.is_lit else self.damp_label.config(text="OFF", fg="Red")
        if self.relays.running_ch5.is_lit:
            if self.relays.error_ch6.is_lit:
                 self.status_label.config(text="Fejl.")
            else:
                if self.sensors.target_values_reached:
                    self.status_label.config(text="Kører.")
                else:
                    self.status_label.config(text="Varmer op.")
        else:
             self.status_label.config(text="Stoppet.")
        self.error_label.config(text=self.malfunctions.message, fg="Red") if self.relays.error_ch6.is_lit else self.error_label.config(text="Ingen fejl.", fg="Green")
        if self.time_controller.start is not None:
            self.update_time_display()
        
        if self.relays.running_ch5.is_lit:
            self.start_button.config(state="disabled")
            self.cancel_button.config(state="normal")
            self.target_temperature_textentry.config(state="disabled")
            self.target_humidity_textentry.config(state="disabled")
            self.running_time_textentry.config(state="disabled")
        else:
            self.start_button.config(state="normal")
            self.cancel_button.config(state="disabled")
            self.target_temperature_textentry.config(state="normal")
            self.target_humidity_textentry.config(state="normal")
            self.running_time_textentry.config(state="normal")

    def update_time_display(self) -> None:
        # Updates elapsed time display
        elapsed_hours, elapsed_minutes, elapsed_seconds = self.time_controller.elapsed_h_m_s
        self.elapsed_time_label.config(text=f"{elapsed_hours:02}:{elapsed_minutes:02}:{elapsed_seconds:02}")
        # Updates remaining time display, if target set; else "Ubestemt"
        if self.time_controller.seconds_remaining > 0 and self.sensors.target_values_reached:
            remaining_hours, remaining_minutes, remaining_seconds = self.time_controller.remaining_h_m_s
            self.remaining_time_label.config(text=f"{remaining_hours:02}:{remaining_minutes:02}:{remaining_seconds:02}")
        else:
            if self.sensors.target_values_reached:
                self.remaining_time_label.config(text="Ubestemt")
            else:
                self.remaining_time_label.config(text="Ukendt")
        
    def clear_text_entry_fields(self) -> None:
        self.target_temperature_textentry.delete(0, tk.END)
        self.target_humidity_textentry.delete(0, tk.END)
        self.running_time_textentry.delete(0, tk.END)
        
    def on_start_button_press(self) -> None:
        self.user_input.read(self.target_temperature_textentry.get(),
                        self.target_humidity_textentry.get(),
                        self.running_time_textentry.get())
        if self.user_input.is_correct:
            self.relays.running_ch5.on()
            self.time_controller.start_timer()
            self.clear_text_entry_fields()
            self.target_temperature_label.config(text=str(self.user_input.target_temp) + "°C")
            self.target_humidity_label.config(text=str(self.user_input.target_humidity) + "%")
        
    def on_cancel_button_press(self) -> None:
        if askyesno_dialog("Bekræft afslutning", "Er du sikker på, at du vil afbryde kørslen?"):
            self.cancel_process()
    
    def cancel_process(self) -> None:
        self.relays.reset_all_channels()
        self.time_controller.reset()
        self.user_input.reset()
        self.sensors.reset()
        self.target_temperature_label.config(text="N/A")
        self.target_humidity_label.config(text="N/A")
        self.elapsed_time_label.config(text="N/A")
        self.remaining_time_label.config(text="N/A")
        self.target_temperature_textentry.focus_set()

    def on_number_button_press(self, number) -> None:
        current_widget = self.window.focus_get()
        if isinstance(current_widget, tk.Entry):
            current_text = current_widget.get()
            current_widget.delete(0, tk.END)
            current_widget.insert(0, current_text + str(number))

    def on_backspace_button_press(self) -> None:
        current_widget = self.window.focus_get()
        if isinstance(current_widget, tk.Entry):
            current_text = current_widget.get()
            current_widget.delete(0, tk.END)
            current_widget.insert(0, current_text[:-1])

    def on_enter_button_press(self) -> None:
        widgets = [
            self.target_temperature_textentry,
            self.target_humidity_textentry,
            self.running_time_textentry,
            self.start_button
        ]
        
        if not self.relays.running_ch5.is_lit:
            focused_widget = self.window.focus_get()
            if focused_widget in widgets:
                current_index = widgets.index(focused_widget)
                if widgets[current_index] == self.start_button:
                    if not self.relays.running_ch5.is_lit:
                        self.on_start_button_press()
                else:
                    next_index = (current_index + 1) % len(widgets)
                    widgets[next_index].focus_set()
        