import mysql.connector 

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

class DAO():
    def __init__(self):
        conn = mysql.connector.connect(host="localhost",user="E155122L",password="E155122L", database="E155122L")
        cursor = conn.cursor()
        conn.close()
    
##Return all the the activities that start with the same latters as the input_string
def guess_input_activites(input_string):
    input = input_string+"%" 
    cursor.execute("""SELECT ActCode, ActLib FROM activite WHERE ActLib like %s""",[input])
    liste_active=[]
    for  activite in cursor:
         liste_active.append({'ActCode':activite[0],'ActLib':activite[1]})
    #conn.close()
    return liste_active;
    
##Return all the the communes that start with the same latters as the input_string or number for postal code
def guess_input_positions(input_string):
    input = input_string+"%" 
    cursor.execute("""SELECT `ComInsee`, `ComLib` FROM `commune` WHERE (ComLib like %s OR ComInsee like  %s)""",[input,input])
    communes=[]
    for  activite in cursor:
         communes.append({'ComInsee':activite[0],'ComLib':activite[1]})
    #conn.close()
    return communes;
    
##Return a sorted list of the activites. Sorted by distance to the position in a range of the radius
def get_activities(position,radius):
    #todo
    return 0
    
##Return activities in a city (search by city nome or by postal code)
def get_activities(city):
    selected_city = guess_input_positions(city)[0]['ComLib']
    cursor.execute("""SELECT ac.ActLib FROM installations i ,acti_equi a, equipement e, activite ac WHERE i.ComLib= %s and a.EquipementId = e.EquipementId and e.InsNumeroInstall=i.InsNumeroInstall and ac.ActCode= a.ActCode """,[selected_city])
    liste_active=[]
    for  activite in cursor:
        print (activite)
        #liste_active.append({'ComLib':[0],'ActLiactiviteb':activite[1]})
    #conn.close()
    return activite;








