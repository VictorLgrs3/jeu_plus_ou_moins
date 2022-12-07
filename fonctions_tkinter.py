"""
Fichier réutilisable pour d'autre programme, utilisant tkinter
"""

import tkinter


# Centrer une fenêtre tkinter
def center_window_main(window: [tkinter.Tk, tkinter.Toplevel], width: int = 600, height: int = 400, pad_y: float = 40):
    x_coordinate = int((window.winfo_screenwidth() / 2) - (width / 2))
    y_coordinate = int((window.winfo_screenheight() / 2) - (height / 2) - pad_y)
    return f"{width}x{height}+{x_coordinate}+{y_coordinate}"


# Centre une fenêtre tkinter dans une autre fenêtre tkinter
def center_toplevel_in_window_main(window_main: tkinter.Tk, width: int, height: int):
    x_coordinate = int((window_main.winfo_width() / 2) - (width / 2) + window_main.winfo_x())
    y_coordinate = int((window_main.winfo_height() / 2) - (height / 2) + window_main.winfo_y())
    return f'{width}x{height}+{x_coordinate}+{y_coordinate}'
