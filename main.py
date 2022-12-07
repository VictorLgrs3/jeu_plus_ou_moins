import random
import tkinter as tk
import tkinter.messagebox as tkmsg
import sqlite3
from fonctions_tkinter import *


class Game:
    def __init__(self):
        self.data_player_fix = []
        self.window_main = tk.Tk()
        self.window_main.title("Jeu du juste prix")
        self.window_main.geometry(center_window_main(self.window_main, 400, 200))
        # self.window_main.iconbitmap()

        self.menubar = tk.Menu(self.window_main, font=("Courrier", 12))
        self.window_main.config(menu=self.menubar)

        self.menu_player = tk.Menu(self.menubar, tearoff=False)

        self.menu_player.add_command(label="Stats", command=self.view_stats)
        self.menu_player.add_separator()
        self.menu_player.add_command(label="Déconnexion", command=self.logout)

        self.menubar.add_cascade(label=" ", menu=self.menu_player)

        frame_main = tk.LabelFrame(self.window_main, text="Entrez les paramètres de jeu", font=("Courrier", 12))
        frame_main.pack(expand=tk.YES)

        tk.Label(frame_main, text="Minimum : ", font=("Courrier", 12)).grid(row=0, column=0, sticky="e")
        self.entry_minimum = tk.Entry(frame_main, font=("Courrier", 11))
        self.entry_minimum.grid(row=0, column=1)

        tk.Label(frame_main, text="Maximum : ", font=("Courrier", 12)).grid(row=1, column=0, sticky="e")
        self.entry_maximum = tk.Entry(frame_main, font=("Courrier", 11))
        self.entry_maximum.grid(row=1, column=1)

        tk.Label(frame_main, text="Essai(s) : ", font=("Courrier", 12)).grid(row=2, column=0, sticky="e")
        self.entry_essais = tk.Entry(frame_main, font=("Courrier", 11))
        self.entry_essais.grid(row=2, column=1)

        self.window_main.after(0, lambda: self.login_graphique())
        self.window_main.mainloop()

    def login_graphique(self):

        def login_fonction():
            pseudo, password, check_login = entry_pseudo.get(), entry_password.get(), var_login.get()
            if len(pseudo) != 0 and len(password) != 0:
                cursor.execute('SELECT * FROM joueurs WHERE pseudo = ? AND password = ?', [pseudo, password])
                data_player = cursor.fetchall()
                if len(data_player) != 0:
                    if check_login:
                        cursor.execute('INSERT INTO connection VALUES (?,?)', [data_player[0][0], 1])
                        db.commit()
                    self.menubar.delete(1)
                    self.menubar.add_cascade(label=data_player[0][1], menu=self.menu_player)
                    self.data_player_fix = data_player
                    self.window_main.deiconify()
                    window_login.destroy()
                else:
                    tkmsg.showwarning("Utilisateur introuvable", "Pseudo ou mot de passe incorrect",
                                      parent=window_login)
            else:
                pass

        def view_password():
            if entry_password["show"] == "*":
                entry_password["show"] = ""
                button_view_password.config(image=icon_button_0)
            else:
                entry_password["show"] = "*"
                button_view_password.config(image=icon_button_1)

        cursor.execute('SELECT * FROM connection')
        data = cursor.fetchall()
        if len(data) == 0:
            self.window_main.withdraw()
            window_login = tk.Toplevel(self.window_main)
            window_login.focus_set()
            window_login.title("Page de connexion")
            window_login.geometry(center_window_main(window_login, 380, 170))
            window_login.resizable(False, False)

            frame_main = tk.LabelFrame(window_login, text="Entrez les informations de connexion", font=("Courrier", 14))
            frame_main.pack(expand=tk.YES)

            tk.Label(frame_main, text="Pseudo : ", font=("Courrier", 13)).grid(row=0, column=0, sticky="e",
                                                                               pady=(15, 5))
            entry_pseudo = tk.Entry(frame_main, font=("Courrier", 12))
            entry_pseudo.grid(row=0, column=1, pady=(15, 5))

            tk.Label(frame_main, text="Mot de passe : ", font=("Courrier", 13)).grid(row=1, column=0)
            entry_password = tk.Entry(frame_main, show="*", font=("Courrier", 12))
            entry_password.grid(row=1, column=1, sticky="e")

            icon_button_1 = tk.PhotoImage(file="image/eye_1.png")
            icon_button_0 = tk.PhotoImage(file="image/eye_0.png")
            button_view_password = tk.Label(frame_main, image=icon_button_1)
            button_view_password.grid(row=1, column=2)
            button_view_password.bind("<Button-1>", lambda event: view_password())

            var_login = tk.BooleanVar()
            checkbutton_login = tk.Checkbutton(frame_main, text="Rester connecté", variable=var_login, onvalue=True,
                                               offvalue=False)
            checkbutton_login.grid(row=2, column=0)

            tk.Button(frame_main, text="Connexion", font=("Courrier", 13),
                      command=login_fonction).grid(row=3, column=0, columnspan=2, pady=(0, 5))

            window_login.bind("<Return>", lambda event: login_fonction())
            window_login.protocol("WM_DELETE_WINDOW", lambda: self.window_main.destroy())
            window_login.mainloop()
        else:
            cursor.execute('SELECT * FROM joueurs JOIN connection ON '
                           'joueurs.id = connection.id')
            data_player = cursor.fetchall()
            self.data_player_fix = data_player
            self.menubar.delete(1)
            self.menubar.add_cascade(label=data_player[0][1], menu=self.menu_player)

    def logout(self):
        cursor.execute('DELETE FROM connection')
        db.commit()
        self.login_graphique()

    def view_stats(self):
        window_stats = tk.Toplevel()
        window_stats.geometry(center_toplevel_in_window_main(self.window_main, 280, 150))
        window_stats.resizable(False, False)

        frame_main = tk.Frame(window_stats)
        frame_main.pack(expand=tk.YES)

        data = self.data_player_fix[0]

        tk.Label(frame_main, text="Pseudo : ", font=("Courrier", 12)).grid(row=0, column=0, sticky="e")
        tk.Label(frame_main, text=data[1], font=("Courrier", 12)).grid(row=0, column=1, sticky="w")

        tk.Label(frame_main, text="Partie gagnée : ", font=("Courrier", 12)).grid(row=1, column=0, sticky="e")
        tk.Label(frame_main, text=data[3], font=("Courrier", 12)).grid(row=1, column=1, sticky="w")

        tk.Label(frame_main, text="Partie perdue : ", font=("Courrier", 12)).grid(row=2, column=0, sticky="e")
        tk.Label(frame_main, text=data[4], font=("Courrier", 12)).grid(row=2, column=1, sticky="w")

        tk.Label(frame_main, text="Partie jouer : ", font=("Courrier", 12)).grid(row=3, column=0, sticky="e")
        tk.Label(frame_main, text=data[3]+data[4], font=("Courrier", 12)).grid(row=3, column=1, sticky="w")

        tk.Label(frame_main, text="Ratio v/d : ", font=("Courrier", 12)).grid(row=4, column=0, sticky="e")
        if data[3] == 0 and data[4] == 0:
            tk.Label(frame_main, text=0, font=("Courrier", 12)).grid(row=4, column=1, sticky="w")
        else:
            tk.Label(frame_main, text=round(data[3]/(data[3] + data[4]), 3),
                     font=("Courrier", 12)).grid(row=4, column=1, sticky="w")

        window_stats.mainloop()


if __name__ == '__main__':
    # Ouverture de la base de données
    db = sqlite3.connect('base.db')
    cursor = db.cursor()

    # Lancement du jeu
    jeu = Game()

    # Fermeture de la base de données
    cursor.close()
    db.close()

