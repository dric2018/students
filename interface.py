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
        label = tk.Label(self, bg="gold", text = "Page d'accueil", font=LARGE_FONT)
        label.pack(padx=10, pady=10)

        l = Label(self, bg="gold", text = " Etu-GES ", font=("Times", 50))
        l.place(x=280, y=250)

        btn_1 = tk.Button(self, bg="white", text=" Etudiants ",padx=10, pady=5, command=lambda: controller.show_frame(PageEtudiants))
        btn_2 = tk.Button(self, bg="white",  text=" Notes ", padx=10, pady=5, command=lambda: controller.show_frame(PageNotes))

        btn_1.pack( side=tk.BOTTOM)
        btn_2.pack(side=tk.BOTTOM)

        btn_1.place(x=325, y=500)
        btn_2.place(x=425, y=500)


# page Notes
class PageNotes(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, bg="gold", text = "Page Notes", font=LARGE_FONT)
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

        btn_1.place(x=325, y=650)
        btn_2.place(x=425, y=650)





class PageEtudiants(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, bg="gold", text = "Page Etudiants", font=LARGE_FONT)
        label.pack(padx=5, pady=6)

        self.q = tk.StringVar() # champ rechercher
        self.c1 = tk.StringVar()
        self.c2 = tk.StringVar()
        self.c3 = tk.StringVar()
        self.c4 = tk.StringVar()
        self.c5 = tk.StringVar()
        self.c6 = tk.StringVar()
        self.c7 = tk.StringVar()
        self.c8 = tk.StringVar()
        self.c9 = tk.StringVar()

        # fonctions
        # page Etudiants
        def update(lignes):
            tree.delete(*tree.get_children())
            for ligne in lignes:
                tree.insert('', 'end', values=ligne)




        def RecherCherEtudiant():
            r = self.q.get()
            req = f"SELECT * FROM Etudiants \
                WHERE Prenoms LIKE '%{self.q.get().lower()}%' OR Nom LIKE '%{self.q.get().upper()}%' ORDER BY Nom, Prenoms ASC"
            
            mon_curseur.execute(req)
            result = mon_curseur.fetchall()
            update(result)




        def effacer():

            req = "SELECT * FROM Etudiants ORDER BY Nom, Prenoms ASC"
            
            mon_curseur.execute(req)
            lignes = mon_curseur.fetchall()
            update(lignes)
            self.q.set("")
            self.c1.set("")
            self.c2.set("")
            self.c3.set("")
            self.c4.set("")
            self.c5.set("")
            self.c6.set("")
            self.c7.set("")
            self.c8.set("")
            self.c9.set("")


        def tous_les_champs_ok():

            matricule = self.c1.get()
            nom = self.c2.get()
            prenoms = self.c3.get()
            sexe = self.c4.get()
            date_naissance = self.c5.get()
            lieu_naissance = self.c6.get()
            nationalite = self.c7.get()
            telephone = self.c8.get()
            email = self.c9.get()

            ch = [matricule, nom, prenoms, sexe, date_naissance, lieu_naissance, nationalite, telephone, email]
            for champ in ch:
                if champ == "" or champ == " ":
                    return False
                else :
                    return True

        def ajouter_etudiant():
            
            if tous_les_champs_ok() and messagebox.askyesno(title="Ajout d'étudiant", message=" Voulez-vous ajouter cet étudiant ?"):
                
                req_insertion_etudiant = f"INSERT INTO Etudiants (Matricule, Nom, Prenoms, Sexe, \
                                                Date_naissance, Lieu_naissance, Nationalite, Telephone, Email)\
                                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                
                try:
                    matricule = self.c1.get()
                    nom = self.c2.get()
                    prenoms = self.c3.get()
                    sexe = self.c4.get()
                    date_naissance = self.c5.get()
                    lieu_naissance = self.c6.get()
                    nationalite = self.c7.get()
                    telephone = self.c8.get()
                    email = self.c9.get()

                    etudiant = (matricule, 
                                    nom.upper(), 
                                    prenoms.lower(), 
                                    sexe, 
                                    date_naissance, 
                                    lieu_naissance, 
                                    nationalite.lower(), 
                                    telephone, 
                                    email)


                    mon_curseur.execute(req_insertion_etudiant, etudiant)
                    print("[INFO] Nouvel étudiant enregistré !")
                    messagebox.showinfo(title="Enregistrement etudiant", message=f"Etudiant {matricule} enregistré !")
                    
                    ma_bd.commit()
                    effacer()

                except Exception as e:
                    print("[INFO]", e)
                    messagebox.showerror(title="Enregistrement etudiant", message=f"Erreur lors de l'enregistrement !")

            else:
                messagebox.showerror(title="Enregistrement etudiant", message=f"Erreur lors de l'enregistrement !")
                messagebox.showwarning(title="Enregistrement etudiant", message=f"Assurez-vous que tous les champs sont renseignés !")
                return True


        def supprimer_etudiant():
            matricule = self.c1.get()

            if tous_les_champs_ok() and messagebox.askyesno(title="Suppression d'étudiant", message=" Voulez-vous supprimer cet étudiant ?"):
                req = "DELETE FROM Etudiants WHERE Matricule = %s"
                mon_curseur.execute(req, (matricule,))
                ma_bd.commit()

                messagebox.showinfo(title="Suppression d'étudiants", message=f"Etudiant {matricule} définitivement supprimé !")
                effacer()
            else:
                messagebox.showerror(title="Suppression d'étudiants", message=f"l'opération a échoué !")
                messagebox.showwarning(title="Suppression d'étudiants", message=f"Assurez-vous que tous les champs sont renseignés !")
                return True


        def modifier_etudiant():

            if tous_les_champs_ok() and messagebox.askyesno(title="Modification d'étudiant", message=" Voulez-vous modifier cet étudiant ?"):

                matricule = self.c1.get()
                nom = self.c2.get()
                prenoms = self.c3.get()
                sexe = self.c4.get()
                date_naissance = self.c5.get()
                lieu_naissance = self.c6.get()
                nationalite = self.c7.get()
                telephone = self.c8.get()
                email = self.c9.get()

                etudiant = (nom.upper(), 
                                prenoms.lower(), 
                                sexe, 
                                date_naissance, 
                                lieu_naissance.lower(), 
                                nationalite.lower(), 
                                telephone, 
                                email, 
                                matricule)

                req = "UPDATE Etudiants SET Nom=%s, Prenoms=%s, Sexe=%s, Date_naissance=%s, Lieu_naissance=%s, Nationalite=%s, Telephone=%s, Email=%s WHERE Matricule = %s"
                mon_curseur.execute(req, etudiant)
                ma_bd.commit()

                # afficher un pop-up de succes
                messagebox.showinfo(title="Modification d'étudiants", message="Modification enregistrée !")
                effacer()
                
                print("[INFO] Modification étudiant enregistrée !")

            else:
                messagebox.showerror(title="Modification d'étudiants", message="La modification a échoué !")
                messagebox.showwarning(title="Modification d'étudiants", message=f"Assurez-vous que tous les champs sont renseignés !")
                return True


        ################# afficher les etudiants 

        req_all_students = "SELECT * FROM Etudiants ORDER BY Nom, Prenoms ASC"
        mon_curseur.execute(req_all_students)
        lignes = mon_curseur.fetchall()
        nb_lignes = mon_curseur.rowcount

        
        # fonctions 
        def get_ligne(event):
            id_ligne = tree.identify_row(event.y)
            selection = tree.item(tree.focus())
            self.c1.set(selection['values'][0])
            self.c2.set(selection['values'][1])
            self.c3.set(selection['values'][2])
            self.c4.set(selection['values'][3])
            self.c5.set(selection['values'][4])
            self.c6.set(selection['values'][5])
            self.c7.set(selection['values'][6])
            self.c8.set(selection['values'][7])
            self.c9.set(selection['values'][8])
            print(f"[INFO] Ligne {id_ligne} sélectionnée")
        # les wrapers
        wrapper1 = LabelFrame(self, text="Liste étudiants")
        wrapper2 = LabelFrame(self, text="Rechercher")
        wrapper3 = LabelFrame(self, text="Infos Etudiant")

        wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
        wrapper2.pack(fill="both", expand="yes", padx=20, pady=5)
        wrapper3.pack(fill="both", expand="yes", padx=20, pady=10)

        # le treeView 
        tree = ttk.Treeview(wrapper1, columns=(1, 2, 3, 4, 5, 6, 7, 8, 9), show="headings", height=10)
        tree.pack(side=tk.LEFT)
        tree.place(x=0, y=0)
        tree.heading(0, text="")
        tree.heading(1, text="Matricule")
        tree.heading(2, text="Nom")
        tree.heading(3, text="Prenom(s)")
        tree.heading(4, text="Sexe")
        tree.heading(5, text="Date de naissance")
        tree.heading(6, text="Lieu de naissance")
        tree.heading(7, text="Nationalité")
        tree.heading(8, text="Telephone")
        tree.heading(9, text="Email")

        # taille des colonnes 
        tree.column("#1", width=80, minwidth=80, stretch=False)
        tree.column("#2", width=80, minwidth=80, stretch=False)
        tree.column("#3", width=100, minwidth=100, stretch=False)
        tree.column("#4", width=33, minwidth=33, stretch=False)
        tree.column("#5", width=100, minwidth=100, stretch=False)
        tree.column("#6", width=100, minwidth=100, stretch=False)
        tree.column("#7", width=80, minwidth=80, stretch=False)
        tree.column("#8", width=80, minwidth=80, stretch=False)
        tree.column("#9", width=80, minwidth=80, stretch=False)

        #scrollBars
        yscrollbar = ttk.Scrollbar(wrapper1, orient="vertical", command=tree.yview)
        yscrollbar.pack(side=tk.RIGHT, fill="y")

        xscrollbar = ttk.Scrollbar(wrapper1, orient="horizontal", command=tree.xview)
        xscrollbar.pack(side=tk.BOTTOM, fill="x")
        tree.configure(yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set)


        # affichage 
        for ligne in lignes:
             tree.insert('', 'end', values=ligne)

        # en cas de double-click sur un éleve
        tree.bind("<Double-1>", get_ligne)

        ######### barre de recherche
        label_recherche_etudiant = Label(wrapper2, text="Rechercher")
        label_recherche_etudiant.pack(side=tk.LEFT, padx = 10)


        champs_saisie1 = Entry(wrapper2, textvariable= self.q)
        champs_saisie1.pack(side=tk.LEFT, padx=10, ipadx=30)
        btn_rechercher_etudiant = Button(wrapper2, bg="white", text="Rechercher", command=RecherCherEtudiant)
        
        btn_effacer_recherche = Button(wrapper2, bg="white", text="Effacer", command=effacer)
        btn_effacer_recherche.pack(side=tk.LEFT, padx=10, pady=5)
        btn_rechercher_etudiant.pack(side=tk.LEFT, padx=10, pady=5)
        
        ######### Buletin etudiant
        # champs de recuperation de données 
        label1 = Label(wrapper3, text="Matricule")
        label1.grid(row=0, column =0, padx=5, pady=3)
        champs1 = Entry(wrapper3, textvariable=self.c1)
        champs1.grid(row=0, column =1, padx=10, pady=3, ipadx=30)


        label2 = Label(wrapper3, text="Nom")
        label2.grid(row=1, column =0, padx=10, pady=3)
        champs2 = Entry(wrapper3, textvariable=self.c2)
        champs2.grid(row=1, column =1, padx=5, pady=3, ipadx=30)

        label3 = Label(wrapper3, text="Prenoms")
        label3.grid(row=2, column =0, padx=20, pady=3)
        champs3 = Entry(wrapper3, textvariable=self.c3)
        champs3.grid(row=2, column =1, padx=5, pady=3, ipadx=30)


        label4 = Label(wrapper3, text="Sexe")
        label4.grid(row=3, column =0, padx=5, pady=3)
        champs4 = Entry(wrapper3, textvariable=self.c4)
        champs4.grid(row=3, column =1, padx=5, pady=3, ipadx=30)

        label5 = Label(wrapper3, text="Date de naissance")
        label5.grid(row=4, column =0, padx=5, pady=3)
        champs5 = Entry(wrapper3, textvariable=self.c5)
        champs5.grid(row=4, column =1, padx=5, pady=3, ipadx=30)

        label6 = Label(wrapper3, text="Lieu de naissance")
        label6.grid(row=5, column =0, padx=10, pady=3)
        champs6 = Entry(wrapper3, textvariable=self.c6)
        champs6.grid(row=5, column =1, padx=5, pady=3, ipadx=30)

        label7 = Label(wrapper3, text="Nationalité")
        label7.grid(row=6, column =0, padx=5, pady=3)
        champs7 = Entry(wrapper3, textvariable=self.c7)
        champs7.grid(row=6, column =1, padx=5, pady=3, ipadx=30)

        label8 = Label(wrapper3, text="Telephone")
        label8.grid(row=7, column =0, padx=10, pady=3)
        champs8 = Entry(wrapper3, textvariable=self.c8)
        champs8.grid(row=7, column =1, padx=5, pady=3, ipadx=30)

        label9 = Label(wrapper3, text="Email")
        label9.grid(row=8, column =0, padx=15, pady=3)
        champs9 = Entry(wrapper3, textvariable=self.c9)
        champs9.grid(row=8, column =1, padx=5, pady=3, ipadx=30)


        # boutons de modification
        btn_ajouter = Button(wrapper3, fg="white", bg="green", text="ajouter", command=ajouter_etudiant)
        btn_modifier = Button(wrapper3, bg="white", text="modifier", command=modifier_etudiant)
        btn_supprimer = Button(wrapper3, fg="white",bg="red", text="supprimer", command=supprimer_etudiant)

        btn_ajouter.grid(row=9, column=0, padx=10, pady=5)
        btn_modifier.grid(row=9, column=1, padx=10, pady=5)
        btn_supprimer.grid(row=9, column=2, padx=10, pady=5)

        # Boutons de navigation
        btn_1 = tk.Button(self, bg="white", text=" Accueil ",padx=10, pady=6, command=lambda: controller.show_frame(PageAccueil))
        btn_2 = tk.Button(self, bg="white",  text=" Notes ", padx=10, pady=6, command=lambda: controller.show_frame(PageNotes))

        btn_1.pack( side=tk.BOTTOM)
        btn_2.pack(side=tk.BOTTOM)

        btn_1.place(x=325, y=650)
        btn_2.place(x=425, y=650)

        



# instanciation de l'application
app = AppStudent()
app.title("Gestions des étudiants")


# lancer l'appli
print("[INFO] Application en cours d'execution...")
app.mainloop()

print("[INFO] Fermeture de l'application. Bye !")
print ("[INFO] Application fermée")
