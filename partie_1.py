# importations 
import tkinter as tk
import mysql.connector as mc

BD_NAME = "students"


# parametres de connexion à la base de données
ma_bd = mc.connect(
    host = "localhost",
    user = "root",
    passwd ="password",
    database = BD_NAME
)

#curseur d'execution des requetes SQL
mon_curseur = ma_bd.cursor()

# requetes
#Table Etudiants
req_creation = f"CREATE DATABASE IF NOT EXISTS {BD_NAME}"
# etudiants a ajouter a la creation
etudiant_a_ajouter = [
    ('20-EFCPC-1', 'YAO', 'marc', 'M', "1984, 5, 21", 'Abengourou', 'ivoirienne', '07070707', 'marc.yao@efcpc.ci'),
    ('20-EFCPC-2', 'OUATTARA', 'kanigui moussa', 'M', "1994, 8, 17", 'Abobo', 'ivoirienne', '07080922', 'moussa.ouattara@efcpc.ci'),
    ('20-EFCPC-3', 'LEGER', 'roxana', 'F', "1991, 2, 10", 'Katiola', 'ivoirienne', '01070207', 'roxana.leger@efcpc.ci'),
    ('20-EFCPC-4', 'KOUAKOU', 'elsa', 'F', "1991, 3, 12", 'Man', 'ivoirienne', '02151448', 'elsa.kouakou@efcpc.ci'),
    ('20-EFCPC-5', 'DJELA', 'abby faustin', 'M', "1986, 10, 15", 'Kong', 'ivoirienne', '05124514', 'faustin.djela@efcpc.ci'),
    
]

req_show = "SHOW DATABASES"

def inserer_etudiant(nom, 
                    prenoms, 
                    sexe, 
                    date_naissance, 
                    lieu_naissance, 
                    nationalite, 
                    telephone, 
                    email):

    req_insertion_etudiant = f"INSERT INTO Etudiants (\
        Matricule, Nom, Prenoms, Sexe, Date_naissance, Lieu_naissance, Nationalite, Telephone, Email)\
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

    # recuperation du nombre de lignes enregistrées
    mon_curseur.execute("SELECT COUNT(*) FROM Etudiants")
    num = mon_curseur.fetchone()[0]

    matricule = f"20-EFCPC-{num}"

    etudiant = (matricule, 
                nom, 
                prenoms, 
                sexe, 
                date_naissance, 
                lieu_naissance, 
                nationalite, 
                telephone, 
                email)

    mon_curseur.execute(req_insertion_etudiant, etudiant)
    ma_bd.commit()


def lister_etudiants():
    req_lister_etudiants = "SELECT * FROM Etudiants ORDER BY Nom DESC"

    mon_curseur.execute(req_lister_etudiants)
    result = mon_curseur.fetchall()

    return result


def check_bd(nom_bd="students"):

    mon_curseur.execute(req_show)
    bases_de_donnees = [db[0] for db in mon_curseur]
    print(bases_de_donnees)
    if nom_bd in bases_de_donnees :
        print(f'Base de données {nom_bd} Trouvée !')

        return True
    else :
        print("Base de données etudiants non trouvée")
        return False

existe = check_bd()

if existe:
    liste_etudiants = lister_etudiants()
    for etudiant in liste_etudiants:
        print(etudiant)

else :
    mon_curseur.execute(req_creation)
    mon_curseur.execute(req_show)
    bases_de_donnees = [db[0] for db in mon_curseur]

    # ajouter les premiers etudiants
    for etudiant in etudiant_a_ajouter:
        mat = etudiant[0]
        nom = etudiant[1]
        prenoms = etudiant[2]
        sexe = etudiant[3]
        date_naiss = etudiant[4]
        lieu_naiss = etudiant[5]
        nationalite = etudiant[6]
        telephone = etudiant[7]
        email = etudiant[8]
        
        inserer_etudiant()
        print()
        break