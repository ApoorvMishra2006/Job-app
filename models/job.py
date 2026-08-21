class Job:

    def __init__(
        self,
        title,
        company,
        location,
        description,
        apply_link,
        source,
        salary_min=None,
        salary_max=None,
        posted_date=None,
        job_type=None,
        work_mode=None
    ):

        self.title = title
        self.company = company
        self.location = location
        self.description = description
        self.apply_link = apply_link
        self.source = source

        self.salary_min = salary_min
        self.salary_max = salary_max
        self.posted_date = posted_date

        self.job_type = job_type
        self.work_mode = work_mode

    def display(self, index):

        print(
            f"{index}. {self.title}"
        )

        print(
            f"Company: {self.company}"
        )

        print(
            f"Location: {self.location}"
        )

        print(
            f"Source: {self.source}"
        )

        print(
            f"Description: "
            f"{self.description[:150]}..."
        )

        if self.salary_min is not None:

            print(
                f"Minimum Salary: "
                f"{self.salary_min}"
            )

        if self.salary_max is not None:

            print(
                f"Maximum Salary: "
                f"{self.salary_max}"
            )

        if self.job_type:

            print(
                f"Job Type: "
                f"{self.job_type}"
            )

        if self.work_mode:

            print(
                f"Work Mode: "
                f"{self.work_mode}"
            )

        if self.posted_date:

            print(
                f"Posted: "
                f"{self.posted_date}"
            )

        print(
            f"Apply: {self.apply_link}"
        )

        print(
            "-" * 60
        )