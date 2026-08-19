import os
import sqlite3

from config import DATABASE_PATH
from models.job import Job
from utils.logger import logger


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

        self.connection = sqlite3.connect(
            DATABASE_PATH
        )

        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                password_salt TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS applied_jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                apply_link TEXT NOT NULL,
                UNIQUE(user_id, apply_link),
                FOREIGN KEY(user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE
            )
        """)

        self.connection.commit()

        logger.info(
            "SQLite database initialized."
        )

    def load_applied_jobs(self, user_id):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT
                title,
                description,
                apply_link
            FROM applied_jobs
            WHERE user_id = ?
            """,
            (user_id,)
        )

        rows = cursor.fetchall()

        self.applied_jobs = []

        for row in rows:

            self.applied_jobs.append({
                "title": row[0],
                "description": row[1],
                "apply_link": row[2]
            })

        logger.info(
            f"Loaded {len(self.applied_jobs)} "
            f"applied job(s) for user_id={user_id}."
        )

    def add_job(self, job: Job):

        self.jobs.append(job)

        logger.info(
            f"Job added to current session: "
            f"'{job.title}'"
        )

    def apply_job(self, job, user_id):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM applied_jobs
            WHERE user_id = ?
            AND apply_link = ?
            """,
            (
                user_id,
                job.apply_link
            )
        )

        existing_job = cursor.fetchone()

        if existing_job:

            logger.info(
                f"Job already applied by user_id="
                f"{user_id}: '{job.title}'"
            )

            return False

        cursor.execute(
            """
            INSERT INTO applied_jobs (
                user_id,
                title,
                description,
                apply_link
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                user_id,
                job.title,
                job.description,
                job.apply_link
            )
        )

        self.connection.commit()

        self.load_applied_jobs(user_id)

        logger.info(
            f"Job marked as applied by "
            f"user_id={user_id}: '{job.title}'"
        )

        return True

    def show_applied_jobs(self):

        print("\nThe applied jobs are:")

        if not self.applied_jobs:

            print("No jobs applied yet.")

        else:

            for i, job in enumerate(
                self.applied_jobs,
                start=1
            ):

                print(
                    f"{i}. {job['title']}"
                )

                print(
                    f"Link: {job['apply_link']}"
                )

                print(
                    f"Description: "
                    f"{job['description'][:100]}..."
                )

                print("-" * 60)

    def close(self):

        if self.connection:

            self.connection.close()

            logger.info(
                "SQLite database connection closed."
            )