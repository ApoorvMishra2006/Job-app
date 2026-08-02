import requests

from config import APP_ID, APP_KEY, RESULTS_PER_PAGE
from models.job import Job


def get_job_info(search_term, location, country, salary_min):

    base_url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"

    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "what": search_term,
        "where": location,
        "results_per_page": RESULTS_PER_PAGE
    }

    if salary_min:
        params["salary_min"] = salary_min

    try:

        response = requests.get(base_url, params=params, timeout=5)
        response.raise_for_status()

        data = response.json()

        jobs = []

        for job in data.get("results", []):

            job_obj = Job(
                title=job.get("title", "Unknown"),
                company=job.get("company", {}).get("display_name", "Unknown"),
                location=job.get("location", {}).get("display_name", "Unknown"),
                description=job.get("description", ""),
                apply_link=job.get("redirect_url", ""),
                source="Adzuna"
            )

            jobs.append(job_obj)

        return jobs

    except requests.exceptions.RequestException:

        print(f"Could not connect to Adzuna ({country}).")
        return []


def get_jobs_from_countries(search_term, location, countries, salary_min):

    all_jobs = []

    for country in countries:

        jobs = get_job_info(
            search_term,
            location,
            country,
            salary_min,
        )

        all_jobs.extend(jobs)

    return all_jobs