import re
import requests

from models.job import Job
from utils.logger import logger


def clean_description(description):

    if not description:

        return ""

    # Remove script blocks
    description = re.sub(
        r"<script.*?>.*?</script>",
        " ",
        description,
        flags=re.IGNORECASE | re.DOTALL
    )

    # Remove style blocks
    description = re.sub(
        r"<style.*?>.*?</style>",
        " ",
        description,
        flags=re.IGNORECASE | re.DOTALL
    )

    # Remove HTML tags
    description = re.sub(
        r"<[^>]+>",
        " ",
        description
    )

    # Decode common HTML entities
    description = (
        description
        .replace("&nbsp;", " ")
        .replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
        .replace("&#39;", "'")
    )

    # Remove excessive whitespace
    description = re.sub(
        r"\s+",
        " ",
        description
    )

    return description.strip()


def get_remotive_jobs(search_term):

    url = "https://remotive.com/api/remote-jobs"

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

                description=clean_description(
                    job.get(
                        "description",
                        ""
                    )
                ),

                apply_link=job.get(
                    "url",
                    ""
                ),

                source="Remotive",

                salary_min=None,

                salary_max=None,

                posted_date=job.get(
                    "publication_date"
                )
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

        status_code = error.response.status_code

        logger.error(
            f"Remotive HTTP error "
            f"status_code={status_code}: "
            f"{error}"
        )

        if status_code == 401:

            print(
                "Remotive authentication failed. "
                "Check the API credentials."
            )

        elif status_code == 403:

            print(
                "Remotive access forbidden."
            )

        elif status_code == 429:

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
            "Remotive returned an invalid response."
        )

        return []

    except requests.exceptions.RequestException as error:

        logger.error(
            f"Remotive request failed: "
            f"{error}"
        )

        print(
            f"Remotive request failed: {error}"
        )

        return []