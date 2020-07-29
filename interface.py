import tkinter as tk 
from tkinter import *


LARGE_FONT = ("Verdana", 12)

# definition de l'application
class AppStudent(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.resizable = (False, False)

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


        btn_1 = tk.Button(self, text=" Etudinats ", command=lambda: controller.show_frame(PageEtudiants))
        btn_2 = tk.Button(self, text=" Notes ", command=lambda: controller.show_frame(PageNotes))

        btn_1.pack()
        btn_2.pack()

# page Notes
class PageNotes(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Page Notes", font=LARGE_FONT)
        label.pack(padx=10, pady=10)


        btn_1 = tk.Button(self, text=" Accueil ", command=lambda: controller.show_frame(PageAccueil))
        btn_2 = tk.Button(self, text=" Etudiants ", command=lambda: controller.show_frame(PageEtudiants))

        btn_1.pack()
        btn_2.pack()

# page Etudiants
class PageEtudiants(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Page Etudiants", font=LARGE_FONT)
        label.pack(padx=10, pady=10)


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
