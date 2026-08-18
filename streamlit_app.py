import math

import streamlit as st

from config import COUNTRIES, RESULTS_PER_PAGE
from managers.job_manager import JobManager
from services.adzuna_api import get_jobs_from_countries
from services.remotive_api import get_remotive_jobs
from services.job_utils import remove_duplicate_jobs


st.set_page_config(
    page_title="Job Aggregator",
    page_icon="💼",
    layout="wide"
)


manager = JobManager()
manager.load_applied_jobs()


if "jobs" not in st.session_state:

    st.session_state.jobs = []


if "page" not in st.session_state:

    st.session_state.page = 1


if "search_performed" not in st.session_state:

    st.session_state.search_performed = False


if "current_source" not in st.session_state:

    st.session_state.current_source = ""


st.title("💼 Job Aggregator")

st.write(
    "Search jobs from Adzuna and Remotive in one place."
)


page = st.sidebar.radio(
    "Navigation",
    [
        "Search Jobs",
        "Applied Jobs"
    ]
)


if page == "Search Jobs":

    st.header("🔎 Search Jobs")

    job_name = st.text_input(
        "Job keyword",
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
        "🔎 Search Jobs",
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

                st.session_state.page = 1

                st.session_state.search_performed = True

                st.session_state.current_source = source


    if st.session_state.search_performed:

        jobs = st.session_state.jobs


        if not jobs:

            st.info(
                "No jobs found for your search."
            )


        else:

            total_jobs = len(jobs)


            total_pages = math.ceil(
                total_jobs / RESULTS_PER_PAGE
            )


            if st.session_state.page > total_pages:

                st.session_state.page = total_pages


            start_index = (
                st.session_state.page - 1
            ) * RESULTS_PER_PAGE


            end_index = (
                start_index + RESULTS_PER_PAGE
            )


            page_jobs = jobs[
                start_index:end_index
            ]


            st.success(
                f"Found {total_jobs} unique jobs."
            )


            previous_col, page_col, next_col = st.columns(
                [1, 2, 1]
            )


            with previous_col:

                if st.button(
                    "← Previous",
                    disabled=st.session_state.page == 1,
                    key="previous_top"
                ):

                    st.session_state.page -= 1

                    st.rerun()


            with page_col:

                st.markdown(
                    f"<div style='text-align: center;'>"
                    f"<b>Page {st.session_state.page} "
                    f"of {total_pages}</b>"
                    f"</div>",
                    unsafe_allow_html=True
                )


            with next_col:

                if st.button(
                    "Next →",
                    disabled=st.session_state.page == total_pages,
                    key="next_top"
                ):

                    st.session_state.page += 1

                    st.rerun()


            st.write(
                f"Showing jobs "
                f"{start_index + 1}–"
                f"{min(end_index, total_jobs)} "
                f"of {total_jobs}"
            )


            for index, job in enumerate(
                page_jobs,
                start=start_index + 1
            ):

                with st.container(border=True):

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


                    description = job.description

                    if len(description) > 500:

                        description = (
                            description[:500]
                            + "..."
                        )


                    st.write(description)


                    already_applied = any(
                        applied_job["apply_link"]
                        == job.apply_link
                        for applied_job in manager.applied_jobs
                    )


                    action_col, status_col = st.columns(
                        [1, 2]
                    )


                    with action_col:

                        st.link_button(
                            "Open Job",
                            job.apply_link
                        )


                    with status_col:

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
                                        "You have already applied "
                                        "to this job."
                                    )


            previous_col, page_col, next_col = st.columns(
                [1, 2, 1]
            )


            with previous_col:

                if st.button(
                    "← Previous",
                    disabled=st.session_state.page == 1,
                    key="previous_bottom"
                ):

                    st.session_state.page -= 1

                    st.rerun()


            with page_col:

                st.markdown(
                    f"<div style='text-align: center;'>"
                    f"<b>Page {st.session_state.page} "
                    f"of {total_pages}</b>"
                    f"</div>",
                    unsafe_allow_html=True
                )


            with next_col:

                if st.button(
                    "Next →",
                    disabled=st.session_state.page == total_pages,
                    key="next_bottom"
                ):

                    st.session_state.page += 1

                    st.rerun()


else:

    st.header("📋 Applied Jobs")


    manager.load_applied_jobs()


    if not manager.applied_jobs:

        st.info(
            "You haven't applied to any jobs yet."
        )


    else:

        st.success(
            f"You have applied to "
            f"{len(manager.applied_jobs)} job(s)."
        )


        for index, job in enumerate(
            manager.applied_jobs,
            start=1
        ):

            with st.container(border=True):

                st.subheader(
                    f"{index}. {job['title']}"
                )


                st.write(
                    f"**Link:** {job['apply_link']}"
                )
                