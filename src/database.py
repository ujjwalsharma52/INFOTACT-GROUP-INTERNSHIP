
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_connection():
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "atmosync_db"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT", "5432")
        )

        print("PostgreSQL connected successfully!")
        return connection

    except Exception as error:
        print("Database connection failed:", error)
        return None
