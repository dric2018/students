import tkinter as tk 
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image

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

LARGE_FONT = ("Times", 12)


# definition de l'application
class AppStudent(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.resizable(False, False)
        self.geometry("900x700")

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

        l = Label(self, bg="gold", text = " Etu-GES ", font=("Times", 70))
        l.place(x=240, y=200)

        # Boutons de navigation
        btn_1 = tk.Button(self, bg="white", text=" Notes ",padx=25, pady=6, command=lambda: controller.show_frame(PageNotes))
        btn_2 = tk.Button(self, bg="white",  text=" Etudiants ", padx=20, pady=6, command=lambda: controller.show_frame(PageEtudiants))

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

        # wrappers
        wrapper1 = LabelFrame(self, text="Tableau des notes")
        wrapper2 = LabelFrame(self, text="Rechercher")
        wrapper3 = LabelFrame(self, text="Bulletin Etudiant & Notes")

        wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
        wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)
        wrapper3.pack(fill="both", expand="yes", padx=20, pady=10)

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
        self.c10 = tk.StringVar()
        self.c11 = tk.StringVar()
        self.c12 = tk.StringVar()

        # fonctions
        def update(lignes):
            tree.delete(*tree.get_children())
            for ligne in lignes:
                tree.insert('', 'end', values=ligne)




        def RecherNote():
            req = f"SELECT SELECT Note_id, Matricule_Etud, etudiants.Nom, etudiants.Prenoms, \
            etudiants.Sexe, etudiants.Date_naissance, etudiants.Lieu_naissance, Note_1, Note_2, Note_3, Note_4, Note_5 \
            FROM Notes \
            WHERE etudiants.Prenoms LIKE '%{self.q.get().lower()}%' OR etudiants.Nom LIKE '%{self.q.get().upper()}%' \
            INNER JOIN `etudiants` ON notes.Matricule_Etud = etudiants.Matricule \
            ORDER BY Matricule_Etud ASC"            
            
            mon_curseur.execute(req)
            result = mon_curseur.fetchall()
            update(result)


        def effacer():

            req_all_notes = "SELECT Note_id, Matricule_Etud, etudiants.Nom, etudiants.Prenoms, \
            etudiants.Sexe, etudiants.Date_naissance, etudiants.Lieu_naissance, Note_1, Note_2, Note_3, Note_4, Note_5 \
            FROM Notes \
            INNER JOIN `etudiants` ON notes.Matricule_Etud = etudiants.Matricule \
            ORDER BY Matricule_Etud ASC"
            
            mon_curseur.execute(req_all_notes)
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
            self.c9.set("")
            self.c10.set("")
            self.c11.set("")
            self.c12.set("")
            self.c8.set("")


        def tous_les_champs_ok():

            note1 = self.c2.get()
            note_2 = self.c3.get()
            note_3 = self.c4.get()
            note_4 = self.c5.get()
            note_5 = self.c6.get()
            matricule = self.c1.get()
            
            ch = [note1, note2, note3, note4, note5]
            for champ in ch:
                if champ == "" or champ == " ":
                    return False
                else :
                    return True

        def ajouter_etudiant():
            
            if tous_les_champs_ok() and messagebox.askyesno(title="Ajout note", message=" Voulez-vous ajouter cette notation ?"):
                
                req_insertion_note = f"INSERT INTO notes (Matricule_Etud, Note_1, Note_2, Note_3, Note_4, Note_5)\
                                VALUES (%s, %s, %s, %s, %s, %s)"

                try:
                    matricule = self.c7.get()
                    note1 = self.c2.get()
                    note_2 = self.c3.get()
                    note_3 = self.c4.get()
                    note_4 = self.c5.get()
                    note_5 = self.c6.get()

                    new_note = (matricule, note1, note2, note3, note4, note5)
                    try:
                        mon_curseur.execute(req_insertion_note, new_note)
                        ma_bd.commit()
                        print("[INFO] Nouvelle note enregistrée !")

                    except Exception as e:
                        print(e)
                    print("[INFO] Nouvelle notation enregistrée !")
                    messagebox.showinfo(title="Enregistrement note", message=f"La notation de l'etudiant {matricule} a été enregistrée !")
                    
                    ma_bd.commit()
                    effacer()

                except Exception as e:
                    print("[INFO]", e)
                    messagebox.showerror(title="Enregistrement note", message=f"Erreur lors de l'enregistrement !")

            else:
                messagebox.showerror(title="Enregistrement note", message=f"Erreur lors de l'enregistrement !")
                messagebox.showwarning(title="Enregistrement note", message=f"Assurez-vous que tous les champs sont bien renseignés !")
                return True


        def supprimer_note():
            matricule = self.c1.get()

            if tous_les_champs_ok() and messagebox.askyesno(title="Suppression de note", message=" Voulez-vous supprimer cet étudiant ?"):
                req = "DELETE FROM Etudiants WHERE Matricule = %s"
                mon_curseur.execute(req, (matricule,))
                ma_bd.commit()

                messagebox.showinfo(title="Suppression de note", message=f"Notes supprimées !")
                effacer()
            else:
                messagebox.showerror(title="Suppression de note", message=f"l'opération a échoué !")
                messagebox.showwarning(title="Suppression de note", message=f"Assurez-vous que tous les champs sont bien renseignés !")
                return True


        def modifier_note():

            if tous_les_champs_ok() and messagebox.askyesno(title="Modification de note", message=" Voulez-vous modifier les notes de cet étudiant ?"):

                note_id = self.c1.get()
                note_1 = self.c2.get()
                note_2 = self.c3.get()
                note_3 = self.c4.get()
                note_4 = self.c5.get()
                note_5 = self.c6.get()
                matricule = self.c7.get()


                new_note = (matricule, note1, note2, note3, note4, note5)


                req = "UPDATE Etudiants SET Nom=%s, Prenoms=%s, Sexe=%s, Date_naissance=%s, Lieu_naissance=%s, Nationalite=%s, Telephone=%s, Email=%s WHERE Matricule = %s"
                mon_curseur.execute(req, new_note)
                ma_bd.commit()

                # afficher un pop-up de succes
                messagebox.showinfo(title="Modification de notes ", message="Modification enregistrée !")
                effacer()
                
                print("[INFO] Modification étudiant enregistrée !")

            else:
                messagebox.showerror(title="Modification de notes", message="La modification a échoué !")
                messagebox.showwarning(title="Modification de notes", message=f"Assurez-vous que tous les champs sont renseignés !")
                return True


        ################# afficher les  notes 

        req_bulletin = "SELECT etudiants.Matricule, etudiants.Nom, etudiants.Prenoms, etudiants.Sexe, etudiants.Date_naissance, \
            etudiants.Lieu_naissance, etudiants.Nationalite, etudiants.Telephone, etudiants.Email, notes.Note_1, notes.Note_2, \
            notes.Note_3, notes.Note_4, notes.Note_5 \
            FROM `notes` \
            INNER JOIN `etudiants` ON notes.Matricule_Etud = etudiants.Matricule "

        
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
            self.c8.set(selection['values'][2])
            self.c9.set(selection['values'][8])
            self.c10.set(selection['values'][9])
            self.c11.set(selection['values'][10])
            self.c12.set(selection['values'][11])

            print(f"[INFO] Ligne {id_ligne} sélectionnée")

        # le treeView 
        tree = ttk.Treeview(wrapper1, columns=(1, 2, 3, 4, 5, 6, 7, 8,9,10,11,12), 
                            show="headings", height=5)

        tree.pack(side=tk.LEFT)
        tree.place(x=0, y=0)

        style = ttk.Style(tree)
        style.configure("Treeview", rowheight=15)
        tree.heading("#0", text="")
        tree.heading("#1", text="NoteID")
        tree.heading("#2", text="Matricule")
        tree.heading("#3", text="Nom")
        tree.heading("#4", text="Prenom(s)")
        tree.heading("#5", text="Sexe")
        tree.heading("#6", text="Né le")
        tree.heading("#7", text="A")        
        tree.heading("#8", text="Note 1")
        tree.heading("#9", text="Note 2")
        tree.heading("#10", text="Note 3")
        tree.heading("#11", text="Note 4")
        tree.heading("#12", text="Note 5")

        # taille des colonnes 
        tree.column("#1", width=50, minwidth=50, stretch=False)
        tree.column("#2", width=90, minwidth=90, stretch=False)
        tree.column("#3", width=90, minwidth=90, stretch=False)
        tree.column("#4", width=120, minwidth=120, stretch=False)
        tree.column("#5", width=50, minwidth=50, stretch=False)
        tree.column("#6", width=70, minwidth=70, stretch=False)
        tree.column("#7", width=113, minwidth=113, stretch=False)
        tree.column("#8", width=50, minwidth=50, stretch=False)
        tree.column("#9", width=50, minwidth=50, stretch=False)
        tree.column("#10", width=50, minwidth=50, stretch=False)
        tree.column("#11", width=50, minwidth=50, stretch=False)
        tree.column("#12", width=50, minwidth=50, stretch=False)

        #scrollBars
        yscrollbar = ttk.Scrollbar(wrapper1, orient="vertical", command=tree.yview)
        yscrollbar.pack(side=tk.RIGHT, fill="y")

        xscrollbar = ttk.Scrollbar(wrapper1, orient="horizontal", command=tree.xview)
        xscrollbar.pack(side=tk.BOTTOM, fill="x")

        tree.configure(yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set)

        req_all_notes = "SELECT Note_id, Matricule_Etud, etudiants.Nom, etudiants.Prenoms, \
            etudiants.Sexe, etudiants.Date_naissance, etudiants.Lieu_naissance, Note_1, Note_2, Note_3, Note_4, Note_5 \
            FROM Notes \
            INNER JOIN `etudiants` ON notes.Matricule_Etud = etudiants.Matricule \
            ORDER BY Matricule_Etud ASC"

        mon_curseur.execute(req_all_notes)
        lignes = mon_curseur.fetchall()
        nb_lignes = mon_curseur.rowcount
        # affichage de la liste
        for ligne in lignes:
             tree.insert('', 'end', values=ligne)

        # en cas de double-click sur un éleve
        tree.bind("<Double-1>", get_ligne)

        ######### barre de recherche
        label_recherche_etudiant = Label(wrapper2, text="Rechercher")
        label_recherche_etudiant.pack(side=tk.LEFT, padx = 10)


        champs_saisie1 = Entry(wrapper2, textvariable= self.q)
        champs_saisie1.pack(side=tk.LEFT, padx=10, ipadx=30)
        btn_rechercher_etudiant = Button(wrapper2, bg="white", text="Rechercher", command=RecherNote)
        
        btn_effacer_recherche = Button(wrapper2, bg="white", text="Effacer", command=effacer)
        btn_effacer_recherche.pack(side=tk.LEFT, padx=20, pady=10)
        btn_rechercher_etudiant.pack(side=tk.LEFT, padx=10, pady=5)  

        #################
        ######## bulletin 
        #      
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

        label7 = Label(wrapper3, text="Note 1")
        label7.grid(row=6, column =0, padx=5, pady=3)
        champs7 = Entry(wrapper3, textvariable=self.c7)
        champs7.grid(row=6, column =1, padx=5, pady=3, ipadx=30)

        label8 = Label(wrapper3, text="Note 2")
        label8.grid(row=7, column =0, padx=10, pady=3)
        champs8 = Entry(wrapper3, textvariable=self.c8)
        champs8.grid(row=7, column =1, padx=5, pady=3, ipadx=30)

        label9 = Label(wrapper3, text="Note 3")
        label9.grid(row=8, column =0, padx=15, pady=3)
        champs9 = Entry(wrapper3, textvariable=self.c9)
        champs9.grid(row=8, column =1, padx=5, pady=3, ipadx=30)        

        label8 = Label(wrapper3, text="Note 4")
        label8.grid(row=9, column =0, padx=10, pady=3)
        champs8 = Entry(wrapper3, textvariable=self.c10)
        champs8.grid(row=9, column =1, padx=5, pady=3, ipadx=30)

        label9 = Label(wrapper3, text="Note 5")
        label9.grid(row=10, column =0, padx=15, pady=3)
        champs9 = Entry(wrapper3, textvariable=self.c11)
        champs9.grid(row=10, column =1, padx=5, pady=3, ipadx=30)  

        # Boutons de navigation
        btn_1 = tk.Button(self, bg="white", text=" Etudiants ",padx=25, pady=6, command=lambda: controller.show_frame(PageEtudiants))
        btn_2 = tk.Button(self, bg="white",  text=" Accueil ", padx=20, pady=6, command=lambda: controller.show_frame(PageAccueil))

        btn_1.pack( side=tk.BOTTOM)
        btn_2.pack(side=tk.BOTTOM)

        btn_1.place(x=325, y=650)
        btn_2.place(x=450, y=650)





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

        wrapper1.pack(fill="both", expand="yes", padx=20, pady=5)
        wrapper2.pack(fill="both", expand="yes", padx=20, pady=5)
        wrapper3.pack(fill="both", expand="yes", padx=20, pady=10)

        # le treeView 
        tree = ttk.Treeview(wrapper1, columns=(1, 2, 3, 4, 5, 6, 7, 8, 9), show="headings", height=5)
        tree.pack(side=tk.LEFT)
        tree.place(x=0, y=0)

        style = ttk.Style(tree)
        style.configure("Treeview", rowheight=15)
        tree.heading("#0", text="")
        tree.heading("#1", text="Matricule")
        tree.heading("#2", text="Nom")
        tree.heading("#3", text="Prenom(s)")
        tree.heading("#4", text="Sexe")
        tree.heading("#5", text="Date de naissance")
        tree.heading("#6", text="Lieu de naissance")
        tree.heading("#7", text="Nationalité")
        tree.heading("#8", text="Telephone")
        tree.heading("#9", text="Email")

        # taille des colonnes 
        tree.column("#1", width=75, minwidth=75, stretch=False)
        tree.column("#2", width=90, minwidth=90, stretch=False)
        tree.column("#3", width=130, minwidth=130, stretch=False)
        tree.column("#4", width=33, minwidth=33, stretch=False)
        tree.column("#5", width=105, minwidth=105, stretch=False)
        tree.column("#6", width=100, minwidth=100, stretch=False)
        tree.column("#7", width=80, minwidth=80, stretch=False)
        tree.column("#8", width=70, minwidth=70, stretch=False)
        tree.column("#9", width=150, minwidth=100, stretch=False)

        #scrollBars
        yscrollbar = ttk.Scrollbar(wrapper1, orient="vertical", command=tree.yview)
        yscrollbar.pack(side=tk.RIGHT, fill="y")

        xscrollbar = ttk.Scrollbar(wrapper1, orient="horizontal", command=tree.xview)
        xscrollbar.pack(side=tk.BOTTOM, fill="x")

        tree.configure(yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set)


        # affichage de la liste
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
        btn_effacer_recherche.pack(side=tk.LEFT, padx=20, pady=10)
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

        btn_ajouter.grid(row=0, column=5, padx=10, pady=5, ipadx=15)
        btn_modifier.grid(row=1, column=5, padx=10, pady=5, ipadx=10)
        btn_supprimer.grid(row=2, column=5, padx=10, pady=5, ipadx=10)

        # Boutons de navigation
        btn_1 = tk.Button(self, bg="white", text=" Accueil ",padx=25, pady=6, command=lambda: controller.show_frame(PageAccueil))
        btn_2 = tk.Button(self, bg="white",  text=" Notes ", padx=20, pady=6, command=lambda: controller.show_frame(PageNotes))

        btn_1.pack( side=tk.BOTTOM)
        btn_2.pack(side=tk.BOTTOM)

        btn_1.place(x=300, y=650)
        btn_2.place(x=425, y=650)

        



# instanciation de l'application
app = AppStudent()
app.title("Gestions des étudiants")


# lancer l'appli
print("[INFO] Application en cours d'execution...")
app.mainloop()

print("[INFO] Fermeture de l'application. Bye !")
print ("[INFO] Application fermée")
