# PhishGuard – Project Structure

## 1. Overview

PhishGuard follows a modular project structure that separates the graphical user interface, backend processing, database operations, testing, and documentation.

This organization makes the application easier to understand, maintain, test, and extend.

## 2. Directory Structure

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
├── reports/
│
├── docs/
│   ├── PROJECT_OVERVIEW.md
│   ├── PROJECT_STRUCTURE.md
│   ├── SYSTEM_ARCHITECTURE.md
│   └── USER_GUIDE.md
│
├── .env
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

> Note: The local virtual environment (`venv/`) is excluded from this documentation tree because it is not intended to be committed to GitHub. The `.env` file is also excluded from public version control because it contains configuration secrets.

## 3. Folder Descriptions

### backend/

Contains the core application logic and processing modules.

| File | Responsibility |
|---|---|
| `database.py` | Handles MySQL database connectivity and scan record operations. |
| `email_detection.py` | Analyzes email content for potential phishing indicators. |
| `reports.py` | Handles the generation of PDF and CSV reports. |
| `url_detection.py` | Analyzes URLs for potentially suspicious characteristics. |
| `__init__.py` | Marks the backend directory as a Python package. |

### frontend/

Contains the graphical user interface.

| File | Responsibility |
|---|---|
| `dashboard.py` | Implements the Tkinter dashboard, user interactions, scan history, statistics, and application screens. |
| `__init__.py` | Marks the frontend directory as a Python package. |

### tests/

Contains testing scripts for the application's major components.

| File | Responsibility |
|---|---|
| `test_database.py` | Tests database-related functionality. |
| `test_email.py` | Tests email detection functionality. |
| `test_url.py` | Tests URL detection functionality. |
| `__init__.py` | Marks the tests directory as a Python package. |

### reports/

A dedicated directory for storing generated application reports, when configured by the application.

### docs/

Contains project documentation, including the overview, project structure, architecture, and user guide.

## 4. Root-Level Files

| File | Responsibility |
|---|---|
| `main.py` | Application entry point used to launch PhishGuard. |
| `README.md` | Provides the main project introduction and setup instructions. |
| `requirements.txt` | Lists the Python dependencies required by the project. |
| `.env` | Stores local environment configuration, including database credentials. |
| `.gitignore` | Specifies files and directories that Git should ignore. |

## 5. Application Organization

The application is divided into separate modules:

1. **Frontend:** Provides the graphical interface and accepts user input.
2. **Backend:** Performs URL and email analysis and handles application operations.
3. **Database:** Stores and retrieves scan information through MySQL.
4. **Reporting:** Generates PDF and CSV reports.
5. **Testing:** Provides scripts for checking individual application components.

## 6. Benefits of This Structure

- Separation of responsibilities.
- Easier maintenance and debugging.
- Better code organization.
- Reusable application modules.
- Simplified testing.
- Easier collaboration and future development.

## 7. Conclusion

The modular structure of PhishGuard provides a clear separation between its interface, processing logic, database operations, testing, and documentation.

This organization supports maintainability and provides a foundation for future enhancements.