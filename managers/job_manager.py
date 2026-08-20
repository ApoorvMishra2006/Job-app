import os
import sqlite3
from datetime import datetime

from config import DATABASE_PATH
from models.job import Job
from utils.logger import logger


class JobManager:

    def __init__(self):

        self.jobs = []
        self.applied_jobs = []
        self.saved_jobs = []

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

        cursor.execute(
            "PRAGMA foreign_keys = ON"
        )

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

        self.migrate_applied_jobs()
        self.migrate_saved_jobs()

        logger.info(
            "SQLite database initialized."
        )

    def migrate_applied_jobs(self):

        cursor = self.connection.cursor()

        cursor.execute(
            "PRAGMA table_info(applied_jobs)"
        )

        columns = [
            row[1]
            for row in cursor.fetchall()
        ]

        if "company" not in columns:

            cursor.execute("""
                ALTER TABLE applied_jobs
                ADD COLUMN company TEXT
                DEFAULT 'Unknown'
            """)

            logger.info(
                "Added 'company' column to applied_jobs."
            )

        if "location" not in columns:

            cursor.execute("""
                ALTER TABLE applied_jobs
                ADD COLUMN location TEXT
                DEFAULT 'Unknown'
            """)

            logger.info(
                "Added 'location' column to applied_jobs."
            )

        if "source" not in columns:

            cursor.execute("""
                ALTER TABLE applied_jobs
                ADD COLUMN source TEXT
                DEFAULT 'Unknown'
            """)

            logger.info(
                "Added 'source' column to applied_jobs."
            )

        if "applied_at" not in columns:

            cursor.execute("""
                ALTER TABLE applied_jobs
                ADD COLUMN applied_at TEXT
                DEFAULT 'Unknown'
            """)

            logger.info(
                "Added 'applied_at' column to applied_jobs."
            )

        self.connection.commit()

        cursor.execute("""
            UPDATE applied_jobs
            SET company = 'Unknown'
            WHERE company IS NULL
            OR company = ''
        """)

        cursor.execute("""
            UPDATE applied_jobs
            SET location = 'Unknown'
            WHERE location IS NULL
            OR location = ''
        """)

        cursor.execute("""
            UPDATE applied_jobs
            SET source = 'Unknown'
            WHERE source IS NULL
            OR source = ''
        """)

        cursor.execute("""
            UPDATE applied_jobs
            SET applied_at = 'Unknown'
            WHERE applied_at IS NULL
            OR applied_at = ''
        """)

        self.connection.commit()

        logger.info(
            "Applied jobs database migration completed."
        )

    def migrate_saved_jobs(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name = 'saved_jobs'
        """)

        table_exists = cursor.fetchone()

        if not table_exists:

            cursor.execute("""
                CREATE TABLE saved_jobs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    company TEXT,
                    location TEXT,
                    description TEXT,
                    apply_link TEXT NOT NULL,
                    source TEXT,
                    saved_at TEXT NOT NULL,
                    UNIQUE(user_id, apply_link),
                    FOREIGN KEY(user_id)
                        REFERENCES users(id)
                        ON DELETE CASCADE
                )
            """)

            self.connection.commit()

            logger.info(
                "Created saved_jobs table."
            )

        else:

            logger.info(
                "saved_jobs table already exists."
            )

    def load_applied_jobs(self, user_id):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT
                title,
                company,
                location,
                description,
                apply_link,
                source,
                applied_at
            FROM applied_jobs
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user_id,)
        )

        rows = cursor.fetchall()

        self.applied_jobs = []

        for row in rows:

            self.applied_jobs.append({
                "title": row[0],
                "company": row[1],
                "location": row[2],
                "description": row[3],
                "apply_link": row[4],
                "source": row[5],
                "applied_at": row[6]
            })

        logger.info(
            f"Loaded {len(self.applied_jobs)} "
            f"applied job(s) for user_id={user_id}."
        )

    def load_saved_jobs(self, user_id):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT
                title,
                company,
                location,
                description,
                apply_link,
                source,
                saved_at
            FROM saved_jobs
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user_id,)
        )

        rows = cursor.fetchall()

        self.saved_jobs = []

        for row in rows:

            self.saved_jobs.append({
                "title": row[0],
                "company": row[1],
                "location": row[2],
                "description": row[3],
                "apply_link": row[4],
                "source": row[5],
                "saved_at": row[6]
            })

        logger.info(
            f"Loaded {len(self.saved_jobs)} "
            f"saved job(s) for user_id={user_id}."
        )

    def is_job_saved(self, job, user_id):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM saved_jobs
            WHERE user_id = ?
            AND apply_link = ?
            """,
            (
                user_id,
                job.apply_link
            )
        )

        if cursor.fetchone():

            return True

        cursor.execute(
            """
            SELECT id
            FROM saved_jobs
            WHERE user_id = ?
            AND LOWER(TRIM(title)) = LOWER(TRIM(?))
            AND LOWER(TRIM(company)) = LOWER(TRIM(?))
            AND LOWER(TRIM(location)) = LOWER(TRIM(?))
            """,
            (
                user_id,
                job.title,
                job.company,
                job.location
            )
        )

        return cursor.fetchone() is not None

    def save_job(self, job, user_id):

        if self.is_job_saved(
            job,
            user_id
        ):

            logger.info(
                f"Job already saved by user_id="
                f"{user_id}: '{job.title}'"
            )

            return False

        saved_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO saved_jobs (
                user_id,
                title,
                company,
                location,
                description,
                apply_link,
                source,
                saved_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                job.title,
                job.company,
                job.location,
                job.description,
                job.apply_link,
                job.source,
                saved_at
            )
        )

        self.connection.commit()

        self.load_saved_jobs(user_id)

        logger.info(
            f"Job saved by user_id="
            f"{user_id}: '{job.title}'"
        )

        return True

    def unsave_job(self, job, user_id):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            DELETE FROM saved_jobs
            WHERE user_id = ?
            AND apply_link = ?
            """,
            (
                user_id,
                job.apply_link
            )
        )

        deleted = cursor.rowcount

        self.connection.commit()

        self.load_saved_jobs(user_id)

        if deleted:

            logger.info(
                f"Job unsaved by user_id="
                f"{user_id}: '{job.title}'"
            )

            return True

        return False

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
            SELECT id
            FROM applied_jobs
            WHERE user_id = ?
            AND LOWER(TRIM(title)) = LOWER(TRIM(?))
            AND LOWER(TRIM(company)) = LOWER(TRIM(?))
            AND LOWER(TRIM(location)) = LOWER(TRIM(?))
            """,
            (
                user_id,
                job.title,
                job.company,
                job.location
            )
        )

        existing_job = cursor.fetchone()

        if existing_job:

            logger.info(
                f"Duplicate job detected for user_id="
                f"{user_id}: '{job.title}'"
            )

            return False

        applied_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor.execute(
            """
            INSERT INTO applied_jobs (
                user_id,
                title,
                company,
                location,
                description,
                apply_link,
                source,
                applied_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                job.title,
                job.company,
                job.location,
                job.description,
                job.apply_link,
                job.source,
                applied_at
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
                    f"Company: {job['company']}"
                )

                print(
                    f"Location: {job['location']}"
                )

                print(
                    f"Source: {job['source']}"
                )

                print(
                    f"Applied at: "
                    f"{job['applied_at']}"
                )

                print(
                    f"Link: {job['apply_link']}"
                )

                print("-" * 60)

    def close(self):

        if self.connection:

            self.connection.close()

            logger.info(
                "SQLite database connection closed."
            )