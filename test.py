import tkinter as tk
import tkinter.messagebox as tkmsg
import sqlite3


def center_window(fen, width: int = 600, height: int = 400):
    x_coordinate = int((fen.winfo_screenwidth() / 2) - (width / 2))
    y_coordinate = int((fen.winfo_screenheight() / 2) - (height / 2) - 40)
    return f"{width}x{height}+{x_coordinate}+{y_coordinate}"


def close_toplevel(win, toplevel):
    toplevel.destroy()
    win.deiconify()


def login_graphique():

    def login_fonction():
        pseudo, password = entry_pseudo.get(), entry_password.get()
        check_login = var_login.get()
        if len(pseudo) != 0 and len(password) != 0:
            cursor.execute('SELECT * FROM joueurs WHERE pseudo = ? AND password = ?', [pseudo, password])
            data = cursor.fetchall()
            if len(data) != 0:
                if check_login:
                    cursor.execute('INSERT INTO connection VALUES (?,?)', [data[0][0], 1])
                    connection.commit()
                    label_pseudo_fixe["text"] = data[0][1]
                    close_toplevel(fen_main, fen)
                else:
                    label_pseudo_fixe["text"] = data[0][1]
                    close_toplevel(fen_main, fen)
            else:
                tkmsg.showinfo("Pseudo ou mot de passe invalide", "Le pseudo ou le mot de passe est invalide",
                               parent=fen)

    cursor.execute('SELECT * FROM connection')
    data_login = cursor.fetchall()
    if len(data_login) == 0:
        fen_main.withdraw()
        fen = tk.Toplevel()
        fen.geometry(center_window(fen, 400, 200))
        fen.title("Test de connexion")
        fen.config(bg="#D32930")

        frame = tk.Frame(fen)
        frame.pack(expand=tk.YES)

        label_pseudo = tk.Label(frame, text="Pseudo : ", font=("Courrier", 12))
        label_pseudo.grid(row=0, column=0, sticky="e")
        entry_pseudo = tk.Entry(frame, font=("Courrier", 11))
        entry_pseudo.grid(row=0, column=1)

        label_password = tk.Label(frame, text="Mot de passe : ", font=("Courrier", 12))
        label_password.grid(row=1, column=0, sticky="e")
        entry_password = tk.Entry(frame, font=("Courrier", 11))
        entry_password.grid(row=1, column=1)

        var_login = tk.BooleanVar()
        checkbox_login = tk.Checkbutton(frame, text="Rester connecté", variable=var_login, onvalue=True, offvalue=False)
        checkbox_login.grid(row=2, column=0)

        button_validate = tk.Button(frame, text="Se connecter", font=("Courrier", 12))
        button_validate.config(command=login_fonction)
        button_validate.grid(row=3, column=0, columnspan=2, pady=5)

        fen.protocol("WM_DELETE_WINDOW", lambda: fen_main.destroy())
        fen.mainloop()
    else:
        cursor.execute('SELECT * FROM joueurs JOIN connection ON joueurs.id = connection.id')
        data_player = cursor.fetchall()

        label_pseudo_fixe["text"] = data_player[0][1]


def logout():
    cursor.execute('DELETE FROM connection')
    connection.commit()
    login_graphique()


connection = sqlite3.connect('base.db')
cursor = connection.cursor()

fen_main = tk.Tk()
fen_main.geometry(center_window(fen_main))
fen_main.config(bg="gray")

label_pseudo_fixe = tk.Label(fen_main, font=("Courrier", 12))
label_pseudo_fixe.pack(expand=tk.YES)

button_logout = tk.Button(fen_main, text="Déconnexion", font=("Courrier", 12))
button_logout.config(command=logout)
button_logout.pack(expand=tk.YES)

fen_main.after(0, lambda: login_graphique())
fen_main.mainloop()

cursor.close()
connection.close()
