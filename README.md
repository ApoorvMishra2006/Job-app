# Job Aggregator

A Python-based job aggregation application that searches for jobs from multiple job APIs and provides a Streamlit web interface for searching, filtering, pagination, and application tracking.

## Features

* Search jobs using **Adzuna**
* Search remote jobs using **Remotive**
* Search both sources simultaneously
* Search across multiple countries with Adzuna
* Minimum salary filtering for Adzuna
* Automatic duplicate job removal
* API error handling and logging
* Pagination for large search results
* SQLite database for persistent data storage
* User signup and login
* Secure password hashing
* User-specific application tracking
* Track:

  * Job title
  * Company
  * Location
  * Job source
  * Application date and time
  * Job link
* Prevent duplicate applications for the same user
* Streamlit web interface
* Applied Jobs section
* Open the original job listing directly from the application

## Tech Stack

* **Python**
* **Streamlit**
* **SQLite**
* **Requests**
* **python-dotenv**
* **Pytest**
* **Adzuna API**
* **Remotive API**

## Project Structure

```text
JobApp/
│
├── data/
│   └── jobs.db
│
├── managers/
│   ├── __init__.py
│   └── job_manager.py
│
├── models/
│   ├── __init__.py
│   └── job.py
│
├── services/
│   ├── __init__.py
│   ├── adzuna_api.py
│   ├── remotive_api.py
│   └── job_utils.py
│
├── tests/
│   ├── __init__.py
│   ├── test_job_utils.py
│   ├── test_adzuna_api.py
│   └── test_remotive_api.py
│
├── utils/
│   ├── __init__.py
│   ├── auth.py
│   └── logger.py
│
├── .env
├── .gitignore
├── config.py
├── requirements.txt
├── streamlit_app.py
└── README.md
```

## Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd JobApp
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root.

Add your Adzuna credentials:

```text
APP_ID=your_adzuna_app_id
APP_KEY=your_adzuna_app_key
```

The `.env` file should **not** be committed to GitHub.

## Running the Application

Start the Streamlit application:

```bash
streamlit run streamlit_app.py
```

The application provides two main sections:

### Search Jobs

Search for jobs by:

* Job keyword
* Job source
* Country
* Minimum salary

Results can be browsed using pagination.

### Applied Jobs

Users can mark jobs as applied.

Application information is stored in SQLite and associated with the logged-in user.

Each user's application history is separate from other users.

## Authentication

The application supports:

* User registration
* User login
* Logout
* Password hashing
* User-specific application data

Passwords are not stored as plain text. Passwords are hashed using PBKDF2-HMAC-SHA256 with a unique salt.

## Application Tracking

When a user marks a job as applied, the application stores:

* User ID
* Job title
* Company
* Location
* Description
* Job link
* Job source
* Application date and time

The application also prevents a user from applying to the same job multiple times.

Duplicate detection checks both the job link and the combination of:

```text
Job title + Company + Location
```

## Database

The application uses SQLite for persistent storage.

The database is automatically created in:

```text
data/jobs.db
```

The database contains:

### users

Stores registered user information.

### applied_jobs

Stores application tracking information associated with individual users.

The application includes database migration logic so existing databases can be updated when the schema changes without manually deleting the database.

## Testing

The project uses **pytest** for automated testing.

Run all tests:

```bash
pytest
```

Run tests with more detailed output:

```bash
pytest -v
```

The test suite currently covers job utilities and API-related functionality.

## Logging

Application events are recorded using Python's logging system.

Logs are stored in:

```text
logs/app.log
```

Logging helps track:

* API requests
* API errors
* Job search results
* Duplicate removal
* Database initialization
* User registration
* Login attempts
* Application tracking

## API Error Handling

The application handles common API problems such as:

* HTTP errors
* Connection errors
* Request timeouts
* Invalid API responses
* Unexpected API failures

Errors are logged and handled without crashing the entire application.

## Current Limitations

The application currently acts as a **job aggregator and application tracker**.

The `Mark as Applied` functionality records that the user applied to a job. It does not automatically submit the job application.

The actual application process still takes place on the job provider's website.

## Future Improvements

Potential future improvements include:

* User profile management
* Saved jobs
* Search history
* Advanced job filtering
* Improved application tracking
* Application status management
* Resume/profile management
* Further UI improvements
* Deployment
* More comprehensive automated testing

## License

This project is for educational and portfolio purposes.
