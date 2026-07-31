import sys

from managers.job_manager import JobManager
from services.adzuna_api import get_job_info


def main():
    job_name = input("Enter job keyword: ")
    job_location = input("Enter job location: ")
    country_name = input("Enter country code (us/in/gb): ")

    salary_min = input("Enter minimum salary (leave blank if none): ")

    jobs = get_job_info(
        job_name,
        job_location,
        country_name,
        salary_min,
    )

    manager = JobManager()
    manager.load_applied_jobs()

    if not jobs:
        print("No jobs found.")

    else:
        print("\nJobs found:\n")

        for i, job in enumerate(jobs, start=1):

            manager.add_job(job)

            job.display(i)

            while True:
                applied = input("Press 1 to apply, 0 to skip or q to exit: ")

                if applied in ["0", "1", "q"]:
                    break

                print("You have to press either 1, 0 or q.")

            if applied == "1":
                manager.apply_job(job)

            elif applied == "q":
                print("Exiting the program...")
                manager.show_applied_jobs()
                sys.exit()

            else:
                print("Skipped!")

    manager.show_applied_jobs()


if __name__ == "__main__":
    main()