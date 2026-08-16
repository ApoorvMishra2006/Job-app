from models.job import Job
from services.job_utils import remove_duplicate_jobs


def test_duplicate_jobs_are_removed():

    job1 = Job(
        title="Python Developer",
        company="ABC",
        location="India",
        description="Python job",
        apply_link="link1",
        source="Adzuna"
    )

    job2 = Job(
        title="Python Developer",
        company="ABC",
        location="India",
        description="Same job",
        apply_link="link2",
        source="Remotive"
    )

    jobs = [job1, job2]

    result = remove_duplicate_jobs(jobs)

    assert len(result) == 1


def test_different_jobs_are_not_removed():

    job1 = Job(
        title="Python Developer",
        company="ABC",
        location="India",
        description="Python job",
        apply_link="link1",
        source="Adzuna"
    )

    job2 = Job(
        title="Backend Developer",
        company="ABC",
        location="India",
        description="Backend job",
        apply_link="link2",
        source="Adzuna"
    )

    jobs = [job1, job2]

    result = remove_duplicate_jobs(jobs)

    assert len(result) == 2


def test_duplicate_detection_ignores_case_and_whitespace():

    job1 = Job(
        title="Python Developer",
        company="ABC",
        location="India",
        description="Python job",
        apply_link="link1",
        source="Adzuna"
    )

    job2 = Job(
        title=" python developer ",
        company=" abc ",
        location=" india ",
        description="Same job",
        apply_link="link2",
        source="Remotive"
    )

    jobs = [job1, job2]

    result = remove_duplicate_jobs(jobs)

    assert len(result) == 1