"""
datasetFeatures.py - create the features of a given dataset or dataset sample
Owner: Malliaridis Konstantinos PHd candidate
"""

import os
import mysql.connector

class mySqlTasks:

    # Replace these with your MySQL server and database information
    host = "localhost"
    user = "aprioriUser"
    password = "aprioripwd"
    database = "aprioriBase"
    connection = None

    def _ConnectTobase(self):
        
        # Create a connection to the MySQL server
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

        except mysql.connector.Error as e:
            print(f"Error: {e}")

        except Exception as e:
            vbcrlf = '\n'
            print(f"Unexpected error:{vbcrlf}{e}")


    def myQuery(self, query, tupleQueryParams=None):
        
        if self.connection.is_connected():

            cursor = self.connection.cursor()

            # Execute the query with the data
            cursor.execute(query, tupleQueryParams)

            # Commit the changes
            self.connection.commit() 

            cursor.close


                                 
    def _disconnectDatabase(self):
        try:
            if self.connection.is_connected():
                self.connection.close()

        except mysql.connector.Error as e:
            print(f"Error: {e}")

        except Exception as e:
            vbcrlf = '\n'
            print(f"Unexpected error:{vbcrlf}{e}")
