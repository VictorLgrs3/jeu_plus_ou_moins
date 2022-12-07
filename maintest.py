"""
La base de données, comporte deux tables dont une 'joueurs' ou il y a les joueurs, cette table est normalement stockée
sur un serveur et la deuxième table 'connection' permet de rester connecté à l'application même quand on la ferme,
cette deuxième table sera stockée localement sur la machine du joueur.
"""

import random
import tkinter as tk
import tkinter.messagebox as tkmsg


def center_window(fen, width: int = 600, height: int = 400):
    x_coordinate = int((fen.winfo_screenwidth() / 2) - (width / 2))
    y_coordinate = int((fen.winfo_screenheight() / 2) - (height / 2) - 40)
    return f"{width}x{height}+{x_coordinate}+{y_coordinate}"


class Window:
    def __init__(self):
        self.essais = 0
        self.fen = tk.Tk()
        self.fen.title("Jeu du juste prix")
        self.fen.geometry(center_window(self.fen, 340, 200))
        self.fen.resizable(False, False)

        frame = tk.LabelFrame(self.fen, text="Choisir les options du jeu", font=("Courrier", 14))
        frame.pack(expand=tk.YES)

        tk.Label(frame, text="Minimum : ", font=("Courrier", 13)).grid(row=0, column=0, sticky="ne", pady=5)
        self.entry_minimum = tk.Entry(frame, font=("Courrier", 12))
        self.entry_minimum.grid(row=0, column=1, sticky="w")

        tk.Label(frame, text="Maximum : ", font=("Courrier", 13)).grid(row=1, column=0, sticky="ne", pady=5)
        self.entry_maximum = tk.Entry(frame, font=("Courrier", 12))
        self.entry_maximum.grid(row=1, column=1, sticky="w")

        tk.Label(frame, text="Essais : ", font=("Courrier", 13)).grid(row=2, column=0, sticky="ne", pady=5)
        self.entry_essais = tk.Entry(frame, font=("Courrier", 12))
        self.entry_essais.grid(row=2, column=1, sticky="w")

        tk.Button(self.fen, text="Jouer !", font=("Courrier", 13), command=self.lancer_jeu_graphique).pack(pady=5)

        self.fen.mainloop()

    def lancer_jeu_graphique(self):

        def lancer_jeu_fonction():
            if len(entry_nbr.get()) != 0:
                if int(entry_nbr.get()) > maximum or int(entry_nbr.get()) < minimum:
                    label_reponse["text"] = f"Le nombre n'est pas entre {minimum} et {maximum}"
                else:
                    if int(entry_nbr.get()) == nbr_alea:
                        tkmsg.showinfo("Gagné !", f"Vous avez trouvé la valeur ! {nbr_alea}", parent=fen)
                        fen.destroy()
                        return 0
                    if int(entry_nbr.get()) < nbr_alea:
                        label_reponse["text"] = "C'est plus !"
                    else:
                        label_reponse["text"] = "C'est moins !"
                    self.essais -= 1
                    if self.essais <= 0:
                        tkmsg.showinfo("Plus d'essais", f"Vous avez plus d'essais, le nombre été {nbr_alea}",
                                       parent=fen)
                        fen.destroy()
                        return 0
                    label_essais["text"] = f"Il vous reste {self.essais} essai(s) !"

        minimum = int(self.entry_minimum.get())
        maximum = int(self.entry_maximum.get())
        self.essais = int(self.entry_essais.get())
        self.entry_minimum.delete(0, tk.END)
        self.entry_maximum.delete(0, tk.END)
        self.entry_essais.delete(0, tk.END)
        nbr_alea = None
        if len(str(minimum)) != 0 and len(str(maximum)) != 0 and len(str(self.essais)) != 0:
            if minimum > maximum:
                tkmsg.showerror("Valeur incorrect", "Le minimum est plus grand que le maximum", parent=self.fen)
            else:
                nbr_alea = random.randint(int(minimum), int(maximum))
                fen = tk.Toplevel()
                fen.geometry(f"400x200+{self.fen.winfo_x() - 28}+{self.fen.winfo_y() - 35}")
                fen.transient(self.fen)
                fen.grab_set()
                fen.focus_set()

                label_essais = tk.Label(fen, text=f"Vous avez {self.essais} essai(s) !", font=("Courrier", 13))
                label_essais.pack(pady=5)

                frame = tk.LabelFrame(fen, text=f"Cherchez une valeur entre {minimum} et {maximum}",
                                      font=("Courrier", 14))
                frame.pack(expand=tk.YES)

                tk.Label(frame, text="Nombre : ", font=("Courrier", 13)).grid(row=0, column=0, sticky="ne", pady=5)
                entry_nbr = tk.Entry(frame, font=("Courrier", 12))
                entry_nbr.grid(row=0, column=1, sticky="w")

                label_reponse = tk.Label(fen, font=("Courrier", 13))
                label_reponse.pack(pady=5)

                entry_nbr.bind("<Return>", lambda event: lancer_jeu_fonction())
                fen.mainloop()
        else:
            tkmsg.showinfo("Options manquantes", "Renseignez toute les options pour jouer", parent=self.fen)


if __name__ == '__main__':
    jeu = Window()
