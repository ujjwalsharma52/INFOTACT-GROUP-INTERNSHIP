
from database import get_connection

connection = get_connection()

if connection:
    print("AtmoSync database connection successful!")

    cursor = connection.cursor()
    cursor.execute("SELECT current_database();")

    result = cursor.fetchone()
    print("Connected Database:", result[0])

    cursor.close()
    connection.close()

    print("Connection closed successfully.")

else:
    print("Please check your database settings.")
