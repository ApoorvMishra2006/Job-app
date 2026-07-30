import json

from config import FILE_PATH


class JobManager:
    def __init__(self):
        self.jobs = []
        self.applied_jobs = []

    def load_applied_jobs(self):
        try:
            with open(FILE_PATH, "r") as file:
                self.applied_jobs = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.applied_jobs = []

    def save_applied_jobs(self):
        with open(FILE_PATH, "w") as file:
            json.dump(self.applied_jobs, file, indent=2)

    def add_job(self, job):
        self.jobs.append(job)

    def apply_job(self, job):
        if any(
            applied_job["apply_link"] == job.apply_link
            for applied_job in self.applied_jobs
        ):
            print("Already applied!")
            return

        self.applied_jobs.append({
            "title": job.title,
            "description": job.description,
            "apply_link": job.apply_link
        })

        self.save_applied_jobs()
        print("Applied!!")

    def show_applied_jobs(self):
        print("\nThe applied jobs are:")

        if not self.applied_jobs:
            print("No jobs applied yet.")
        else:
            for i, job in enumerate(self.applied_jobs, start=1):
                print(f"{i}. {job['title']}")
                print(f"Link: {job['apply_link']}")
                print(f"Description: {job['description'][:100]}...")
                print("-" * 60)