import mysql.connector 

class DAO():
    def __init():
##Connextion with db
        try:
            conn = mysql.connector.connect(host="infoweb",user="E155122L",password="E155122L", database="E155122L")
            self.cursor = conn.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print (err)
    
    ##Return all the the activities that start with the same latters as the input_string
    def guess_input_activites(self,input_string):
        input = input_string+"%" 
        self.cursor.execute("""SELECT ActCode, ActLib FROM activite WHERE ActLib like %s""",[input])
        liste_active=[]
        for  activite in self.cursor:
            liste_active.append({'ActCode':activite[0],'ActLib':activite[1]})
        #conn.close()
        return liste_active;
        
    ##Return all the the communes that start with the same latters as the input_string or number for postal code
    def guess_input_positions(self,input_string):
        input = input_string+"%" 
        self.cursor.execute("""SELECT `ComInsee`, `ComLib` FROM `commune` WHERE (ComLib like %s OR ComInsee like  %s)""",[input,input])
        communes=[]
        for  activite in self.cursor:
            communes.append({'ComInsee':activite[0],'ComLib':activite[1]})
        #conn.close()
        return communes;
        
    ##Return a sorted list of the activites. Sorted by distance to the position in a range of the radius
    def get_activities(self,position,radius):
        #todo
        return 0
        
    ##Return activities in a city (search by city nome or by postal code)
    def get_activities(self,city):
        selected_city = self.guess_input_positions(city)[0]['ComLib']
        self.cursor.execute("""SELECT ac.ActLib FROM installations i ,acti_equi a, equipement e, activite ac WHERE i.ComLib= %s and a.EquipementId = e.EquipementId and e.InsNumeroInstall=i.InsNumeroInstall and ac.ActCode= a.ActCode """,[selected_city])
        liste_active=[]
        for  activite in self.cursor:
            print (activite)
            #liste_active.append({'ComLib':[0],'ActLiactiviteb':activite[1]})
        #conn.close()
        return activite;
    
        
    ### Get installation of on city  and one activity
    
    
    
    




