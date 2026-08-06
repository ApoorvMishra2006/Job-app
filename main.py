import sys

from managers.job_manager import JobManager
from services.adzuna_api import get_jobs_from_countries
from services.remotive_api import get_remotive_jobs
from config import COUNTRIES, ALL_COUNTRIES
from services.job_utils import remove_duplicate_jobs


def choose_countries():

    while True:

        print("\nChoose search mode")
        print("1. Single Country")
        print("2. Multiple Countries")
        print("3. All Countries")

        mode = input("\nChoice: ")

        if mode in ["1", "2", "3"]:
            break

        print("Please enter 1, 2 or 3.")

    if mode == "1":

        print("\nChoose country:\n")

        for number, (name, code) in COUNTRIES.items():
            print(f"{number}. {name}")

        while True:

            choice = input("\nChoice: ")

            if choice in COUNTRIES:
                break

            print("Please enter a valid country number.")

        return [COUNTRIES[choice][1]]

    elif mode == "2":

        print("\nChoose countries:\n")

        for number, (name, code) in COUNTRIES.items():
            print(f"{number}. {name}")

        choices = input(
            "\nEnter country numbers separated by commas: "
        )

        selected = []

        for choice in choices.split(","):

            choice = choice.strip()

            if choice in COUNTRIES:

                code = COUNTRIES[choice][1]

                if code not in selected:
                    selected.append(code)

        while not selected:

            choices = input(
                "\nEnter country numbers separated by commas: "
            )

            selected = []

            for choice in choices.split(","):

                choice = choice.strip()

                if choice in COUNTRIES:

                    code = COUNTRIES[choice][1]

                    if code not in selected:
                        selected.append(code)

            if not selected:
                print("Please enter at least one valid country.")

        return selected

    elif mode == "3":

        print("\nSearching all supported countries...\n")

        return ALL_COUNTRIES

    else:

        print("Invalid choice.")
        return None


def main():

    while True:

        job_name = input("Enter job keyword: ").strip()

        if job_name:
            break

    print("Job keyword cannot be empty.")

    print("\nChoose job source")
    print("1. Adzuna (location-based jobs)")
    print("2. Remotive (remote jobs)")
    print("3. Both")

    while True:

        source = input("\nChoice: ")

        if source in ["1", "2", "3"]:
            break

        print("Please enter 1, 2 or 3.")

    page = 1
    all_remotive_jobs = []

    if source == "1":

        countries = choose_countries()

        if countries is None:
            return

        salary_min = input(
            "Enter minimum salary (leave blank if none): "
        )

    elif source == "2":

        all_remotive_jobs = get_remotive_jobs(job_name)

    elif source == "3":

        countries = choose_countries()

        if countries is None:
            return

        while True:

            salary_min = input(
                "Enter minimum salary (leave blank if none): "
            ).strip()

            if salary_min == "":
                break

            if salary_min.isdigit():
                break

            print("Please enter a valid salary.")

        print(
            "\nNote:"
            "\nCountry and salary filters apply only to Adzuna."
            "\nRemotive searches remote jobs using only the keyword.\n"
        )

        all_remotive_jobs = get_remotive_jobs(job_name)

    else:

        print("Invalid choice.")
        return
    
    manager = JobManager()
    manager.load_applied_jobs()

    while True:

        if source == "1":

            jobs = remove_duplicate_jobs(
                get_jobs_from_countries(
                    job_name,
                    countries,
                    salary_min,
                    page,
                )
            )


        elif source == "2":

            start = (page - 1) * 50
            end = start + 50

            jobs = remove_duplicate_jobs(
                all_remotive_jobs[start:end]
            )

        elif source == "3":

            adzuna_jobs = get_jobs_from_countries(
                job_name,
                countries,
                salary_min,
                page,
            )

            start = (page - 1) * 50
            end = start + 50

            remotive_jobs = all_remotive_jobs[start:end]

            jobs = remove_duplicate_jobs(
            adzuna_jobs + remotive_jobs
            )

        if not jobs:

            print("\nNo jobs found on this page.")

        else:

            print(f"\n========== PAGE {page} ==========\n")

            for i, job in enumerate(jobs, start=1):

                manager.add_job(job)

                job.display(i)

                while True:

                    applied = input(
                        "Press 1 to apply, 0 to skip or q to exit: "
                    )

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

        print("\nCurrent page:", page)
        print("n - Next page")
        print("p - Previous page")
        print("q - Quit")

        while True:

            nav = input("\nChoice: ").lower()

            if nav == "n":

                page += 1
                break

            elif nav == "p":

                if page > 1:
                    page -= 1
                else:
                    print("Already on the first page.")

                break

            elif nav == "q":

                print("Exiting the program...")
                manager.show_applied_jobs()
                sys.exit()

            else:

                print("Invalid choice.")
if __name__ == "__main__":
    main()