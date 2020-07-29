# importations 
import tkinter as tk
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

# requetes
req_creation_bd = f"CREATE DATABASE IF NOT EXISTS {BD_NAME}"
req_creation_table_etudiants = "CREATE TABLE IF NOT EXISTS Etudiants \
                                (Matricule varchar(255) NOT NULL, \
                                Nom varchar(255) NOT NULL, \
                                Prenoms varchar(255) NOT NULL, \
                                Sexe varchar(2) NOT NULL, \
                                Date_naissance DATE NOT NULL, \
                                Lieu_naissance varchar(255) NOT NULL, \
                                Nationalite varchar(255) NOT NULL, \
                                Telephone varchar(45), \
                                Email varchar(255) NOT NULL, \
                                PRIMARY KEY (Matricule)) \
                            "

# etudiants a ajouter a la creation
etudiants_a_ajouter = [
    ('20-EFCPC-1', 'YAO', 'marc', 'M', "1984-5-21", 'Abengourou', 'ivoirienne', '07070707', 'marc.yao@efcpc.ci'),
    ('20-EFCPC-2', 'OUATTARA', 'kanigui moussa', 'M', "1994-8-17", 'Abobo', 'ivoirienne', '07080922', 'moussa.ouattara@efcpc.ci'),
    ('20-EFCPC-3', 'LEGER', 'roxana', 'F', "1991-2-10", 'Katiola', 'ivoirienne', '01070207', 'roxana.leger@efcpc.ci'),
    ('20-EFCPC-4', 'KOUAKOU', 'elsa', 'F', "1991-3-12", 'Man', 'ivoirienne', '02151448', 'elsa.kouakou@efcpc.ci'),
    ('20-EFCPC-5', 'DJELA', 'abby faustin', 'M', "1986-10-15", 'Kong', 'ivoirienne', '05124514', 'faustin.djela@efcpc.ci'),
    
]

req_show_db = "SHOW DATABASES"
req_show_tables = "SHOW TABLES"


def inserer_etudiant(nom, 
                    prenoms, 
                    sexe, 
                    date_naissance, 
                    lieu_naissance, 
                    nationalite, 
                    telephone, 
                    email):

    req_insertion_etudiant = f"INSERT INTO Etudiants (Matricule, Nom, Prenoms, Sexe, \
                                Date_naissance, Lieu_naissance, Nationalite, Telephone, Email)\
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

    # recuperation du nombre de lignes enregistrées
    mon_curseur.execute("SELECT COUNT(*) FROM Etudiants")
    num = mon_curseur.fetchone()[0]

    matricule = f"20-EFCPC-{num + 1}"

    etudiant = (matricule, 
                nom, 
                prenoms.lower(), 
                sexe, 
                date_naissance, 
                lieu_naissance, 
                nationalite.lower(), 
                telephone, 
                email)
    try:
        mon_curseur.execute(req_insertion_etudiant, etudiant)
        ma_bd.commit()
        print("[INFO] Nouvel étudiant enregistré !")
    except Exception as e:
        print(e)


def lister_etudiants():
    req_lister_etudiants = "SELECT * FROM Etudiants ORDER BY Nom ASC"

    mon_curseur.execute(req_lister_etudiants)
    result = mon_curseur.fetchall()

    return result



def check_table(table="Etudiants"):
    mon_curseur.execute(f"USE {BD_NAME}")
    mon_curseur.execute(req_show_tables)

    tables = [table[0] for table in mon_curseur]

    if table in tables :
        print(f'Table {table} Trouvée !')
        return True
    else :
        print(f"Table {table} non trouvée")
        return False




def check_bd(nom_bd="students"):

    mon_curseur.execute(req_show_db)
    bases_de_donnees = [db[0] for db in mon_curseur]
    if nom_bd in bases_de_donnees :
        print(f'Base de données {nom_bd} Trouvée !')
        return True
    else :
        print("Base de données etudiants non trouvée")
        return False



def init_projet(etudiants_a_ajouter):
    existe = check_bd()

    if existe:
        table_existe = check_table(table="Etudiants")
        if table_existe:
            liste_etudiants = lister_etudiants()
            for etudiant in liste_etudiants:
                print(etudiant)
        else :
            print("[INFO] Creation table Etudiants...")
            try:
                mon_curseur.execute(req_creation_table_etudiants)
                # ajouter les premiers etudiants
                for etudiant in etudiants_a_ajouter:
                    mat = etudiant[0]
                    nom = etudiant[1]
                    prenoms = etudiant[2]
                    sexe = etudiant[3]
                    date_naiss = etudiant[4]
                    lieu_naiss = etudiant[5]
                    nationalite = etudiant[6]
                    telephone = etudiant[7]
                    email = etudiant[8]

                    inserer_etudiant(nom=nom, 
                                    prenoms=prenoms, 
                                    sexe=sexe, 
                                    date_naissance=date_naiss, 
                                    lieu_naissance=lieu_naiss, 
                                    nationalite=nationalite, 
                                    telephone=telephone, 
                                    email=email)
                                    
                # lister les etudiants
                #liste_etudiants = lister_etudiants()
                #for etudiant in liste_etudiants:
                    #print(etudiant)
            print("[INFO] Table Etudiants créée avec succès...")

            except Exception as e:
                print(e)

    else :
        mon_curseur.execute(req_creation_bd)
        mon_curseur.execute(f"USE {BD_NAME}")
        mon_curseur.execute(req_creation_table_etudiants)


        # ajouter les premiers etudiants
        for etudiant in etudiants_a_ajouter:
            mat = etudiant[0]
            nom = etudiant[1]
            prenoms = etudiant[2]
            sexe = etudiant[3]
            date_naiss = etudiant[4]
            lieu_naiss = etudiant[5]
            nationalite = etudiant[6]
            telephone = etudiant[7]
            email = etudiant[8]

            inserer_etudiant(nom=nom, 
                            prenoms=prenoms, 
                            sexe=sexe, 
                            date_naissance=date_naiss, 
                            lieu_naissance=lieu_naiss, 
                            nationalite=nationalite, 
                            telephone=telephone, 
                            email=email)


# initialisation du projet
init_projet(etudiants_a_ajouter=etudiants_a_ajouter)

                            

