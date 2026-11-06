
# PhishGuard
### Phishing Detection and Security Analysis System

PhishGuard is a Python-based desktop application designed to identify and analyze potential phishing threats in website URLs and email content.

The application provides risk classification, scan history management, dashboard statistics, database integration, and report generation through a graphical user interface.

---

## Features

### 1. URL Phishing Detection
- Analyze website URLs.
- Detect suspicious URL patterns and keywords.
- Identify URLs that do not use HTTPS.
- Classify URL risk levels.

### 2. Email Phishing Detection
- Analyze email content.
- Detect suspicious phrases and keywords.
- Identify insecure links.
- Detect urgent or pressuring language.
- Classify email risk levels.

### 3. Dashboard
- View scan statistics.
- Monitor URL and email scans.
- View risk distribution.
- Access application modules through a sidebar.

### 4. Scan History
- Store URL and email scan records.
- View previous scan results.
- Search and filter scan history.
- Display risk levels using different colours.
- Delete individual records.
- Clear scan history with confirmation.

### 5. Reports
- Generate PDF reports.
- Export scan information to CSV.
- Review scan results outside the application.

### 6. Database Management
- MySQL database integration.
- Persistent storage of scan records.
- Database connection testing.

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| Tkinter | Graphical user interface |
| MySQL | Database management |
| mysql-connector-python | Python-MySQL connectivity |
| python-dotenv | Environment configuration |
| ReportLab | PDF report generation |

---

## Project Structure

PhishGuard/
|
|-- assets/
|   |-- icons/
|
|-- backend/
|   |-- __init__.py
|   |-- database.py
|   |-- email_detection.py
|   |-- url_detection.py
|   |-- reports.py
|
|-- frontend/
|   |-- __init__.py
|   |-- dashboard.py
|
|-- tests/
|   |-- __init__.py
|   |-- test_database.py
|   |-- test_email.py
|   |-- test_url.py
|
|-- docs/
|-- reports/
|-- venv/
|
|-- .env
|-- .gitignore
|-- main.py
|-- README.md
|-- requirements.txt

---

## System Requirements

- Windows 10 or Windows 11
- Python 3.13 or compatible version
- MySQL Server
- pip package manager

---

## Installation and Setup

### Step 1: Install Python

Install Python and verify:

    python --version

### Step 2: Install MySQL

Install and configure MySQL Server.

Create the database:

    CREATE DATABASE phishguard_db;

### Step 3: Create a Virtual Environment

    python -m venv venv

Activate it in PowerShell:

    .\venv\Scripts\Activate.ps1

### Step 4: Install Dependencies

    pip install -r requirements.txt

### Step 5: Configure Environment Variables

Create a `.env` file in the project root directory.

Add your local database configuration:

    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=your_mysql_password
    DB_NAME=phishguard_db

Use your actual MySQL credentials locally. Never publish this file.

### Step 6: Run the Application

    python main.py

---

## Running Tests

Run the following commands from the project root directory:

### URL Detection Test

    python -m tests.test_url

### Email Detection Test

    python -m tests.test_email

### Database Test

    python -m tests.test_database

Note: The database test can insert records into your configured database.

---

## Database

PhishGuard uses MySQL to maintain scan records.

The database stores information related to:
- URL scans
- Email scans
- Risk classifications
- Detection results
- Scan timestamps

---

## Security Considerations

- Keep database credentials inside `.env`.
- Never upload `.env` to a public repository.
- Use `.gitignore` to exclude sensitive configuration files.
- Do not assume that a low-risk classification guarantees a URL or email is safe.
- Verify suspicious websites and emails independently.

---

## Project Limitations

- Detection is based on programmed rules and patterns.
- New phishing techniques may not always be detected.
- Risk classifications are indicators, not guarantees.
- The application requires a working MySQL connection for database operations.

---

## Future Enhancements

- Machine learning-based phishing detection.
- Real-time threat intelligence integration.
- Domain reputation checking.
- Advanced email header analysis.
- Improved detection accuracy.
- User authentication and access management.

---

## Project Information

**Project Name:** PhishGuard

**Category:** Cybersecurity

**Application Type:** Python Desktop Application

**Primary Language:** Python

**Database:** MySQL

---

## License

This project is developed for educational and academic purposes.
