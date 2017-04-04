import mysql.connector
from mysql.connector import errorcode
import csv
from pprint import pprint


##Lien des fichiers de config
def get_path():
    path_ac_eq = "load_base/activite_eq.csv"
    path_installation = "load_base/installation.csv"
    path_equimepent = "load_base/equipement.csv"
    return [path_ac_eq, path_installation, path_equimepent]


##Connextion with db













##Filling the tables
def parse_activite():
    cursor.execute("""DELETE FROM activite WHERE 1""")
    conn.commit()
    with open(get_path()[0])  as data_file:
        fichier_activite = csv.DictReader(data_file);
        # Activité
        for iterator_activite in fichier_activite:
            ligne = [iterator_activite["ComInsee"],
                     iterator_activite["ComLib"], iterator_activite["EquipementId"],
                     iterator_activite["ActCode"], iterator_activite["ActLib"]]
            # print(ligne)
            cursor.execute(
                """INSERT IGNORE INTO activite (ComInsee, ComLib, EquipementId, ActCode, ActLib)  VALUES(%s, %s, %s, %s,%s)""",
                ligne)
            conn.commit()


def parse_installation():
    cursor.execute("""DELETE FROM installation WHERE 1""")
    conn.commit()
    with open(get_path()[1])  as data_file:
        fichier_installation = csv.DictReader(data_file);
        # installation
        for iterator_installation in fichier_installation:
            # print(iterator_installation)
            address = iterator_installation["Numero de la voie"] +" "+ iterator_installation["Nom de la voie"] + " " + \
                      iterator_installation["Nom de la commune"] + " "+ iterator_installation["Code postal"]
            # print(address)
            ligne = [iterator_installation["Nom usuel de l'installation"],
                     iterator_installation["Numéro de l'installation"],
                     iterator_installation["Latitude"], iterator_installation["Longitude"],
                     iterator_installation["Code INSEE"], iterator_installation["Code postal"],
                     address,
                     iterator_installation["Nom de la commune"]]
            cursor.execute(
                """INSERT IGNORE INTO installation (NomInstall,InsNumeroInstall, Latitude,Longitude,ComInsee,ComCode,Adresse,ComLib) VALUES(%s,%s, %s,%s,%s,%s,%s,%s)""",
                ligne)
            conn.commit()


def parse_equipement():
    with open(get_path()[2])  as data_file:
        cursor.execute("""DELETE FROM equipement WHERE 1""")
        conn.commit()
        fichier_equipement = csv.DictReader(data_file);
        # equipement
        for iterator_equipement in fichier_equipement:
            # print(iterator_equipement)
            ligne = [iterator_equipement["ComInsee"], iterator_equipement["InsNumeroInstall"],
                     iterator_equipement["InsNom"], iterator_equipement["EquipementId"],
                     iterator_equipement["EquNom"],
                     iterator_equipement["EquGpsY"], iterator_equipement["EquGpsX"]]
            cursor.execute(
                """INSERT IGNORE INTO equipement (ComInsee, InsNumeroInstall, InsNomInstall, EquipementId, EquNom,EquGpsY,EquGpsX) VALUES(%s,%s, %s,%s,%s,%s,%s)""",
                ligne)
            conn.commit()








try:
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="SportEquip")
    cursor = conn.cursor()
    parse_installation()
    parse_equipement()
    parse_activite()
    conn.close()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
        conn.close()
        exit(-1)
