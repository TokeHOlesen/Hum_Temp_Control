import tkinter as tk


def askyesno_dialog(title, message) -> bool:
    dialog = tk.Toplevel()
    dialog.title(title)
    dialog.geometry("520x130")
    dialog.resizable(False, False)
    dialog_font = ("TkDefaultFont", 16)

    label = tk.Label(dialog, text=message, font=dialog_font, pady=10,)
    label.pack()

    response = tk.BooleanVar(value=False)
    
    no_button = tk.Button(dialog, text="Nej", width=10, font=dialog_font, command=lambda: (response.set(False), dialog.destroy()))
    no_button.bind("<Return>", lambda event: (response.set(False), dialog.destroy()))
    no_button.bind("<KP_Enter>", lambda event: (response.set(False), dialog.destroy()))
    no_button.pack(side=tk.LEFT, padx=(60, 0), pady=(0, 20))
    yes_button = tk.Button(dialog, text="Ja", width=10, font=dialog_font, command=lambda: (response.set(True), dialog.destroy()))
    yes_button.bind("<Return>", lambda event: (response.set(True), dialog.destroy()))
    yes_button.bind("<KP_Enter>", lambda event: (response.set(True), dialog.destroy()))
    yes_button.pack(side=tk.RIGHT, padx=(0, 60), pady=(0, 20))
    
    no_button.focus_set()

    dialog.grab_set()
    dialog.wait_window()

    return response.get()


def info_dialog(title, message) -> None:
    dialog = tk.Toplevel()
    dialog.title(title)
    dialog.geometry("520x130")
    dialog.resizable(False, False)
    dialog_font = ("TkDefaultFont", 16)
    
    label = tk.Label(dialog, text=message, font=dialog_font, pady=10,)
    label.pack()
    
    ok_button = tk.Button(dialog, text="OK", width=10, font=dialog_font, command=lambda: dialog.destroy())
    ok_button.bind("<Return>", lambda event: dialog.destroy())
    ok_button.bind("<KP_Enter>", lambda event: dialog.destroy())
    ok_button.pack()
    
    ok_button.focus_set()
    
    dialog.grab_set()
    dialog.wait_window()
