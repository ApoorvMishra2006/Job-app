import requests

from models.job import Job


def get_remotive_jobs(search_term):

    url = "https://remotive.com/api/remote-jobs"

    params = {
        "search": search_term
    }

    try:

        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()

        data = response.json()

        jobs = []

        for job in data.get("jobs", []):

            job_obj = Job(
                title=job.get("title", "Unknown"),
                company=job.get("company_name", "Unknown"),
                location=job.get("candidate_required_location", "Remote"),
                description=job.get("description", ""),
                apply_link=job.get("url", ""),
                source="Remotive"
            )

            jobs.append(job_obj)

        return jobs

    except requests.exceptions.RequestException:
        print("Could not connect to Remotive.")
        return []