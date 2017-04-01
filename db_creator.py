import mysql.connector
import json
from pprint import pprint

##Lien des fichiers de config

path_ac_eq = "/hometu/etudiants/l/e/E154981H/Documents/jousselin/activite_eq.json"
path_installation = "/hometu/etudiants/l/e/E154981H/Documents/jousselin/installation.json"
path_equimepent = "/hometu/etudiants/l/e/E154981H/Documents/jousselin/equipement.json"

##Connextion with db
try:
    conn = mysql.connector.connect(host="infoweb",user="E154981H",password="E154981H", database="E154981H")
    cursor = conn.cursor()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
    conn.close()
    exit(-1)


##Cleanning tables
cursor.execute("""DELETE FROM activite WHERE 1""")
cursor.execute("""DELETE FROM equipement WHERE 1""")
cursor.execute("""DELETE FROM installations WHERE 1""")
conn.commit()

##Filling the tables
with open(path_ac_eq)  as data_file:
    fichier_activite = csv.reader(data_file);

with open(path_installation)  as data_file:
    fichier_installation = csv.reader(data_file);

with open(path_equimepent)  as data_file:
    fichier_equipement = csv.reader(data_file);

# Activité
for iterator_activite in fichier_activite:
    print(iterator_activite)
    ligne = {"ComInsee" :   iterator_activite["ComInsee"],"ComLib" :   iterator_activite["ComLib"],"EquipementId" :   iterator_activite["EquipementId"],"ActCode":  iterator_activite["ActCode"], "ActLib" :   iterator_activite["ActLib"]}
    cursor.execute("""INSERT IGNORE INTO activite (ComInsee, ComLib, EquipementId, ActCode, ActLib)  VALUES(%(ComInsee)s, %(ComLib)s, %(EquipementId)s, %(ActCode)s,%( ActLibs)s)""", ligne)
    conn.commit()
    
#equipement
for iterator_equipement in fichier_equipement:
    print(iterator_equipement)
    ligne = {"ComInsee" :   iterator_activite["ComInsee"],"InsNumeroInstall" :   iterator_equipement["InsNumeroInstall"],"InsNomInstall" :   iterator_equipement["InsNomInstall"],"EquipementId":  iterator_equipement["EquipementId"], "EquNom" :   iterator_equipement["EquNom"],"EquGpsX" :   iterator_equipement["EquGpsX"],"EquGpsY" :   iterator_equipement["EquGpsY"]}
    cursor.execute("""INSERT IGNORE INTO equipement (ComInsee, InsNumeroInstall, InsNomInstall, EquipementId, EquNom) VALUES(%(ComInsee)s, %(InsNumeroInstall)s, %(InsNomInstall)s,%(EquipementId)s, %(EquNom)s)""", ligne)
    conn.commit()

#installation
for iterator_installation in fichier_installation:
    print(iterator_installation)
    address = iterator_installation["Adresse"] + iterator_installation["ComLib"]+  iterator_installation["ComCode"]
    ligne = {"NomInstall":  iterator_installation["NomInstall"],"InsNumeroInstall":  iterator_installation["InsNumeroInstall"], "Latitude" :   iterator_installation["Latitude"], "Longitude" :   iterator_installation["Longitude"], "ComInsee" :   iterator_installation["ComInsee"], "ComCode" :   iterator_installation["ComCode"], "Adresse" :  address, "ComLib" :   iterator_installation["ComLib"]}
    cursor.execute("""INSERT IGNORE INTO installations (NomInstall,InsNumeroInstall, Latitude,Longitude,ComInsee,ComCode,Adresse,ComLib,EquGpsY,EquGpsX) VALUES(%(NomInstall)s,%(InsNumeroInstall)s, %(Latitude)s,%(Longitude)s,%(ComInsee)s,%(ComCode)s,%(Aresse)s,%(ComLib)s),%s(EquGpsY),%s(EquGpsX)""", ligne)
    conn.commit()


conn.close()



