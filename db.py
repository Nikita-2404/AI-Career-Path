import os

import mysql.connector
from mysql.connector import Error

from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()


# ============================================================
# MYSQL CONFIGURATION
# ============================================================

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_NAME = os.getenv("DB_NAME", "ai_career_db")


# ============================================================
# CREATE DATABASE
# ============================================================

def create_database():

    connection = None
    cursor = None

    try:

        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )

        cursor = connection.cursor()

        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`"
        )

        connection.commit()

        print("Database checked successfully.")

    except Error as error:

        print("DATABASE CREATION ERROR:", error)
        raise

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ============================================================
# GET MYSQL CONNECTION
# ============================================================

def get_db():

    try:

        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        return connection

    except Error as error:

        print("MYSQL CONNECTION ERROR:", error)
        raise


# ============================================================
# CLOSE DB
# ============================================================

def close_db(error=None):
    pass


# ============================================================
# EXECUTE QUERY
# ============================================================

def execute_query(query, params=None, fetch=False, many=False):

    connection = None
    cursor = None

    try:

        connection = get_db()

        # dictionary=True allows:
        # row["name"]
        # row["career"]
        # row["total"]
        # etc.

        cursor = connection.cursor(dictionary=True)

        if many:

            cursor.executemany(
                query,
                params or []
            )

        else:

            cursor.execute(
                query,
                params or ()
            )

        # ----------------------------------------------------
        # SELECT QUERY
        # ----------------------------------------------------

        if fetch:

            result = cursor.fetchall()

            return result

        # ----------------------------------------------------
        # INSERT / UPDATE / DELETE
        # ----------------------------------------------------

        connection.commit()

        return cursor.lastrowid

    except Error as error:

        print("QUERY ERROR:")
        print(error)

        raise

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ============================================================
# FETCH ONE ROW
# ============================================================

def fetch_one(query, params=None):

    connection = None
    cursor = None

    try:

        connection = get_db()

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            query,
            params or ()
        )

        result = cursor.fetchone()

        return result

    except Error as error:

        print("FETCH ONE ERROR:")
        print(error)

        raise

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ============================================================
# FETCH ALL ROWS
# ============================================================

def fetch_all(query, params=None):

    connection = None
    cursor = None

    try:

        connection = get_db()

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            query,
            params or ()
        )

        result = cursor.fetchall()

        return result

    except Error as error:

        print("FETCH ALL ERROR:")
        print(error)

        raise

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ============================================================
# INITIALIZE DATABASE TABLES
# ============================================================

def init_db():

    connection = None
    cursor = None

    try:

        create_database()

        connection = get_db()

        cursor = connection.cursor()

        # ====================================================
        # USERS
        # ====================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (

                id INT AUTO_INCREMENT PRIMARY KEY,

                name VARCHAR(100) NOT NULL,

                email VARCHAR(150) NOT NULL UNIQUE,

                password VARCHAR(255) NOT NULL,

                education VARCHAR(150),

                skills TEXT,

                interests TEXT,

                status VARCHAR(30) DEFAULT 'Active',

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
        """)

        # ====================================================
        # ADMINS
        # ====================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admins (

                id INT AUTO_INCREMENT PRIMARY KEY,

                username VARCHAR(100) NOT NULL UNIQUE,

                password VARCHAR(255) NOT NULL,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
        """)

        # ====================================================
        # PREDICTIONS
        # ====================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (

                id INT AUTO_INCREMENT PRIMARY KEY,

                user_id INT NOT NULL,

                education VARCHAR(150),

                skills TEXT,

                interests TEXT,

                experience VARCHAR(150),

                career VARCHAR(150),

                score DECIMAL(5,2),

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE

            )
        """)

        # ====================================================
        # JOBS
        # ====================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (

                id INT AUTO_INCREMENT PRIMARY KEY,

                company VARCHAR(150),

                title VARCHAR(150),

                location VARCHAR(150),

                job_type VARCHAR(100),

                salary VARCHAR(100),

                skills TEXT,

                logo VARCHAR(255),

                description TEXT

            )
        """)

        # ====================================================
        # APPLICATIONS
        # ====================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS applications (

                id INT AUTO_INCREMENT PRIMARY KEY,

                user_id INT NOT NULL,

                job_id INT NOT NULL,

                status VARCHAR(50) DEFAULT 'Applied',

                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                UNIQUE KEY unique_application (user_id, job_id),

                FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE,

                FOREIGN KEY (job_id)
                REFERENCES jobs(id)
                ON DELETE CASCADE

            )
        """)

        connection.commit()

        print("All database tables checked successfully.")

    except Error as error:

        print("DATABASE INITIALIZATION ERROR:")
        print(error)

        raise

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ============================================================
# SEED DATA
# ============================================================

def seed_data():

    connection = None
    cursor = None

    try:

        connection = get_db()

        cursor = connection.cursor()

        # ====================================================
        # ADMIN
        # ====================================================

        cursor.execute(
            """
            SELECT id
            FROM admins
            WHERE username = %s
            """,
            ("admin",)
        )

        admin = cursor.fetchone()

        if not admin:

            password_hash = generate_password_hash(
                "admin123"
            )

            cursor.execute(
                """
                INSERT INTO admins
                (
                    username,
                    password
                )
                VALUES
                (
                    %s,
                    %s
                )
                """,
                (
                    "admin",
                    password_hash
                )
            )

            print("Default admin created.")

        # ====================================================
        # CHECK JOBS
        # ====================================================

        cursor.execute(
            "SELECT COUNT(*) FROM jobs"
        )

        job_count = cursor.fetchone()[0]

        # ====================================================
        # ADD SAMPLE JOBS
        # ====================================================

        if job_count == 0:

            jobs = [

                (
                    "Google",
                    "Machine Learning Engineer",
                    "Remote",
                    "Full-time",
                    "₹12-18 LPA",
                    "Python, Machine Learning, TensorFlow",
                    "G",
                    "Develop machine learning models and AI applications."
                ),

                (
                    "Amazon",
                    "Data Scientist",
                    "Bangalore",
                    "Full-time",
                    "₹10-16 LPA",
                    "Python, SQL, Machine Learning",
                    "A",
                    "Analyze data and build predictive models."
                ),

                (
                    "Microsoft",
                    "AI Research Intern",
                    "Remote",
                    "Internship",
                    "₹8-12 LPA",
                    "Python, AI, Deep Learning",
                    "M",
                    "Work on artificial intelligence research projects."
                ),

                (
                    "Deloitte",
                    "Data Analyst",
                    "Pune",
                    "Full-time",
                    "₹5-8 LPA",
                    "SQL, Power BI, Excel",
                    "D",
                    "Analyze business data and create reports."
                ),

                (
                    "TCS",
                    "Software Developer",
                    "Pune",
                    "Full-time",
                    "₹4-7 LPA",
                    "Java, SQL, Python",
                    "T",
                    "Develop and maintain software applications."
                ),

                (
                    "Infosys",
                    "Python Developer",
                    "Pune",
                    "Full-time",
                    "₹4-8 LPA",
                    "Python, Flask, SQL",
                    "I",
                    "Develop Python-based applications."
                ),

                (
                    "Accenture",
                    "Web Developer",
                    "Mumbai",
                    "Full-time",
                    "₹4-7 LPA",
                    "HTML, CSS, JavaScript",
                    "A",
                    "Develop modern web applications."
                )

            ]

            cursor.executemany(
                """
                INSERT INTO jobs
                (
                    company,
                    title,
                    location,
                    job_type,
                    salary,
                    skills,
                    logo,
                    description
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                jobs
            )

            print("Sample jobs added.")

        connection.commit()

        print("Seed data checked successfully.")

    except Error as error:

        print("SEED DATA ERROR:")
        print(error)

        raise

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ============================================================
# DATABASE TEST
# ============================================================

def test_database():

    connection = None
    cursor = None

    try:

        connection = get_db()

        cursor = connection.cursor()

        # ----------------------------------------------------
        # USERS
        # ----------------------------------------------------

        cursor.execute(
            "SELECT COUNT(*) FROM users"
        )

        users = cursor.fetchone()[0]

        # ----------------------------------------------------
        # PREDICTIONS
        # ----------------------------------------------------

        cursor.execute(
            "SELECT COUNT(*) FROM predictions"
        )

        predictions = cursor.fetchone()[0]

        # ----------------------------------------------------
        # JOBS
        # ----------------------------------------------------

        cursor.execute(
            "SELECT COUNT(*) FROM jobs"
        )

        jobs = cursor.fetchone()[0]

        # ----------------------------------------------------
        # APPLICATIONS
        # ----------------------------------------------------

        cursor.execute(
            "SELECT COUNT(*) FROM applications"
        )

        applications = cursor.fetchone()[0]

        print("")
        print("========================================")
        print("DATABASE TEST")
        print("========================================")
        print("Users       :", users)
        print("Predictions :", predictions)
        print("Jobs        :", jobs)
        print("Applications:", applications)
        print("========================================")

    except Error as error:

        print("DATABASE TEST ERROR:", error)

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("")
    print("========================================")
    print("AI CAREER PATH - DATABASE SETUP")
    print("========================================")

    init_db()

    seed_data()

    test_database()

    print("")
    print("MySQL database setup completed successfully.")