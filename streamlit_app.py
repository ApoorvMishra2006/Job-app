import streamlit as st

from config import COUNTRIES
from managers.job_manager import JobManager
from services.adzuna_api import get_jobs_from_countries
from services.remotive_api import get_remotive_jobs
from services.job_utils import remove_duplicate_jobs


st.set_page_config(
    page_title="Job Aggregator",
    page_icon="💼",
    layout="wide"
)


st.title("💼 Job Aggregator")
st.write(
    "Search jobs from Adzuna and Remotive in one place."
)


manager = JobManager()
manager.load_applied_jobs()


if "jobs" not in st.session_state:

    st.session_state.jobs = []


job_name = st.text_input(
    "Enter job keyword",
    placeholder="e.g. Python Developer"
)


source = st.selectbox(
    "Choose job source",
    [
        "Adzuna",
        "Remotive",
        "Both"
    ]
)


countries = []

if source in ["Adzuna", "Both"]:

    country_options = {
        name: code
        for name, code in COUNTRIES.values()
    }

    selected_countries = st.multiselect(
        "Choose countries",
        options=list(country_options.keys())
    )

    for country in selected_countries:

        countries.append(
            country_options[country]
        )


salary_min = ""

if source in ["Adzuna", "Both"]:

    salary_min = st.text_input(
        "Minimum salary (optional)",
        placeholder="e.g. 500000"
    )


search_button = st.button(
    "Search Jobs",
    type="primary"
)


if search_button:

    if not job_name.strip():

        st.warning(
            "Please enter a job keyword."
        )

    elif source in ["Adzuna", "Both"] and not countries:

        st.warning(
            "Please select at least one country."
        )

    elif (
        source in ["Adzuna", "Both"]
        and salary_min
        and not salary_min.isdigit()
    ):

        st.warning(
            "Please enter a valid minimum salary."
        )

    else:

        with st.spinner("Searching for jobs..."):

            jobs = []

            if source == "Adzuna":

                jobs = get_jobs_from_countries(
                    job_name.strip(),
                    countries,
                    salary_min,
                    1
                )

            elif source == "Remotive":

                jobs = get_remotive_jobs(
                    job_name.strip()
                )

            elif source == "Both":

                adzuna_jobs = get_jobs_from_countries(
                    job_name.strip(),
                    countries,
                    salary_min,
                    1
                )

                remotive_jobs = get_remotive_jobs(
                    job_name.strip()
                )

                jobs = (
                    adzuna_jobs
                    + remotive_jobs
                )

            jobs = remove_duplicate_jobs(jobs)

            st.session_state.jobs = jobs


jobs = st.session_state.jobs


if jobs:

    st.success(
        f"Found {len(jobs)} jobs."
    )

    for index, job in enumerate(
        jobs,
        start=1
    ):

        with st.container():

            st.subheader(
                f"{index}. {job.title}"
            )

            st.write(
                f"**Company:** {job.company}"
            )

            st.write(
                f"**Location:** {job.location}"
            )

            st.write(
                f"**Source:** {job.source}"
            )

            st.write(
                job.description[:500]
                + "..."
            )

            already_applied = any(
                applied_job["apply_link"]
                == job.apply_link
                for applied_job in manager.applied_jobs
            )

            if already_applied:

                st.success(
                    "Already applied"
                )

            else:

                if st.button(
                    "Mark as Applied",
                    key=f"apply_{index}_{job.apply_link}"
                ):

                    if manager.apply_job(job):

                        st.success(
                            "Job marked as applied!"
                        )

                        st.rerun()

                    else:

                        st.info(
                            "You have already applied to this job."
                        )

            st.link_button(
                "Open Job",
                job.apply_link
            )

            st.divider()


st.subheader("Applied Jobs")

manager.load_applied_jobs()


if not manager.applied_jobs:

    st.info(
        "You haven't applied to any jobs yet."
    )

else:

    for index, job in enumerate(
        manager.applied_jobs,
        start=1
    ):

        st.write(
            f"**{index}. {job['title']}**"
        )

        st.write(
            f"Link: {job['apply_link']}"
        )

        st.divider()