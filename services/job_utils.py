from datetime import datetime, timezone


def remove_duplicate_jobs(jobs):

    seen = set()
    unique_jobs = []

    for job in jobs:

        key = (
            job.title.strip().lower(),
            job.company.strip().lower(),
            job.location.strip().lower()
        )

        if key not in seen:

            seen.add(key)
            unique_jobs.append(job)

    return unique_jobs


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

            job_type = (
                getattr(
                    job,
                    "job_type",
                    None
                )
                or "Unknown"
            ).lower()

            if not any(
                selected.lower() in job_type
                for selected in job_types
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
                or "Unknown"
            ).lower()

            if work_mode not in [
                mode.lower()
                for mode in work_modes
            ]:

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