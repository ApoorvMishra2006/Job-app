def remove_duplicate_jobs(jobs):

    unique_jobs = []
    seen = set()

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