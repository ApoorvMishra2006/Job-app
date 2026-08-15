from utils.logger import logger


def remove_duplicate_jobs(jobs):

    unique_jobs = []
    seen = set()

    duplicate_count = 0

    for job in jobs:

        key = (
            job.title.strip().lower(),
            job.company.strip().lower(),
            job.location.strip().lower()
        )

        if key not in seen:

            seen.add(key)
            unique_jobs.append(job)

        else:

            duplicate_count += 1

    if duplicate_count > 0:

        logger.info(
            f"Removed {duplicate_count} duplicate job(s)."
        )

    return unique_jobs