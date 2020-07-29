import tkinter as tk 
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import mysql.connector as mc 

BD_NAME = "students"

# parametres de connexion à la base de données
ma_bd = mc.connect(
    host = "localhost",
    user = "root",
    passwd ="",
    database = BD_NAME
)

#curseur d'execution des requetes SQL
mon_curseur = ma_bd.cursor()

# mysql requetes 

# mysql requetes

LARGE_FONT = ("Verdana", 12)

# definition de l'application
class AppStudent(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.resizable(False, False)
        self.geometry("800x700")

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


        btn_1 = tk.Button(self, bg="white", text=" Etudinats ",padx=10, pady=5, command=lambda: controller.show_frame(PageEtudiants))
        btn_2 = tk.Button(self, bg="white",  text=" Notes ", padx=10, pady=5, command=lambda: controller.show_frame(PageNotes))

        btn_1.pack( side=tk.BOTTOM)
        btn_2.pack(side=tk.BOTTOM)

        btn_1.place(x=600, y=500)
        btn_2.place(x=750, y=500)


# page Notes
class PageNotes(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Page Notes", font=LARGE_FONT)
        label.pack(padx=10, pady=10)

        wrapper1 = LabelFrame(self, text="Tableau des notes")
        wrapper2 = LabelFrame(self, text="Rechercher")
        wrapper3 = LabelFrame(self, text="Bulletin Etudiant & Notes")

        wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
        wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)
        wrapper3.pack(fill="both", expand="yes", padx=20, pady=10)

         # Boutons de navigation
        btn_1 = tk.Button(self, bg="white", text=" Accueil ",padx=10, pady=6, command=lambda: controller.show_frame(PageAccueil))
        btn_2 = tk.Button(self, bg="white",  text=" Etudiants ", padx=10, pady=6, command=lambda: controller.show_frame(PageEtudiants))

        btn_1.pack( side=tk.BOTTOM)
        btn_2.pack(side=tk.BOTTOM)

        btn_1.place(x=550, y=600)
        btn_2.place(x=700, y=600)

# page Etudiants
def update(lignes):
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
    update(result)




def effacer():
    req = "SELECT Matricule, Nom, Prenoms, Sexe, Date_naissance, Lieu_naissance, Email\
             FROM Etudiants ORDER BY Nom, Prenoms ASC"
    
    mon_curseur.execute(req)
    lignes = mon_curseur.fetchall()
    update(lignes)





def ajouter_etudiant():
    pass

def supprimer_etudiant():
    matricule_etu = c1.get()

    if messagebox.askyesno(title="Suppression d'étudiant", message=" Voulez-vous supprimer cet étudiant ?"):
        req = "DELETE FROM Etudiants WHERE Matricule = "+matricule_etu
        mon_curseur.execute(req)
        effacer()
    else:
        return True

def modifier_etudiant():
    pass


class PageEtudiants(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Page Etudiants", font=LARGE_FONT)
        label.pack(padx=5, pady=6)
        ################# afficher les etudiants 

        req_all_students = "SELECT Matricule, Nom, Prenoms, Sexe, Date_naissance, Lieu_naissance, Email\
             FROM Etudiants ORDER BY Nom, Prenoms ASC"
        mon_curseur.execute(req_all_students)
        lignes = mon_curseur.fetchall()
        nb_lignes = mon_curseur.rowcount

        q = StringVar()
        c1 = StringVar()
        c2 = StringVar()
        c3 = StringVar()
        c4 = StringVar()
        c5 = StringVar()
        c6 = StringVar()
        c7 = StringVar()

        # les wrapers
        wrapper1 = LabelFrame(self, text="Liste étudiants")
        wrapper2 = LabelFrame(self, text="Rechercher")
        wrapper3 = LabelFrame(self, text="Bulletin Etudiant")

        wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
        wrapper2.pack(fill="both", expand="yes", padx=20, pady=5)
        wrapper3.pack(fill="both", expand="yes", padx=20, pady=10)

        # les treeView 
        tree = ttk.Treeview(wrapper1, columns=(1, 2, 3, 4, 5, 6, 7), show="headings", height=9)
        tree.pack(side=tk.LEFT)
        tree.place(x=0, y=0)
        tree.heading(1, text="Matricule")
        tree.heading(2, text="Nom")
        tree.heading(3, text="Prenom(s)")
        tree.heading(4, text="Genre")
        tree.heading(5, text="Date de naissance")
        tree.heading(6, text="Lieu de naissance")
        tree.heading(7, text="Email")

        #scrollBars
        yscrollbar = ttk.Scrollbar(wrapper1, orient="vertical", command=tree.yview)
        yscrollbar.pack(side=tk.RIGHT, fill="y")
       # tree.configure(yscrollcommand=yscrollbar.set)

        xscrollbar = ttk.Scrollbar(wrapper1, orient="horizontal", command=tree.xview)
        xscrollbar.pack(side=tk.BOTTOM, fill="x")
       # tree.configure(xscrollcommand=xscrollbar.set)
        # affichage 
        for ligne in lignes:
             tree.insert('', 'end', values=ligne)

        ######### barre de recherche
        label_recherche_etudiant = Label(wrapper2, text="Rechercher")
        label_recherche_etudiant.pack(side=tk.LEFT, padx = 10)


        champs_saisie1 = Entry(wrapper2, textvariable= q)
        champs_saisie1.pack(side=tk.LEFT, padx=10)
        btn_rechercher_etudiant = Button(wrapper2, text="Rechercher", command=RecherCherEtudiant)
        btn_effacer_recherche = Button(wrapper2, text="Effacer", command=effacer)
        btn_effacer_recherche.pack(side=tk.LEFT, padx=10, pady=5)
        btn_rechercher_etudiant.pack(side=tk.LEFT, padx=10, pady=5)
        
        ######### Buletin etudiant
        # champs de recuperation de données 
        label1 = Label(wrapper3, text="Matricule")
        label1.grid(row=0, column =0, padx=5, pady=3)
        champs1 = Entry(wrapper3, textvariable=c1)
        champs1.grid(row=0, column =1, padx=5, pady=3)

        label2 = Label(wrapper3, text="Nom")
        label2.grid(row=1, column =0, padx=10, pady=3)
        champs2 = Entry(wrapper3, textvariable=c1)
        champs2.grid(row=1, column =1, padx=5, pady=3)

        label3 = Label(wrapper3, text="Prenoms")
        label3.grid(row=2, column =0, padx=20, pady=3)
        champs3 = Entry(wrapper3, textvariable=c1)
        champs3.grid(row=2, column =1, padx=5, pady=3)


        label4 = Label(wrapper3, text="Sexe")
        label4.grid(row=3, column =0, padx=5, pady=3)
        champs4 = Entry(wrapper3, textvariable=c1)
        champs4.grid(row=3, column =1, padx=5, pady=3)

        label5 = Label(wrapper3, text="Date de naissance")
        label5.grid(row=4, column =0, padx=5, pady=3)
        champs5 = Entry(wrapper3, textvariable=c1)
        champs5.grid(row=4, column =1, padx=5, pady=3)

        label6 = Label(wrapper3, text="Lieu de naissance")
        label6.grid(row=5, column =0, padx=10, pady=3)
        champs6 = Entry(wrapper3, textvariable=c1)
        champs6.grid(row=5, column =1, padx=5, pady=3)

        label7 = Label(wrapper3, text="Email")
        label7.grid(row=6, column =0, padx=15, pady=3)
        champs7 = Entry(wrapper3, textvariable=c1)
        champs7.grid(row=6, column =1, padx=5, pady=3)


        # boutons de modification
        btn_ajouter = Button(wrapper3, fg="white", bg="green", text="ajouter", command=ajouter_etudiant)
        btn_modifier = Button(wrapper3, bg="white", text="modifier", command=modifier_etudiant)
        btn_supprimer = Button(wrapper3, fg="white",bg="red", text="supprimer", command=supprimer_etudiant)

        btn_ajouter.grid(row=7, column=0, padx=10, pady=5)
        btn_modifier.grid(row=7, column=1, padx=10, pady=5)
        btn_supprimer.grid(row=7, column=2, padx=10, pady=5)

        # Boutons de navigation
        btn_1 = tk.Button(self, bg="white", text=" Accueil ",padx=10, pady=6, command=lambda: controller.show_frame(PageAccueil))
        btn_2 = tk.Button(self, bg="white",  text=" Notes ", padx=10, pady=6, command=lambda: controller.show_frame(PageNotes))

        btn_1.pack( side=tk.BOTTOM)
        btn_2.pack(side=tk.BOTTOM)

        btn_1.place(x=550, y=600)
        btn_2.place(x=700, y=600)

        # fonctions 
        def get_ligne(event):
            id_ligne = tree.identify_row(event.y)
            selection = tree.item(tree.focus())
            c1.set(selection['values'][0])
            c2.set(selection['values'][1])
            c3.set(selection['values'][2])
            c4.set(selection['values'][3])
            c5.set(selection['values'][4])
            c6.set(selection['values'][5])
            c7.set(selection['values'][6])


# instanciation de l'application
app = AppStudent()
app.title("Gestions des étudiants")

# lancer l'appli
print("[INFO] Application en cours d'execution...")
app.mainloop()

print("[INFO] Fermeture de l'application. Bye !")
print ("[INFO] Application fermée")
