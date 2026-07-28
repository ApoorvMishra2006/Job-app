import requests
import json

file_path = r"C:\Users\Apoorv Mishra\Desktop\Apoorv_Py\JobApp\applied.json"

app_id = "7f611dde"
app_key = "20ad94644ef7f5e8c66f14b883aabd86"

class Job:
    def __init__(self, title, company, location, description, apply_link):
        self.title = title
        self.company = company
        self.location = location
        self.description = description
        self.apply_link = apply_link

    def display(self, index):
        print(f"{index}. {self.title}")
        print(f"Company: {self.company}")
        print(f"Location: {self.location}")
        print(f"Description: {self.description[:150]}...")
        print(f"Apply: {self.apply_link}")
        print("-" * 50)

class JobManager:
    def __init__(self):
        self.jobs = []
        self.applied_jobs = []

    def load_applied_jobs(self):
        try:
            with open(file_path, "r") as file:
                self.applied_jobs = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.applied_jobs = []

    def save_applied_jobs(self):
        with open(file_path, "w") as file:
            json.dump(self.applied_jobs, file, indent=2)

    def add_job(self, job):
        self.jobs.append(job)

    def apply_job(self, job):
        if job.apply_link not in self.applied_jobs:
            self.applied_jobs.append(job.apply_link)
            self.save_applied_jobs()
            print("Applied!!")
        else:
            print("Already applied!")

    def show_applied_jobs(self):
        print("\nThe applied jobs are:")
        if not self.applied_jobs:
            print("No jobs applied yet.")
        else:
            for i, job in enumerate(self.applied_jobs, start=1):
                print(f"{i}. {job}")

def get_job_info(search_term, location, country):
    base_url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "what": search_term,
        "where": location
    }

    try:
        response = requests.get(base_url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        print("Network error")
        return None

job_name = input("enter job keyword: ")
job_location = input("enter job location: ")
country_name = input("enter country code (us,in,gb): ")

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
                applied = input("press 1 to apply and 0 to skip: ")
                if applied in ["0", "1"]:
                    break
                else:
                    print("You have to press either 1 or 0")

            if applied == "1":
                manager.apply_job(job_obj)
            else:
                print("Skipped!")

manager.show_applied_jobs()