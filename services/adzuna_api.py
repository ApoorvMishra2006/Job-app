import requests

from config import APP_ID, APP_KEY, RESULTS_PER_PAGE
from models.job import Job
from utils.logger import logger


def get_job_info(search_term, country, salary_min, page):

    base_url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/{page}"

    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "what": search_term,
        "results_per_page": RESULTS_PER_PAGE,
    }

    if salary_min:
        params["salary_min"] = salary_min

    logger.info(
        f"Adzuna search started: "
        f"keyword='{search_term}', "
        f"country='{country}', "
        f"page={page}"
    )

    try:

        response = requests.get(
            base_url,
            params=params,
            timeout=5
        )

        response.raise_for_status()

        data = response.json()

        jobs = []

        for job in data.get("results", []):

            job_obj = Job(
                title=job.get("title", "Unknown"),
                company=job.get(
                    "company",
                    {}
                ).get(
                    "display_name",
                    "Unknown"
                ),
                location=job.get(
                    "location",
                    {}
                ).get(
                    "display_name",
                    "Unknown"
                ),
                description=job.get(
                    "description",
                    ""
                ),
                apply_link=job.get(
                    "redirect_url",
                    ""
                ),
                source="Adzuna"
            )

            jobs.append(job_obj)

        logger.info(
            f"Adzuna returned {len(jobs)} jobs "
            f"for country='{country}', page={page}"
        )

        return jobs

    except requests.exceptions.Timeout:

        logger.error(
            f"Adzuna request timed out "
            f"for country='{country}'"
        )

        print(
            f"Adzuna request timed out ({country})."
        )

        return []

    except requests.exceptions.ConnectionError:

        logger.error(
            f"Could not connect to Adzuna "
            f"for country='{country}'"
        )

        print(
            f"Could not connect to Adzuna ({country})."
        )

        return []

    except requests.exceptions.HTTPError as error:

        status_code = error.response.status_code

        logger.error(
            f"Adzuna HTTP error "
            f"for country='{country}', "
            f"status_code={status_code}: {error}"
        )

        if status_code == 401:

            print(
                f"Adzuna authentication failed ({country}). "
                "Check your API credentials."
            )

        elif status_code == 403:

            print(
                f"Adzuna access forbidden ({country})."
            )

        elif status_code == 429:

            print(
                f"Adzuna rate limit reached ({country}). "
                "Please try again later."
            )

        elif status_code >= 500:

            print(
                f"Adzuna server error ({country}). "
                "Please try again later."
            )

        else:

            print(
                f"Adzuna request failed ({country}). "
                f"HTTP status: {status_code}"
            )

        return []

    except requests.exceptions.JSONDecodeError:

        logger.error(
            f"Adzuna returned invalid JSON "
            f"for country='{country}'"
        )

        print(
            f"Adzuna returned an invalid response ({country})."
        )

        return []

    except requests.exceptions.RequestException as error:

        logger.error(
            f"Adzuna request failed "
            f"for country='{country}': {error}"
        )

        print(
            f"Adzuna request failed ({country}): {error}"
        )

        return []


def get_jobs_from_countries(
    search_term,
    countries,
    salary_min,
    page
):

    all_jobs = []

    for country in countries:

        jobs = get_job_info(
            search_term,
            country,
            salary_min,
            page,
        )

        all_jobs.extend(jobs)

    logger.info(
        f"Adzuna total jobs returned: "
        f"{len(all_jobs)}"
    )

    return all_jobs