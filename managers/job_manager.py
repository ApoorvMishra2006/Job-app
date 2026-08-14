import json
import os
import sqlite3

from config import DATABASE_PATH
from models.job import Job


class JobManager:

    def __init__(self):

        self.jobs = []
        self.applied_jobs = []

        self.connection = None

        self.initialize_database()

    def initialize_database(self):

        os.makedirs(
            os.path.dirname(DATABASE_PATH),
            exist_ok=True
        )

        self.connection = sqlite3.connect(DATABASE_PATH)

        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS applied_jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                apply_link TEXT NOT NULL UNIQUE
            )
        """)

        self.connection.commit()

    def load_applied_jobs(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT title, description, apply_link
            FROM applied_jobs
        """)

        rows = cursor.fetchall()

        self.applied_jobs = []

        for row in rows:

            self.applied_jobs.append({
                "title": row[0],
                "description": row[1],
                "apply_link": row[2]
            })

    def add_job(self, job: Job) -> None:

        self.jobs.append(job)

    def apply_job(self, job: Job) -> None:

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT id
            FROM applied_jobs
            WHERE apply_link = ?
        """, (job.apply_link,))

        existing_job = cursor.fetchone()

        if existing_job:

            print("Already applied!")
            return

        cursor.execute("""
            INSERT INTO applied_jobs (
                title,
                description,
                apply_link
            )
            VALUES (?, ?, ?)
        """, (
            job.title,
            job.description,
            job.apply_link
        ))

        self.connection.commit()

        self.load_applied_jobs()

        print("Applied!!")

    def show_applied_jobs(self):

        print("\nThe applied jobs are:")

        if not self.applied_jobs:

            print("No jobs applied yet.")

        else:

            for i, job in enumerate(
                self.applied_jobs,
                start=1
            ):

                print(f"{i}. {job['title']}")
                print(f"Link: {job['apply_link']}")
                print(
                    f"Description: "
                    f"{job['description'][:100]}..."
                )
                print("-" * 60)

    def close(self):

        if self.connection:

            self.connection.close()