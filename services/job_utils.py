from datetime import datetime, timezone


def normalize_job_type(job_type):

    if not job_type:
        return ""

    job_type = str(job_type).strip().lower()

    replacements = {
        "full-time": "full time",
        "full_time": "full time",
        "fulltime": "full time",

        "part-time": "part time",
        "part_time": "part time",
        "parttime": "part time",

        "contractor": "contract",

        "internship": "intern",

        "permanent": "permanent",

        "temporary": "temporary"
    }

    return replacements.get(
        job_type,
        job_type
    )


def filter_jobs(
    jobs,
    job_types=None,
    work_modes=None,
    posted_within=None
):

    filtered_jobs = []

    now = datetime.now(
        timezone.utc
    )

    for job in jobs:

        # -----------------------------
        # Job Type Filter
        # -----------------------------

        if job_types:

            job_type = normalize_job_type(
                getattr(
                    job,
                    "job_type",
                    None
                )
            )

            selected_types = [
                normalize_job_type(
                    selected
                )
                for selected in job_types
            ]

            if not job_type:

                continue

            if not any(
                selected == job_type
                or selected in job_type
                or job_type in selected
                for selected in selected_types
            ):

                continue

        # -----------------------------
        # Work Mode Filter
        # -----------------------------

        if work_modes:

            work_mode = (
                getattr(
                    job,
                    "work_mode",
                    None
                )
                or ""
            ).strip().lower()

            selected_modes = [
                str(mode).strip().lower()
                for mode in work_modes
            ]

            if work_mode not in selected_modes:

                continue

        # -----------------------------
        # Posted Date Filter
        # -----------------------------

        if posted_within:

            posted_date = getattr(
                job,
                "posted_date",
                None
            )

            if not posted_date:

                continue

            if posted_date.tzinfo is None:

                posted_date = posted_date.replace(
                    tzinfo=timezone.utc
                )

            days_old = (
                now - posted_date
            ).days

            if days_old > posted_within:

                continue

        filtered_jobs.append(
            job
        )

    return filtered_jobs


def remove_duplicate_jobs(jobs):

    unique_jobs = []

    seen = set()

    for job in jobs:

        key = (
            job.title.strip().lower(),
            job.company.strip().lower(),
            job.location.strip().lower()
        )

        if key in seen:

            continue

        seen.add(key)

        unique_jobs.append(
            job
        )

    return unique_jobs


def sort_jobs(
    jobs,
    sort_by="Relevance"
):

    if sort_by == "Salary: High to Low":

        return sorted(
            jobs,
            key=lambda job: (
                getattr(
                    job,
                    "salary_max",
                    None
                ) or
                getattr(
                    job,
                    "salary_min",
                    None
                ) or
                0
            ),
            reverse=True
        )

    elif sort_by == "Salary: Low to High":

        return sorted(
            jobs,
            key=lambda job: (
                getattr(
                    job,
                    "salary_min",
                    None
                ) or
                0
            )
        )

    elif sort_by == "Newest":

        return sorted(
            jobs,
            key=lambda job: (
                getattr(
                    job,
                    "posted_date",
                    None
                ) or
                datetime.min.replace(
                    tzinfo=timezone.utc
                )
            ),
            reverse=True
        )

    return jobs