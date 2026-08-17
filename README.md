# Job Aggregator

A Python-based job aggregation application that searches jobs from multiple job platforms in one place. It combines location-based jobs from **Adzuna** with remote jobs from **Remotive**, removes duplicate listings, and lets users keep track of the jobs they have applied to.

---

## Features

* Search jobs by keyword
* Search location-based jobs using the Adzuna API
* Search remote jobs using the Remotive API
* Search across multiple countries
* Search all supported countries at once
* Filter jobs by minimum salary (Adzuna)
* Pagination support
* Duplicate job detection
* Track applied jobs using SQLite
* Prevent duplicate applications
* API error handling
* Application logging
* Automated backend tests
* Streamlit web interface
* Environment variable support for API credentials
* Modular project structure

---

## Technologies Used

- **Python**
- **SQLite**
- **Streamlit**
- **Requests**
- **Pytest**
- **python-dotenv**
- **REST APIs**
- **JSON**
- **Adzuna API**
- **Remotive API**
- **Git**
- **GitHub**

---

## Project Structure

JobApp/
│
├── config.py
├── main.py
├── streamlit_app.py
├── .env
├── README.md
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
├── utils/
│   ├── __init__.py
│   └── logger.py
│
└── tests/
    ├── test_job_utils.py
    ├── test_job_manager.py
    ├── test_adzuna_api.py
    └── test_remotive_api.py

---

## Usage

### Terminal Version

Run:

python main.py

Enter a job keyword.

Choose a job source:

1. Adzuna
2. Remotive
3. Both

Select the required countries and minimum salary when using Adzuna.

Browse jobs and apply through the provided links.

### Streamlit Version

Run:

streamlit run streamlit_app.py

The web interface allows you to:

- Search for jobs
- Select job sources
- Select countries
- Apply salary filters
- View job listings
- Mark jobs as applied
- View previously applied jobs

---

## APIs Used

### Adzuna API

Used for location-based job listings with support for:

- Multiple countries
- Salary filtering
- Pagination

### Remotive API

Used for remote job listings with support for:

- Keyword search
- Remote opportunities
- Pagination

---

## Testing

The project uses **pytest** for automated backend testing.

Run:

pytest

The current test suite covers:

- Duplicate job detection
- SQLite application tracking
- Adzuna API handling
- Remotive API handling

---

## Future Improvements

- Streamlit pagination
- Advanced filtering and sorting
- Improved UI
- Production deployment

---

## Author

Apoorv Mishra