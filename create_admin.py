import os

import mysql.connector
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash


# ============================================================
# LOAD .ENV
# ============================================================

load_dotenv()


# ============================================================
# DATABASE SETTINGS
# ============================================================

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "ai_career_db")
DB_PORT = int(os.getenv("DB_PORT", "3306"))


# ============================================================
# ADMIN DETAILS
# ============================================================

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


# ============================================================
# CONNECT TO MYSQL
# ============================================================

try:

    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )

    print("MySQL connected successfully.")

except mysql.connector.Error as e:

    print("MySQL connection failed.")
    print(e)

    raise SystemExit


# ============================================================
# CREATE ADMINS TABLE
# ============================================================

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

conn.commit()


# ============================================================
# CREATE / UPDATE ADMIN
# ============================================================

hashed_password = generate_password_hash(
    ADMIN_PASSWORD
)

cursor.execute(
    "SELECT id FROM admins WHERE username = %s",
    (ADMIN_USERNAME,)
)

existing_admin = cursor.fetchone()


if existing_admin:

    # Update existing admin password
    cursor.execute(
        """
        UPDATE admins
        SET password = %s
        WHERE username = %s
        """,
        (
            hashed_password,
            ADMIN_USERNAME
        )
    )

    print()
    print("Existing admin account updated successfully.")

else:

    # Create new admin
    cursor.execute(
        """
        INSERT INTO admins
        (username, password)
        VALUES (%s, %s)
        """,
        (
            ADMIN_USERNAME,
            hashed_password
        )
    )

    print()
    print("New admin account created successfully.")


conn.commit()


# ============================================================
# CLOSE CONNECTION
# ============================================================

cursor.close()
conn.close()


# ============================================================
# SHOW LOGIN DETAILS
# ============================================================

print()
print("==========================================")
print("       ADMIN ACCOUNT READY")
print("==========================================")
print("Username : admin")
print("Password : admin123")
print("==========================================")
print()