import mysql.connector 
import math

class DAO():
    """
    Provide all the methods to connect between the database and the serveur
    """
    def __init__(self):
        #Connextion with db
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
    
    
    def guess_input_activites(self,input_string):
        """
        Return all the the activities that start with the same latters as the input_string
        @param input_string  
        @return a dictionnary of activities
        """
        input = input_string+"%" 
        self.cursor.execute("""SELECT DISTINCT ActCode, ActLib FROM activite WHERE ActLib like %s""",[input])
        liste_active=[]
        for  activite in self.cursor:
            liste_active.append({'ActCode':activite[0],'ActLib':activite[1]})
        #conn.close()
        return liste_active;

    
   
    def guess_input_positions(self,input_string):
        """
        Return all the the communes that start with the same latters as the input_string or number for postal code
        @param input_string  
        @return a dictionnary of cities
        """
        input = input_string+"%" 
        self.cursor.execute("""SELECT DISTINCT ComCode, ComLib, ComInsee FROM installation WHERE (ComLib like %s OR ComCode like  %s)""",[input,input])
        communes=[]
        for  activite_it in self.cursor:
            communes.append({'ComCode':activite_it[0],'ComLib':activite_it[1],'ComInsee':activite_it[2]})
        #conn.close()
        return communes;
        
        
    
    def guess_Activities_byGCity(self,incompleteCity,incompleteActivity,range=0):
        """
        Get activity with an incomplete city name ans a range.
        @return a set of activities
        """
        city = incompleteCity+"%" #inputed city field
        self.cursor.execute("""SELECT DISTINCT ComInsee,latitude,longitude FROM installation WHERE (ComLib like %s OR ComInsee like  %s)""",[city,city])
        city_set = set()#set of comInsee of the cities that are either the inputed one or the one withn range 
        for cityPos_it in self.cursor:
            cities = self.get_citiesFrom(cityPos_it[1],cityPos_it[2],range)
            city_set = city_set.union(cities)
            
        
        activity = incompleteActivity+"%" #inputed activity field
        activity_set = []
        for city in list_city:
            self.cursor.execute("""SELECT DISTINCT ActLib FROM activite WHERE ActLib like %s and comInsee = %s""",[activity,city])
            for  activity_it in self.cursor:
                activity_set.add(activity_it[0])
        return activity_set
        
    
    
    def guess_City_byGActivity(self,incompleteCity,incompleteActivity):
        """
        Get cities that offer an activity
        @return a dictionnary of cities 
        """
        all_activities = self.guess_input_activites(incompleteActivity)
        city_set = set()#store the comInsee of all city to unsure no duplicate exist
        city = incompleteCity+"%"
        for activity_it in all_activities:
            actCode = activity_it['ActCode']
            self.cursor.execute("SELECT DISTINCT ComInsee FROM activite  WHERE ActCode = %s and a.ComLib like %s  "+ conditions,[actCode,city])
            for comInsee_it in self.cursor:
                city_set.add(comInsee_it[0])
        city_dic = []
        #Getting the name and post code for the city we have in the set
        for city_it in city_set:
            self.cursor.execute("""SELECT DISTINCT ComInsee,ComLib,ComCode FROM installation WHERE ComInsee = %s""",[city_it])
            city_dic.append({'ComInsee':activite_it[0],'ComLib':activite_it[1],'ComCode':activite_it[2]})
            
            
    def get_installation(comLib,incompleteActivity,range):
        """
        Lookup for all the installation that offer the activities provided by the first city guessed by the autocompletion
        @return a dictionnary of installations
        """
        activity_list = self.guess_input_activites(incompleteActivity)
        cityLatitude,cityLongitude = get_City_Pos(city)
        city_list = self.get_citiesFrom(self,cityLatitude,cityLongitude,range)
        installation_set = set()
        for comInsee from city_list:
            for activity_it from activity_list:
                ActCode = activity_it['ActCode']
                self.cursor.execute("""SELECT DISTINCT instNu FROM activite a,Installation i WHERE ActCode =  %s and comInsee = %s and a.equipementID = i.eqID""",[ActCode,comInsee])
                for  installation_it in self.cursor:
                    installation_set.add(installation_it[0])
        
        #Getting the information relatives to alla the output installations
        #todo 
        
        
            
    
            
            
             
         
         
        
        
            
        
            
        
        
    def get_citiesFrom(self,latitude,logitude,radius):
        """
        Get all cities within a range from another based on its coordonates
        @return a set on comInsee
        """
        #calculation of the longitude whitin range
        minLat,maxLat   =  sorted((round(latitude - 1/110.574*radius ,5),round(latitude + 1/110.574*radius ,5)))
        minLong,maxLong =  sorted((round(longitude - 1/(111.320*math.cos(latitude)) *radius ,5),round(longitude + 1/(111.320*math.cos(latitude)) *radius ,5)))
        #get cities that match the range
        condition =  ( "i.Latitude > "+ minLat + " and i.Latitude < " +maxLat+ " and i.Longitude > "+minLong +"and i.Longitude < "+maxLong)
        self.cursor.execute("SELECT DISTINCT i.ComInsee FROM installation i WHERE"+condition)
        city_set = set()
        for city in self.cursor:
            city_set.add(city[0])
        return city_set
        
    def get_City_Pos(incompleteCity):
        """
        Get city coordonates
        @return a set on comInsee
        """
        city = incompleteCity+"%" #inputed city field
        self.cursor.execute("""SELECT DISTINCT ComInsee,latitude,longitude FROM installation WHERE (ComLib like %s OR ComInsee like  %s)""",[city,city])
        return [cityPos_it[1],cityPos_it[2]]
            
            


        
   
        
    
    
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    
    




