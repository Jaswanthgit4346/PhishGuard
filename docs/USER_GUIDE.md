
# PhishGuard - User Guide

## 1. Introduction

PhishGuard is a Python-based desktop application designed to analyze website URLs and email content for potential phishing threats.

This guide explains how to install, configure, run, and use the application.

## 2. System Requirements

| Component | Requirement |
|---|---|
| Operating System | Windows 10 or Windows 11 |
| Programming Language | Python 3.13 or compatible version |
| Database | MySQL Server |
| Package Manager | pip |
| GUI Framework | Tkinter |

## 3. Download the Project

Open PowerShell or the VS Code terminal.

Clone the GitHub repository:

```powershell
git clone https://github.com/Jaswanthgit4346/PhishGuard.git
```

Navigate into the project directory:

```powershell
cd PhishGuard
```

## 4. Create a Virtual Environment

Create a Python virtual environment:

```powershell
python -m venv venv
```

Activate the environment:

```powershell
.\venv\Scripts\Activate.ps1
```

After activation, the terminal should display `(venv)`.

## 5. Install Dependencies

Install all required Python packages:

```powershell
python -m pip install -r requirements.txt
```

The project uses the following packages:

- mysql-connector-python
- python-dotenv
- reportlab

## 6. Configure the MySQL Database

### 6.1 Install MySQL

Install and configure MySQL Server on your computer.

Make sure the MySQL service is running.

### 6.2 Create the Database

Open MySQL and execute:

```sql
CREATE DATABASE phishguard_db;
```

The application uses this database to store URL and email scan records.

### 6.3 Configure the Database Password

Create a file named `.env` in the root PhishGuard directory.

Add the following configuration:

```env
PHISHGUARD_DB_PASSWORD=your_mysql_password
```

Replace `your_mysql_password` with your actual local MySQL password.

Keep this file private. It must not be uploaded to GitHub.

## 7. Run the Application

Make sure the virtual environment is activated and MySQL Server is running.

Execute:

```powershell
python main.py
```

The PhishGuard desktop application should open.

## 8. Using the Application

### 8.1 Dashboard

The dashboard provides an overview of the application's scan activity.

Users can view:
- Total scan statistics.
- URL and email scan information.
- Risk distribution.
- Application navigation options.

### 8.2 URL Scanner

The URL Scanner analyzes a website URL and checks for suspicious characteristics.

The application evaluates programmed indicators such as:
- HTTPS usage.
- Suspicious keywords.
- IP-based hostnames.
- URL length.
- Suspicious URL structure.

The application displays a risk classification and detection results.

### 8.3 Email Analyzer

The Email Analyzer evaluates email content for potential phishing indicators.

It checks for:
- Suspicious phrases.
- Urgent or pressuring language.
- Insecure links.
- Suspicious URL patterns.

The analysis produces a risk classification and associated findings.

### 8.4 Scan History

The Scan History section displays previously stored URL and email scan records.

Users can:
- View previous scans.
- Search and filter records.
- Identify risk levels through colour coding.
- Delete individual records.
- Clear history after confirmation.

### 8.5 Reports

The Reports section provides options to generate and export scan information.

Supported formats:
- PDF
- CSV

Generated reports can be saved and reviewed outside the application.

### 8.6 Settings

The Settings section provides access to the application's available configuration and database-related options.

## 9. Running the Tests

The project contains separate test modules.

### URL Detection Test

```powershell
python -m tests.test_url
```

This test module allows URL detection functionality to be checked.

### Email Detection Test

```powershell
python -m tests.test_email
```

This test module checks email analysis functionality.

### Database Test

```powershell
python -m tests.test_database
```

This test module checks database connectivity and scan-history operations.

Note: The database test may create records in the configured database.

## 10. Troubleshooting

### Problem: MySQL Connection Failed

Possible reasons:
- MySQL Server is not running.
- Database does not exist.
- Incorrect MySQL password.
- Incorrect database configuration.

Solutions:
1. Check whether MySQL Server is running.
2. Verify that `phishguard_db` exists.
3. Check the password in `.env`.
4. Restart the application.

### Problem: Module Not Found

Install the required packages:

```powershell
python -m pip install -r requirements.txt
```

### Problem: Application Does Not Start

Check the Python version:

```powershell
python --version
```

Check whether the virtual environment is activated.

Also verify that all required project files are present.

## 11. Security Guidelines

- Never share your MySQL password.
- Never upload `.env` to GitHub.
- Avoid opening suspicious URLs.
- Do not enter personal credentials on untrusted websites.
- Treat detection results as indicators rather than guarantees.

## 12. Limitations

PhishGuard currently uses rule-based detection.

It does not guarantee the detection of every phishing website or email.

A low-risk result does not guarantee that the analyzed content is safe.

The application is intended for educational and demonstration purposes.

## 13. Future Enhancements

Possible improvements include:

- Machine learning-based phishing detection.
- Real-time threat intelligence.
- Domain reputation analysis.
- Advanced email header analysis.
- Improved detection techniques.

## 14. Conclusion

PhishGuard provides a desktop-based environment for analyzing potentially malicious URLs and email content.

It combines Python, Tkinter, and MySQL to provide phishing analysis, risk classification, scan-history management, and report generation.

This guide provides the basic instructions required to install and use the application.
