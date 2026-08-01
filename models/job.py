class Job:
    def __init__(self, title, company, location, description, apply_link, source):
        self.title = title
        self.company = company
        self.location = location
        self.description = description
        self.apply_link = apply_link
        self.source = source

    def display(self, index):
        print(f"{index}. {self.title}")
        print(f"Company: {self.company}")
        print(f"Location: {self.location}")
        print(f"Source: {self.source}")
        print(f"Description: {self.description[:150]}...")
        print(f"Apply: {self.apply_link}")
        print("-" * 60)