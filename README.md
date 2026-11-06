
# PhishGuard
### Phishing Detection and Security Analysis System

PhishGuard is a Python-based desktop application designed to identify and analyze potential phishing threats in website URLs and email content.

It provides rule-based phishing detection, risk classification, scan history management, dashboard statistics, MySQL database integration, and PDF/CSV report generation through a graphical user interface.

## Features

### 1. URL Phishing Detection
- Analyze website URLs.
- Detect suspicious URL patterns and keywords.
- Identify URLs that do not use HTTPS.
- Check for suspicious IP-based URLs.
- Identify potentially misleading URL structures.
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
- Navigate application modules through a sidebar.

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

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| Tkinter | Graphical user interface |
| MySQL | Database management |
| mysql-connector-python | Python–MySQL connectivity |
| python-dotenv | Environment variable management |
| ReportLab | PDF report generation |

## Project Structure

```text
PhishGuard/
│
├── backend/
│   ├── __init__.py
│   ├── database.py
│   ├── email_detection.py
│   ├── reports.py
│   └── url_detection.py
│
├── frontend/
│   ├── __init__.py
│   └── dashboard.py
│
├── tests/
│   ├── __init__.py
│   ├── test_database.py
│   ├── test_email.py
│   └── test_url.py
│
├── docs/
│   ├── PROJECT_OVERVIEW.md
│   ├── PROJECT_STRUCTURE.md
│   ├── SYSTEM_ARCHITECTURE.md
│   └── USER_GUIDE.md
│
├── reports/
│
├── .env
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

Note: `.env` and the virtual environment are local files and are not included in the public repository.

## System Requirements

- Windows 10 or Windows 11
- Python 3.13 or compatible version
- MySQL Server
- pip package manager

## Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/Jaswanthgit4346/PhishGuard.git
cd PhishGuard
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it using PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 4: Configure MySQL

Install and configure MySQL Server.

Create the project database:

```sql
CREATE DATABASE phishguard_db;
```

### Step 5: Configure Environment Variables

Create a `.env` file in the project root directory.

Add your MySQL password:

```env
PHISHGUARD_DB_PASSWORD=your_mysql_password
```

Replace `your_mysql_password` with your actual local MySQL password.

Keep your `.env` file private. Never upload it to GitHub.

### Step 6: Run the Application

```bash
python main.py
```

## Running Tests

Run the following commands from the project root directory.

### URL Detection Test

```bash
python -m tests.test_url
```

### Email Detection Test

```bash
python -m tests.test_email
```

### Database Test

```bash
python -m tests.test_database
```

Note: The database test may insert records into your configured MySQL database.

## Database

PhishGuard uses MySQL to maintain scan records.

The database stores information related to:

- URL scans
- Email scans
- Risk classifications
- Detection results
- Scan timestamps

## Security Considerations

- Keep database credentials inside `.env`.
- Never upload `.env` to a public repository.
- Use `.gitignore` to exclude sensitive configuration files.
- Do not assume that a low-risk classification guarantees a URL or email is safe.
- Verify suspicious websites and emails independently.

## Project Limitations

- Detection is based on programmed rules and patterns.
- New phishing techniques may not always be detected.
- Risk classifications are indicators, not guarantees.
- Database operations require a working MySQL connection.

## Future Enhancements

- Machine learning-based phishing detection.
- Real-time threat intelligence integration.
- Domain reputation checking.
- Advanced email header analysis.
- Improved detection accuracy.
- User authentication and access management.

## Project Information

| Detail | Description |
|---|---|
| Project Name | PhishGuard |
| Category | Cybersecurity |
| Application Type | Python Desktop Application |
| Primary Language | Python |
| GUI Framework | Tkinter |
| Database | MySQL |
| Detection Approach | Rule-based |

## License

This project is developed for educational and academic purposes.
