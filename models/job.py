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
        posted_date=None
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
            f"Salary: "
            f"{self.salary_min or 'Not specified'}"
            f" - "
            f"{self.salary_max or 'Not specified'}"
        )

        print(
            f"Posted: "
            f"{self.posted_date or 'Not specified'}"
        )

        print(
            f"Description: "
            f"{self.description[:150]}..."
        )

        print(
            f"Apply: {self.apply_link}"
        )

        print("-" * 60)