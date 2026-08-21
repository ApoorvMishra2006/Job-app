from datetime import datetime

import requests

from models.job import Job
from utils.logger import logger


def get_remotive_jobs(search_term):

    url = (
        "https://remotive.com/api/remote-jobs"
    )

    params = {
        "search": search_term
    }

    logger.info(
        f"Remotive search started: "
        f"keyword='{search_term}'"
    )

    try:

        response = requests.get(
            url,
            params=params,
            timeout=5
        )

        response.raise_for_status()

        data = response.json()

        jobs = []

        for job in data.get(
            "jobs",
            []
        ):

            posted_date = None

            publication_date = job.get(
                "publication_date"
            )

            if publication_date:

                try:

                    posted_date = datetime.fromisoformat(
                        publication_date.replace(
                            "Z",
                            "+00:00"
                        )
                    )

                except ValueError:

                    posted_date = None

            job_type = job.get(
                "job_type",
                "Unknown"
            )

            if job_type:

                job_type = job_type.replace(
                    "_",
                    " "
                ).title()

            else:

                job_type = "Unknown"

            job_obj = Job(

                title=job.get(
                    "title",
                    "Unknown"
                ),

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

                source="Remotive",

                job_type=job_type,

                work_mode="Remote",

                salary_min=job.get(
                    "salary_min"
                ),

                salary_max=job.get(
                    "salary_max"
                ),

                posted_date=posted_date
            )

            jobs.append(
                job_obj
            )

        logger.info(
            f"Remotive returned "
            f"{len(jobs)} jobs"
        )

        return jobs

    except requests.exceptions.Timeout:

        logger.error(
            "Remotive request timed out."
        )

        print(
            "Remotive request timed out."
        )

        return []

    except requests.exceptions.ConnectionError:

        logger.error(
            "Could not connect to Remotive."
        )

        print(
            "Could not connect to Remotive."
        )

        return []

    except requests.exceptions.HTTPError as error:

        status_code = (
            error.response.status_code
        )

        logger.error(
            f"Remotive HTTP error "
            f"status_code={status_code}: "
            f"{error}"
        )

        if status_code == 429:

            print(
                "Remotive rate limit reached. "
                "Please try again later."
            )

        elif status_code >= 500:

            print(
                "Remotive server error. "
                "Please try again later."
            )

        else:

            print(
                f"Remotive request failed. "
                f"HTTP status: {status_code}"
            )

        return []

    except requests.exceptions.JSONDecodeError:

        logger.error(
            "Remotive returned invalid JSON."
        )

        print(
            "Remotive returned an invalid "
            "response."
        )

        return []

    except requests.exceptions.RequestException as error:

        logger.error(
            f"Remotive request failed: {error}"
        )

        print(
            f"Remotive request failed: {error}"
        )

        return []