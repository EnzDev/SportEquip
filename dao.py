import mysql.connector 


class DAO():
    def __init__(self):
        conn = mysql.connector.connect(host="localhost",user="E155122L",password="E155122L", database="E155122L")
        cursor = conn.cursor()
        conn.close()
        
    #Return all the the activities that start with the same latters as the input_string
    def guess_input_activites(input_string):
        #todo    
        return 0;
        
    #Return a sorted list of the activites. Sorted by distance to the position
    def get_activities(position):
        #todo    
        return 0;
   





