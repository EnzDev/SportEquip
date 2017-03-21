import mysql.connector 
import math

class DAO():
    def __init__(self):
##Connextion with db
        try:
            self.conn = mysql.connector.connect(host="infoweb",user="E155122L",password="E155122L", database="E155122L")
            self.cursor = self.conn.cursor()
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
        
    ##Return all the installations distant from a city
    #param: position = city inputed (can be null)
    #param: radius = distance from the city
    def get_activitiesFrom(self,position,radius):
        list_city = self.get_citiesFrom(position,radius)
        list_city_activ = []
        for city in list_city:
            list_city_activ.append(self.get_activities(city))
            self.get_activities(city)
        
        return list_city_activ
        
    ###Return all the cities in a certain range
    #position = the firsts letteres of the city or first numbers of the post code 
    def get_citiesFrom(self,position,radius):
        liste_city = []
        #guessing cities
        cities_dic = self.guess_input_positions(position)
        #get only the name of the city
        cities = []
        for city in cities_dic:
            cities.append(city['ComLib'])
        #getting each cities a locations
        for city in cities:
            self.cursor.execute("""SELECT DISTINCT `Latitude`, `Longitude`, c.ComLib FROM installations i , commune c WHERE c.ComLib=i.ComLib and c.ComLib=%s""",[city])
            areas = []
            for  loc in self.cursor:
                longitude = float(loc[1])
                latitude = float(loc[0])
              
        
               #calculation of the longitude whitin range
                minlat =  round(latitude - 1/110.574*radius ,5)
                maxlat =  round(latitude + 1/110.574*radius,5)
                minlong =  round(longitude - 1/(111.320*math.cos(latitude)) *radius ,5)
                maxlong =  round(longitude + 1/(111.320*math.cos(latitude)) *radius ,5)
                
             
                self.cursor.execute(""" SELECT DISTINCT i.ComLib FROM installations i WHERE i.Latitude > %s and i.Latitude < %s and i.Longitude > %s and i.Longitude < %s  """,[minlat, maxlat,minlong ,maxlong])
               
                for  row in self.cursor:
                    
                    liste_city.append(row[0])
        
        return liste_city
        
    ##Return activities in a city (search by city nome or by postal code)
    #param:city = the firsts letteres of the city or first numbers of the post code 
    #return : a dictionary that contains activities code and name
    def get_activities(self,city):
        selected_city = self.guess_input_positions(city)[0]['ComLib']
        self.cursor.execute("""SELECT ac.ActLib FROM installations i ,acti_equi ae, equipement e, activite ac 
                                WHERE i.ComLib= %s 
                                    and ae.EquipementId = e.EquipementId 
                                    and e.InsNumeroInstall=i.InsNumeroInstall 
                                    and ac.ActCode= ae.ActCode """,[selected_city])
        liste_active=[]
        for  activite in self.cursor:
            print(activite)
            liste_active.append({'ComLib':activite[0],'ActLib':activite[1]})
        #conn.close()
        return liste_active;
    
        
    ### Get installation of on city  and one activity
    #param:city = the firsts letteres of the city or first numbers of the post code 
    #param:activity = the first letters of an activity
    #param: radius = distance from the city allowed
    #return: a table of dictionary that contains all infos of a spectific installations
    def get_installation(self,city,activity,radius):
        #list_city = self.get_citiesFrom(city,radius)
        list_city = self.guess_input_positions(city)
        list_activ = self.guess_input_activites(activity)
        liste_install=[]
        for it_city in list_city:
            city_name = it_city['ComLib']
            for it_activ in list_activ:
                act_code = it_activ['ActCode']
                self.cursor.execute("""SELECT i.Latitude, i.Longitude, i.Nom, i.InsLibelleVoie
                                FROM installations i ,acti_equi ae, equipement e, activite ac 
                                WHERE i.ComLib= %s
                                    and ae.ActCode =%s
                                    and ae.EquipementId = e.EquipementId 
                                    and e.InsNumeroInstall=i.InsNumeroInstall ;
                                    """,[city_name,act_code])
                for  res in self.cursor:
                      liste_install.append({'ComLib':city_name,
                                            'ActLib':it_city['ActLib'],
                                            'Latitude':res[0],
                                            'Longitude':res[1],
                                            'Nom':res[2],
                                            'Address':res[3]})
                                            
        #conn.close()
        return liste_install;
        

        
        
    
    
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    
    




