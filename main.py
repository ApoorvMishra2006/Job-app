import sys

from models.job import Job
from managers.job_manager import JobManager
from services.adzuna_api import get_job_info


def main():
    job_name = input("Enter job keyword: ")
    job_location = input("Enter job location: ")
    country_name = input("Enter country code (us,in,gb): ")

    job_info = get_job_info(job_name, job_location, country_name)

    manager = JobManager()
    manager.load_applied_jobs()

    if job_info:
        results = job_info["results"]

        if not results:
            print("No jobs found")
        else:
            print("\nJobs found:\n")

            for i, job in enumerate(results, start=1):

                job_obj = Job(
                    job.get("title", "Unknown"),
                    job.get("company", {}).get("display_name", "Unknown"),
                    job.get("location", {}).get("display_name", "Unknown"),
                    job.get("description", ""),
                    job.get("redirect_url", "")
                )

                manager.add_job(job_obj)

                job_obj.display(i)

                while True:
                    applied = input("Press 1 to apply, 0 to skip or q to exit: ")

                    if applied in ["0", "1", "q"]:
                        break

                    print("You have to press either 1, 0 or q.")

                if applied == "1":
                    manager.apply_job(job_obj)

                elif applied == "q":
                    print("Exiting the program...")
                    manager.show_applied_jobs()
                    sys.exit()

                else:
                    print("Skipped!")

    manager.show_applied_jobs()


if __name__ == "__main__":
    main()