import mysql.connector
import json
from pprint import pprint

##Lien des fichiers de config

path_ac_eq = "/hometu/etudiants/l/e/E154981H/Documents/jousselin/activite_eq.json"
path_installation = "/hometu/etudiants/l/e/E154981H/Documents/jousselin/installation.json"
path_equimepent = "/hometu/etudiants/l/e/E154981H/Documents/jousselin/equipement.json"

##Connextion with db
try:
    conn = mysql.connector.connect(host="infoweb",user="E155122L",password="E155122L", database="E155122L")
    cursor = conn.cursor()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print (err)

## recuperer les créateurs de base chez enzo

#+les changer pour avoir plus d'info sur la localisation des sites sportifs avec les adresses

##Filling the tables

with open(path_ac_eq ) as data_file:    
    fichier_activite = json.load(data_file)
with open(path_installation) as data_file:    
    fichier_installation = json.load(data_file)
with open(path_equimepent) as data_file:    
    fichier_equipement = json.load(data_file)
    

#Activité
for iterator_activite in fichier_activite['data']:
    ligne = {"ActCode":  iterator_activite["ActCode"], "ActLib" :   iterator_activite["ActLib"], "EquipementId" :   iterator_activite["EquipementId"]}
    cursor.execute("""INSERT IGNORE INTO activite (ActCode, ActLib,EquipementId) VALUES(%(ActCode)s, %(ActLib)s, %(EquipementId)s)""", ligne)
    conn.commit()


#installation
for iterator_installation in fichier_installation['data']:
    ligne = {"ComInsee":  iterator_installation["ComInsee"], "ComLib" :   iterator_installation["ComLib"]}
    cursor.execute("""INSERT IGNORE INTO commune (ComInsee, ComLib) VALUES(%(ComInsee)s, %(ComLib)s)""", ligne)
    conn.commit()

#equipement
for iterator_equipement in fichier_equipement['data']:
    ligne = {"EquipementId":  iterator_equipement["EquipementId"], "EquNom" :   iterator_equipement["EquNom"]}
    cursor.execute("""INSERT IGNORE INTO equipement (EquipementId, EquNom) VALUES(%(EquipementId)s, %(EquNom)s)""", ligne)
    conn.commit()
   




conn.close()