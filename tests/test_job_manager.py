from managers.job_manager import JobManager
from models.job import Job


def create_test_manager(tmp_path):

    database_path = tmp_path / "test_jobs.db"

    manager = JobManager.__new__(JobManager)

    manager.jobs = []
    manager.applied_jobs = []
    manager.connection = None

    import sqlite3

    manager.connection = sqlite3.connect(database_path)

    cursor = manager.connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applied_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            apply_link TEXT NOT NULL UNIQUE
        )
    """)

    manager.connection.commit()

    return manager


def test_job_can_be_applied(tmp_path):

    manager = create_test_manager(tmp_path)

    job = Job(
        title="Python Developer",
        company="ABC",
        location="India",
        description="Python backend job",
        apply_link="https://example.com/job1",
        source="Adzuna"
    )

    manager.apply_job(job)

    cursor = manager.connection.cursor()

    cursor.execute("""
        SELECT title, description, apply_link
        FROM applied_jobs
    """)

    result = cursor.fetchone()

    assert result is not None
    assert result[0] == "Python Developer"
    assert result[1] == "Python backend job"
    assert result[2] == "https://example.com/job1"

    manager.close()


def test_applied_jobs_can_be_loaded(tmp_path):

    manager = create_test_manager(tmp_path)

    job = Job(
        title="Backend Developer",
        company="ABC",
        location="India",
        description="Backend job",
        apply_link="https://example.com/job2",
        source="Adzuna"
    )

    manager.apply_job(job)

    manager.load_applied_jobs()

    assert len(manager.applied_jobs) == 1
    assert manager.applied_jobs[0]["title"] == "Backend Developer"
    assert manager.applied_jobs[0]["apply_link"] == "https://example.com/job2"

    manager.close()


def test_duplicate_application_is_prevented(tmp_path):

    manager = create_test_manager(tmp_path)

    job = Job(
        title="Python Developer",
        company="ABC",
        location="India",
        description="Python backend job",
        apply_link="https://example.com/job3",
        source="Adzuna"
    )

    manager.apply_job(job)
    manager.apply_job(job)

    cursor = manager.connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM applied_jobs
        WHERE apply_link = ?
    """, (job.apply_link,))

    count = cursor.fetchone()[0]

    assert count == 1

    manager.close()