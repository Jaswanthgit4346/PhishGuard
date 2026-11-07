
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

# Prevent repeated email-table initialization during one app session.
_email_table_ready = False


# ==========================================
# DATABASE CONNECTION
# ==========================================

def connect_database():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password=os.getenv("PHISHGUARD_DB_PASSWORD"),
            database="phishguard_db"
        )

    except Error as error:
        print("Database connection failed:", error)
        return None


# ==========================================
# CREATE EMAIL TABLE
# ==========================================

def create_email_table():
    global _email_table_ready

    if _email_table_ready:
        return True

    connection = connect_database()

    if connection is None:
        return False

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
        CREATE TABLE IF NOT EXISTS email_scan_history (
            email_scan_id INT AUTO_INCREMENT PRIMARY KEY,
            email_content LONGTEXT NOT NULL,
            risk_level VARCHAR(20) NOT NULL,
            detection_reasons TEXT,
            scan_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """

        cursor.execute(query)
        connection.commit()

        _email_table_ready = True

        print("Email scan table is ready!")
        return True

    except Error as error:
        print("Error creating email table:", error)
        return False

    finally:
        if cursor is not None:
            cursor.close()

        if connection.is_connected():
            connection.close()


# ==========================================
# SAVE URL SCAN
# ==========================================

def save_scan(url, risk_level, reasons):
    connection = connect_database()

    if connection is None:
        return False

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
        INSERT INTO scan_history
        (url, risk_level, detection_reasons)
        VALUES (%s, %s, %s)
        """

        detection_reasons = "\n".join(
            map(str, reasons)
        )

        cursor.execute(
            query,
            (url, risk_level, detection_reasons)
        )

        connection.commit()

        print("URL scan saved successfully!")
        return True

    except Error as error:
        print("Error saving URL scan:", error)
        return False

    finally:
        if cursor is not None:
            cursor.close()

        if connection.is_connected():
            connection.close()


# ==========================================
# SAVE EMAIL SCAN
# ==========================================

def save_email_scan(email_content, risk_level, reasons):

    if not create_email_table():
        return False

    connection = connect_database()

    if connection is None:
        return False

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
        INSERT INTO email_scan_history
        (email_content, risk_level, detection_reasons)
        VALUES (%s, %s, %s)
        """

        detection_reasons = "\n".join(
            map(str, reasons)
        )

        cursor.execute(
            query,
            (email_content, risk_level, detection_reasons)
        )

        connection.commit()

        print("Email scan saved successfully!")
        return True

    except Error as error:
        print("Error saving email scan:", error)
        return False

    finally:
        if cursor is not None:
            cursor.close()

        if connection.is_connected():
            connection.close()


# ==========================================
# GET URL SCAN HISTORY
# ==========================================

def get_scan_history():
    connection = connect_database()

    if connection is None:
        return []

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
        SELECT
            scan_id,
            url,
            risk_level,
            detection_reasons,
            scan_time
        FROM scan_history
        ORDER BY scan_id DESC
        """

        cursor.execute(query)

        return cursor.fetchall()

    except Error as error:
        print("Error retrieving URL history:", error)
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection.is_connected():
            connection.close()


# ==========================================
# GET EMAIL SCAN HISTORY
# ==========================================

def get_email_scan_history():

    if not create_email_table():
        return []

    connection = connect_database()

    if connection is None:
        return []

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
        SELECT
            email_scan_id,
            email_content,
            risk_level,
            detection_reasons,
            scan_time
        FROM email_scan_history
        ORDER BY email_scan_id DESC
        """

        cursor.execute(query)

        return cursor.fetchall()

    except Error as error:
        print("Error retrieving email history:", error)
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection.is_connected():
            connection.close()


# ==========================================
# DELETE ONE SELECTED RECORD
# ==========================================

def delete_scan_history_record(scan_type, scan_id):

    delete_queries = {
        "URL": """
            DELETE FROM scan_history
            WHERE scan_id = %s
        """,

        "EMAIL": """
            DELETE FROM email_scan_history
            WHERE email_scan_id = %s
        """
    }

    scan_type = str(scan_type).upper()

    if scan_type not in delete_queries:
        print("Invalid scan type.")
        return False

    try:
        scan_id = int(scan_id)

        if scan_id <= 0:
            return False

    except (ValueError, TypeError):
        print("Invalid scan ID.")
        return False

    if scan_type == "EMAIL":
        if not create_email_table():
            return False

    connection = connect_database()

    if connection is None:
        return False

    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute(
            delete_queries[scan_type],
            (scan_id,)
        )

        deleted_count = cursor.rowcount

        connection.commit()

        if deleted_count == 1:
            print(
                f"{scan_type} scan #{scan_id} deleted successfully."
            )
            return True

        print("No matching scan record found.")
        return False

    except Error as error:
        connection.rollback()
        print("Error deleting scan:", error)
        return False

    finally:
        if cursor is not None:
            cursor.close()

        if connection.is_connected():
            connection.close()


# ==========================================
# CLEAR ALL HISTORY
# ==========================================

def clear_scan_history():

    if not create_email_table():
        return False

    connection = connect_database()

    if connection is None:
        return False

    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute("DELETE FROM scan_history")
        cursor.execute("DELETE FROM email_scan_history")

        connection.commit()

        print("All scan history deleted successfully.")
        return True

    except Error as error:
        connection.rollback()
        print("Error clearing history:", error)
        return False

    finally:
        if cursor is not None:
            cursor.close()

        if connection.is_connected():
            connection.close()


# ==========================================
# DASHBOARD STATISTICS
# ==========================================

def get_dashboard_stats():

    if not create_email_table():
        return {
            "total": 0,
            "low": 0,
            "medium": 0,
            "high": 0
        }

    connection = connect_database()

    if connection is None:
        return {
            "total": 0,
            "low": 0,
            "medium": 0,
            "high": 0
        }

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
        SELECT
            COUNT(*),

            SUM(
                CASE
                    WHEN risk_level = 'Low' THEN 1
                    ELSE 0
                END
            ),

            SUM(
                CASE
                    WHEN risk_level = 'Medium' THEN 1
                    ELSE 0
                END
            ),

            SUM(
                CASE
                    WHEN risk_level = 'High' THEN 1
                    ELSE 0
                END
            )

        FROM (
            SELECT risk_level
            FROM scan_history

            UNION ALL

            SELECT risk_level
            FROM email_scan_history
        ) AS combined_scans
        """

        cursor.execute(query)

        result = cursor.fetchone()

        return {
            "total": result[0] or 0,
            "low": result[1] or 0,
            "medium": result[2] or 0,
            "high": result[3] or 0
        }

    except Error as error:
        print("Error retrieving statistics:", error)

        return {
            "total": 0,
            "low": 0,
            "medium": 0,
            "high": 0
        }

    finally:
        if cursor is not None:
            cursor.close()

        if connection.is_connected():
            connection.close()


# ==========================================
# TEST DATABASE
# ==========================================

if __name__ == "__main__":

    connection = connect_database()

    if connection:
        print("Connected to PhishGuard MySQL Database!")

        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE()")

        print("Connected Database:", cursor.fetchone()[0])

        cursor.close()
        connection.close()

        print("Database connection closed.")

    print("\n----- EMAIL TABLE -----")

    if create_email_table():
        print("Email table is ready.")

    print("\n----- DASHBOARD STATISTICS -----")

    stats = get_dashboard_stats()

    print("Total Scans:", stats["total"])
    print("Low Risk:", stats["low"])
    print("Medium Risk:", stats["medium"])
    print("High Risk:", stats["high"])
