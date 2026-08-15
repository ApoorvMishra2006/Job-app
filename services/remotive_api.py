import requests

from models.job import Job


def get_remotive_jobs(search_term):

    url = "https://remotive.com/api/remote-jobs"

    params = {
        "search": search_term
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=5
        )

        response.raise_for_status()

        data = response.json()

        jobs = []

        for job in data.get("jobs", []):

            job_obj = Job(
                title=job.get("title", "Unknown"),
                company=job.get(
                    "company_name",
                    "Unknown"
                ),
                location=job.get(
                    "candidate_required_location",
                    "Remote"
                ),
                description=job.get(
                    "description",
                    ""
                ),
                apply_link=job.get(
                    "url",
                    ""
                ),
                source="Remotive"
            )

            jobs.append(job_obj)

        return jobs

    except requests.exceptions.Timeout:

        print(
            "Remotive request timed out."
        )
        return []

    except requests.exceptions.ConnectionError:

        print(
            "Could not connect to Remotive."
        )
        return []

    except requests.exceptions.HTTPError as error:

        if response.status_code == 429:

            print(
                "Remotive rate limit reached. "
                "Please try again later."
            )

        elif response.status_code >= 500:

            print(
                "Remotive server error. "
                "Please try again later."
            )

        else:

            print(
                f"Remotive request failed: {error}"
            )

        return []

    except requests.exceptions.JSONDecodeError:

        print(
            "Remotive returned an invalid response."
        )
        return []

    except requests.exceptions.RequestException as error:

        print(
            f"Remotive request failed: {error}"
        )
        return []