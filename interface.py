import tkinter as tk 
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import mysql.connector as mc 

BD_NAME = "students"

"""
# parametres de connexion à la base de données
ma_bd = mc.connect(
    host = "localhost",
    user = "root",
    passwd ="password",
    database = BD_NAME
)

#curseur d'execution des requetes SQL
mon_curseur = ma_bd.cursor()

# mysql requetes 
"""

# mysql requetes

LARGE_FONT = ("Verdana", 12)

# definition de l'application
class AppStudent(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.resizable(False, False)
        self.geometry("1200x650")

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # pages
        self.frames = {}

        for F in (PageAccueil, PageEtudiants, PageNotes):
            
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(PageAccueil)


    def show_frame(self, cont):
    
        frame = self.frames[cont]
        frame.tkraise()




# page d'accueil
class PageAccueil(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Page d'accueil", font=LARGE_FONT)
        label.pack(padx=10, pady=10)


        btn_1 = tk.Button(self, text=" Etudinats ",padx=20, pady=10, command=lambda: controller.show_frame(PageEtudiants))
        btn_2 = tk.Button(self, text=" Notes ", padx=20, pady=10, command=lambda: controller.show_frame(PageNotes))

        btn_1.pack( side=tk.BOTTOM)
        btn_2.pack(side=tk.BOTTOM)

# page Notes
class PageNotes(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Page Notes", font=LARGE_FONT)
        label.pack(padx=10, pady=10)

        wrapper1 = LabelFrame(self, text="Liste étudiants & Notes")
        wrapper2 = LabelFrame(self, text="Rechercher")
        wrapper3 = LabelFrame(self, text="Données Etudiant & Notes")

        wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
        wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)
        wrapper3.pack(fill="both", expand="yes", padx=20, pady=10)

        btn_1 = tk.Button(self, text=" Accueil ", command=lambda: controller.show_frame(PageAccueil))
        btn_2 = tk.Button(self, text=" Etudiants ", command=lambda: controller.show_frame(PageEtudiants))

        btn_1.pack(side=tk.BOTTOM)
        btn_2.pack(side=tk.BOTTOM)

# page Etudiants
def renvoyer(lignes):
    tree.delete(*tree.get_children())
    for ligne in lignes:
        tree.insert('', 'end', ligne)

def RecherCherEtudiant():
    r = q.get()
    req = "SELECT Matricule, Nom, Prenoms, Genre, Date_naissance, Lieu_naissance, Email\
         FROM Etudiants \
         WHERE Prenoms LIKE '%"+q+"'% OR Nom LIKE '%"+q+"'%"
    mon_curseur.execute(req)
    result = mon_curseur.fetchall()
    renvoyer(result)


class PageEtudiants(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Page Etudiants", font=LARGE_FONT)
        label.pack(padx=10, pady=10)

        # les wrapers
        wrapper1 = LabelFrame(self, text="Liste étudiants")
        wrapper2 = LabelFrame(self, text="Rechercher")
        wrapper3 = LabelFrame(self, text="Données Etudiant")

        wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
        wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)
        wrapper3.pack(fill="both", expand="yes", padx=20, pady=10)

        # les treeView 
        tree = ttk.Treeview(wrapper1, columns=(1, 2, 3, 4, 5, 6, 7), show="headings", height=9)
        tree.pack()
        tree.heading(1, text="Matricule")
        tree.heading(2, text="Nom")
        tree.heading(3, text="Prenom(s)")
        tree.heading(4, text="Genre")
        tree.heading(5, text="Date de naissance")
        tree.heading(6, text="Lieu de naissance")
        tree.heading(7, text="Email")

        # barre de recherche
        label_recherche_etudiant = Label(wrapper2, text="Rechercher")
        label_recherche_etudiant.pack(side=tk.LEFT, padx = 10)

        q = StringVar()

        champs_saisie1 = Entry(wrapper2, textvariable= q)
        champs_saisie1.pack(side=tk.LEFT, padx=10)
        btn_rechercher_etudiant = Button(wrapper2, text="Rechercher", command=RecherCherEtudiant)
        btn_rechercher_etudiant.pack(side=tk.LEFT, padx=6)
        # donnees etudiant

       

        btn_1 = tk.Button(self, text=" Accueil ", command=lambda: controller.show_frame(PageAccueil))
        btn_2 = tk.Button(self, text=" Notes ", command=lambda: controller.show_frame(PageNotes))

        btn_1.pack()
        btn_2.pack()

# instanciation de l'application
app = AppStudent()
app.title("Gestions des étudiants")

# lancer l'appli
print("[INFO] Application en cours d'execution...")
app.mainloop()

print("[INFO] Fermeture de l'application. Bye !")
print ("[INFO] Application fermée")
