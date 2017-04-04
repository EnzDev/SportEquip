import mysql.connector
import math

from mysql.connector import errorcode


class DAO():
    """
    Provide all the methods to connect between the database and the serveur
    """

    def __init__(self):
        # Connextion with db
        try:
            self.conn = mysql.connector.connect(host="localhost", user="root", password="", database="SportEquip")
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def guess_input_activites(self, input_string):
        """
        Return all the the activities that start with the same latters as the input_string
        @param input_string  
        @return a dictionnary of activities
        """
        input = input_string + "%"
        self.cursor.execute("""SELECT DISTINCT ActCode, ActLib FROM activite WHERE ActLib like %s""", [input])
        liste_active = []
        for activite in self.cursor:
            liste_active.append({'ActCode': activite[0], 'ActLib': activite[1]})
        # conn.close()
        return liste_active;

    def guess_input_positions(self, input_string):
        """
        Return all the the communes that start with the same latters as the input_string or number for postal code
        @param input_string  
        @return a dictionnary of cities
        """
        input = input_string + "%"
        self.cursor.execute(
            """SELECT DISTINCT ComCode, ComLib, ComInsee FROM installation WHERE (ComLib like %s OR ComCode like  %s)""",
            [input, input])
        communes = []
        for activite_it in self.cursor:
            communes.append({'ComCode': activite_it[0], 'ComLib': activite_it[1], 'ComInsee': activite_it[2]})
        # conn.close()
        return communes;

    def guess_Activities_byGCity(self, incompleteCity, incompleteActivity, range=0):
        """
        Get activity with an incomplete city name ans a range.
        @return a set of activities
        """
        city = incompleteCity + "%"  # inputed city field
        self.cursor.execute(
            """SELECT DISTINCT ComInsee,latitude,longitude FROM installation WHERE (ComLib like %s OR ComInsee like  %s)""",
            [city, city])
        city_set = set()  # set of comInsee of the cities that are either the inputed one or the one withn range
        for cityPos_it in self.cursor:
            cities = self.get_citiesFrom(cityPos_it[1], cityPos_it[2], range)
            city_set = city_set.union(cities)

        activity = incompleteActivity + "%"  # inputed activity field
        activity_set = set()
        for city in city_set:
            self.cursor.execute("""SELECT DISTINCT ActLib FROM activite WHERE ActLib like %s and comInsee = %s""",
                                [activity, city])
            for activity_it in self.cursor:
                activity_set.add(activity_it[0])
        return activity_set

    def guess_City_byGActivity(self, incompleteCity, incompleteActivity):
        """
        Get cities that offer an activity
        @return a dictionnary of cities 
        """
        all_activities = self.guess_input_activites(incompleteActivity)
        city_set = set()  # store the comInsee of all city to unsure no duplicate exist
        city = incompleteCity + "%"
        for activity_it in all_activities:
            actCode = activity_it['ActCode']
            self.cursor.execute("SELECT DISTINCT ComInsee FROM activite  WHERE ActCode = %s and ComLib like %s  ",
                                [actCode, city])
            for comInsee_it in self.cursor:
                city_set.add(comInsee_it[0])

        city_dic = []
        # Getting the name and post code for the city we have in the set
        for city_it in city_set:
            self.cursor.execute("""SELECT DISTINCT ComInsee,ComLib,ComCode FROM installation WHERE ComInsee = %s""",
                                [city_it])
            for result_it in self.cursor:
                city_dic.append({'ComInsee': result_it[0], 'ComLib': result_it[1], 'ComCode': result_it[2]})

        return city_dic

    def get_installation(self, comLib, incompleteActivity, range=0):
        """
        Lookup for all the installation that offer the activities provided by the first city guessed by the autocompletion
        @return a dictionnary of installations
        """
        activity_list = self.guess_input_activites(incompleteActivity)
        cityLatitude, cityLongitude = self.get_City_Pos(comLib)
        city_list = self.get_citiesFrom(cityLatitude, cityLongitude, range)
        equipement_dic = {}
        for comInsee in city_list:
            for activity_it in activity_list:
                ActCode = activity_it['ActCode']
                self.cursor.execute(
                    """SELECT DISTINCT a.equipementID,i.EquGpsY,i.EquGpsX,i.EquNom, i.InsNumeroInstall FROM activite a,equipement i WHERE ActCode =  %s and a.ComInsee = %s and a.equipementID = i.equipementID""",
                    [ActCode, comInsee])
                for equipement_it in self.cursor:
                    equipement_dic[equipement_it[0]] = {'EquGpsY': equipement_it[1], 'EquGpsX': equipement_it[2],
                                                        'EquNom': equipement_it[3], 'install': equipement_it[4]}

        # Getting the information relatives to all the output installations
        # Adresse
        for equipement_id in equipement_dic:
            self.cursor.execute("""SELECT  Adresse FROM installation WHERE InsNumeroInstall=%s""", [equipement_dic[equipement_id]['install']])
            for equipement_it in self.cursor:
                equipement_dic[equipement_id]['Adresse'] = equipement_it
        # List of avalable activities
        for equipement_id in equipement_dic:
            self.cursor.execute("""SELECT  ActLib FROM activite WHERE EquipementId =%s""", [equipement_id])
            activity_set = set()
            for activity_it in self.cursor:
                activity_set.add(activity_it[0])
            equipement_dic[equipement_id]['Activite'] = activity_set
        return equipement_dic

    def get_citiesFrom(self, latitude, longitude, radius=1):
        """
        Get all cities within a range from another based on its coordonates
        @return a set on comInsee
        """
        # calculation of the longitude whitin range
        latitude = float(latitude)
        longitude = float(longitude)
        minLat, maxLat = sorted((round(latitude - 1 / 110.574 * radius, 3), round(latitude + 1 / 110.574 * radius, 3)))
        minLong, maxLong = sorted((round(longitude - 1 / (111.320 * math.cos(latitude)) * radius, 3),
                                   round(longitude + 1 / (111.320 * math.cos(latitude)) * radius, 3)))
        minLat = round(minLat - 0.001, 3)
        minLong = round(minLong - 0.005, 3)
        maxLong = round(maxLong + 0.005, 3)

        # get cities that match the range
        condition = (
        "i.Latitude >= " + str(minLat) + " and i.Latitude <= " + str(maxLat) + "  and i.Longitude >= " + str(
            minLong) + " and i.Longitude <= " + str(maxLong))
        self.cursor.execute("SELECT DISTINCT i.ComInsee FROM installation i WHERE " + condition)
        city_set = set()
        for city in self.cursor:
            city_set.add(city[0])
        return city_set

    def get_City_Pos(self, incompleteCity):
        """
        Get city coordonates
        @return a set on comInsee
        """
        city = incompleteCity + "%"  # inputed city field
        self.cursor.execute(
            """SELECT DISTINCT ComInsee,latitude,longitude FROM installation WHERE (ComLib like %s OR ComInsee like  %s) LIMIT 0,1""",
            [city, city])
        for cityPos_it in self.cursor:
            return [float(cityPos_it[1]), float(cityPos_it[2])]
