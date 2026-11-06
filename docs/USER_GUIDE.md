# PhishGuard – User Guide

## 1. Introduction

This guide explains how to install, configure, launch, and use PhishGuard.

PhishGuard is a Python-based desktop application for analyzing potentially suspicious URLs and email content.

## 2. System Requirements

Before installing PhishGuard, ensure that your system has:

- Windows, Linux, or another supported Python environment.
- Python 3.10 or later.
- MySQL Server 8.0 or compatible version.
- Internet access for downloading dependencies.
- Basic knowledge of using a terminal.

## 3. Installation

### Step 1: Install Python

Download and install Python from:

https://www.python.org/downloads/

Verify the installation:

```bash
python --version
```

### Step 2: Install MySQL

Install MySQL Server and ensure that the database service is running.

Official download:

https://dev.mysql.com/downloads/mysql/

### Step 3: Obtain the Project

Clone the PhishGuard repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Alternatively, download the repository as a ZIP file and extract it.

Navigate to the project directory:

```bash
cd PhishGuard
```

## 4. Environment Setup

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the required dependencies:

```bash
python -m pip install -r requirements.txt
```

## 5. Database Configuration

PhishGuard uses MySQL to store scan records.

Open MySQL and create the application database if it does not already exist:

```sql
CREATE DATABASE phishguard_db;
```

Configure the database connection using a local `.env` file.

Use the environment variable names and configuration format expected by `backend/database.py`.

**Important:** Replace placeholder credentials with your own local MySQL credentials. Never publish your actual database password or `.env` file on GitHub.

## 6. Running PhishGuard

After completing the installation and database configuration, launch the application:

```bash
python main.py
```

The PhishGuard desktop dashboard should open.

## 7. Using the Application

### 7.1 Dashboard

The dashboard provides an overview of application activity, including available scan statistics.

### 7.2 URL Analysis

1. Open the URL scanning section.
2. Enter the URL you want to analyze.
3. Start the scan.
4. Review the risk classification and analysis results.

### 7.3 Email Analysis

1. Open the email scanning section.
2. Enter or paste the email content.
3. Start the analysis.
4. Review the detected phishing indicators and risk classification.

### 7.4 Scan History

The scan history section allows users to:

- View previous URL scans.
- View previous email scans.
- Review risk classifications.
- Search or filter available records.
- Delete individual records.
- Clear scan history.

### 7.5 Dashboard Statistics

The dashboard provides statistics based on stored scan records.

### 7.6 Report Generation

Users can generate reports in supported formats:

- PDF
- CSV

Follow the application's report generation options to create and save reports.

## 8. Running Tests

PhishGuard includes testing scripts for its main components.

Run the following commands from the project root:

**Database test**

```bash
python -m tests.test_database
```

**Email detection test**

```bash
python -m tests.test_email
```

**URL detection test**

```bash
python -m tests.test_url
```

Some tests may require user input or a working MySQL connection.

## 9. Troubleshooting

| Problem | Suggested Solution |
|---|---|
| Python command not recognized | Check Python installation and PATH configuration. |
| Module not found | Activate the virtual environment and install requirements. |
| Database connection failed | Verify MySQL is running and check local database credentials. |
| Database does not exist | Create `phishguard_db` in MySQL. |
| Application does not launch | Check the terminal for Python errors. |
| Report generation fails | Verify the required reporting dependencies are installed. |

## 10. Security Recommendations

- Never share database passwords publicly.
- Keep `.env` excluded from Git.
- Do not enter real passwords or sensitive personal information into test inputs.
- Treat detection results as indicators rather than guaranteed security verdicts.
- Do not open suspicious links simply because a scan reports a low risk.

## 11. Limitations

PhishGuard currently uses predefined detection rules. It does not guarantee detection of every phishing attack.

A low-risk result does not guarantee that a URL or email is safe.

## 12. Conclusion

PhishGuard provides an accessible desktop interface for basic URL and email phishing analysis.

This guide helps users install, configure, and operate the application while following basic security practices.