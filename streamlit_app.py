import math

import streamlit as st

from config import COUNTRIES, RESULTS_PER_PAGE
from managers.job_manager import JobManager
from services.adzuna_api import get_jobs_from_countries
from services.remotive_api import get_remotive_jobs
from services.job_utils import (
    remove_duplicate_jobs,
    filter_jobs,
    sort_jobs
)
from utils.auth import register_user, login_user


st.set_page_config(
    page_title="Job Aggregator",
    page_icon="💼",
    layout="wide"
)


manager = JobManager()


# --------------------------------------------------
# Authentication Session State
# --------------------------------------------------

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


if "user" not in st.session_state:

    st.session_state.user = None


# --------------------------------------------------
# Login / Sign Up
# --------------------------------------------------

if not st.session_state.logged_in:

    st.title("💼 Job Aggregator")

    st.write(
        "Search jobs from Adzuna and Remotive in one place."
    )

    login_tab, signup_tab = st.tabs(
        [
            "Login",
            "Sign Up"
        ]
    )

    with login_tab:

        st.header("Login")

        login_username = st.text_input(
            "Username",
            key="login_username"
        )

        login_password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        login_button = st.button(
            "Login",
            type="primary"
        )

        if login_button:

            if (
                not login_username.strip()
                or not login_password
            ):

                st.warning(
                    "Please enter your username and password."
                )

            else:

                user = login_user(
                    manager.connection,
                    login_username,
                    login_password
                )

                if user:

                    st.session_state.logged_in = True
                    st.session_state.user = user

                    st.success(
                        "Login successful!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Invalid username or password."
                    )

    with signup_tab:

        st.header("Create Account")

        signup_username = st.text_input(
            "Username",
            key="signup_username"
        )

        signup_email = st.text_input(
            "Email",
            key="signup_email"
        )

        signup_password = st.text_input(
            "Password",
            type="password",
            key="signup_password"
        )

        signup_button = st.button(
            "Create Account",
            type="primary"
        )

        if signup_button:

            success, message = register_user(
                manager.connection,
                signup_username,
                signup_email,
                signup_password
            )

            if success:

                st.success(
                    message
                )

                st.info(
                    "You can now log in."
                )

            else:

                st.error(
                    message
                )

    st.stop()


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "jobs" not in st.session_state:

    st.session_state.jobs = []


if "filtered_jobs" not in st.session_state:

    st.session_state.filtered_jobs = []


if "page" not in st.session_state:

    st.session_state.page = 1


if "search_performed" not in st.session_state:

    st.session_state.search_performed = False


if "current_source" not in st.session_state:

    st.session_state.current_source = ""


user_id = st.session_state.user["id"]

manager.load_applied_jobs(user_id)
manager.load_saved_jobs(user_id)


# --------------------------------------------------
# Main UI
# --------------------------------------------------

st.title("💼 Job Aggregator")

st.write(
    f"Welcome, **{st.session_state.user['username']}**!"
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.write(
    f"Logged in as: "
    f"**{st.session_state.user['username']}**"
)


if st.sidebar.button("Logout"):

    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.jobs = []
    st.session_state.filtered_jobs = []
    st.session_state.search_performed = False
    st.session_state.page = 1

    st.rerun()


page = st.sidebar.radio(
    "Navigation",
    [
        "Search Jobs",
        "Saved Jobs",
        "Applied Jobs"
    ]
)


# ==================================================
# SEARCH JOBS
# ==================================================

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


    # --------------------------------------------------
    # Search
    # --------------------------------------------------

    if search_button:

        if not job_name.strip():

            st.warning(
                "Please enter a job keyword."
            )

        elif (
            source in ["Adzuna", "Both"]
            and not countries
        ):

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

            with st.spinner(
                "Searching for jobs..."
            ):

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

                    adzuna_jobs = (
                        get_jobs_from_countries(
                            job_name.strip(),
                            countries,
                            salary_min,
                            1
                        )
                    )

                    remotive_jobs = (
                        get_remotive_jobs(
                            job_name.strip()
                        )
                    )

                    jobs = (
                        adzuna_jobs
                        + remotive_jobs
                    )

                jobs = remove_duplicate_jobs(
                    jobs
                )

                st.session_state.jobs = jobs

                st.session_state.filtered_jobs = jobs

                st.session_state.page = 1

                st.session_state.search_performed = True

                st.session_state.current_source = source


    # ==================================================
    # FILTERS AND SORTING
    # ==================================================

    if st.session_state.search_performed:

        jobs = st.session_state.jobs

        st.divider()

        st.subheader("🎯 Filters & Sorting")

        filter_col1, filter_col2, filter_col3, filter_col4 = (
            st.columns(4)
        )


        # --------------------------------------------------
        # Job Type
        # --------------------------------------------------

        with filter_col1:

            selected_job_types = st.multiselect(
                "Job Type",
                [
                    "Full-time",
                    "Part-time",
                    "Contract",
                    "Internship",
                    "Temporary"
                ]
            )


        # --------------------------------------------------
        # Work Mode
        # --------------------------------------------------

        with filter_col2:

            selected_work_modes = st.multiselect(
                "Work Mode",
                [
                    "Remote",
                    "Hybrid",
                    "On-site"
                ]
            )


        # --------------------------------------------------
        # Posted Date
        # --------------------------------------------------

        with filter_col3:

            posted_options = {
                "Any time": None,
                "Last 1 day": 1,
                "Last 3 days": 3,
                "Last 7 days": 7,
                "Last 14 days": 14,
                "Last 30 days": 30
            }

            selected_posted = st.selectbox(
                "Posted Within",
                list(posted_options.keys())
            )


        # --------------------------------------------------
        # Sorting
        # --------------------------------------------------

        with filter_col4:

            sort_option = st.selectbox(
                "Sort By",
                [
                    "Default",
                    "Newest first",
                    "Highest salary",
                    "Lowest salary"
                ]
            )


        apply_filters_col, clear_filters_col = (
            st.columns(2)
        )


        # --------------------------------------------------
        # Apply Filters
        # --------------------------------------------------

        with apply_filters_col:

            apply_filters_button = st.button(
                "Apply Filters & Sort",
                type="primary"
            )


        # --------------------------------------------------
        # Clear Filters
        # --------------------------------------------------

        with clear_filters_col:

            clear_filters_button = st.button(
                "Clear Filters"
            )


        if apply_filters_button:

            filtered_jobs = filter_jobs(
                jobs,
                job_types=selected_job_types,
                work_modes=selected_work_modes,
                posted_within=posted_options[
                    selected_posted
                ]
            )

            if sort_option != "Default":

                filtered_jobs = sort_jobs(
                    filtered_jobs,
                    sort_option
                )

            st.session_state.filtered_jobs = (
                filtered_jobs
            )

            st.session_state.page = 1


        if clear_filters_button:

            st.session_state.filtered_jobs = jobs

            st.session_state.page = 1


        # --------------------------------------------------
        # Display Jobs
        # --------------------------------------------------

        jobs = st.session_state.filtered_jobs


        if not jobs:

            st.info(
                "No jobs match your selected filters."
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
                f"Showing {total_jobs} job(s)."
            )


            # ==================================================
            # TOP PAGINATION
            # ==================================================

            previous_col, page_col, next_col = (
                st.columns([1, 2, 1])
            )


            with previous_col:

                if st.button(
                    "← Previous",
                    disabled=(
                        st.session_state.page == 1
                    ),
                    key="previous_top"
                ):

                    st.session_state.page -= 1

                    st.rerun()


            with page_col:

                st.markdown(
                    f"<div style='text-align: center;'>"
                    f"<b>Page "
                    f"{st.session_state.page} "
                    f"of {total_pages}</b>"
                    f"</div>",
                    unsafe_allow_html=True
                )


            with next_col:

                if st.button(
                    "Next →",
                    disabled=(
                        st.session_state.page
                        == total_pages
                    ),
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


            # ==================================================
            # JOB CARDS
            # ==================================================

            for index, job in enumerate(
                page_jobs,
                start=start_index + 1
            ):

                with st.container(
                    border=True
                ):

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


                    # --------------------------------------------------
                    # Salary
                    # --------------------------------------------------

                    salary_min_value = getattr(
                        job,
                        "salary_min",
                        None
                    )

                    salary_max_value = getattr(
                        job,
                        "salary_max",
                        None
                    )


                    if (
                        salary_min_value is not None
                        or salary_max_value is not None
                    ):

                        if (
                            salary_min_value is not None
                            and salary_max_value is not None
                        ):

                            st.write(
                                f"💰 **Salary:** "
                                f"{salary_min_value:,} - "
                                f"{salary_max_value:,}"
                            )

                        elif salary_min_value is not None:

                            st.write(
                                f"💰 **Minimum Salary:** "
                                f"{salary_min_value:,}"
                            )

                        else:

                            st.write(
                                f"💰 **Maximum Salary:** "
                                f"{salary_max_value:,}"
                            )

                    elif job.source == "Remotive":

                        st.write(
                            "💰 **Salary:** Not specified"
                        )


                    # --------------------------------------------------
                    # Posted Date
                    # --------------------------------------------------

                    posted_date = getattr(
                        job,
                        "posted_date",
                        None
                    )

                    if posted_date:

                        st.write(
                            f"📅 **Posted:** "
                            f"{posted_date}"
                        )


                    # --------------------------------------------------
                    # Description
                    # --------------------------------------------------

                    description = (
                        job.description
                        or ""
                    )


                    if description:

                        with st.expander(
                            "📄 View Job Description"
                        ):

                            st.write(
                                description
                            )

                    else:

                        st.write(
                            "No job description available."
                        )


                    # --------------------------------------------------
                    # Application / Save Status
                    # --------------------------------------------------

                    already_applied = any(
                        applied_job["apply_link"]
                        == job.apply_link
                        for applied_job
                        in manager.applied_jobs
                    )


                    already_saved = (
                        manager.is_job_saved(
                            job,
                            user_id
                        )
                    )


                    action_col, save_col, status_col = (
                        st.columns([1, 1, 2])
                    )


                    # --------------------------------------------------
                    # Open Job
                    # --------------------------------------------------

                    with action_col:

                        st.link_button(
                            "Open Job",
                            job.apply_link
                        )


                    # --------------------------------------------------
                    # Save Job
                    # --------------------------------------------------

                    with save_col:

                        if already_saved:

                            if st.button(
                                "⭐ Saved",
                                key=(
                                    f"unsave_{index}_"
                                    f"{job.apply_link}"
                                )
                            ):

                                manager.unsave_job(
                                    job,
                                    user_id
                                )

                                st.rerun()

                        else:

                            if st.button(
                                "☆ Save",
                                key=(
                                    f"save_{index}_"
                                    f"{job.apply_link}"
                                )
                            ):

                                if manager.save_job(
                                    job,
                                    user_id
                                ):

                                    st.success(
                                        "Job saved!"
                                    )

                                    st.rerun()


                    # --------------------------------------------------
                    # Applied Status
                    # --------------------------------------------------

                    with status_col:

                        if already_applied:

                            st.success(
                                "Already applied"
                            )

                        else:

                            if st.button(
                                "Mark as Applied",
                                key=(
                                    f"apply_{index}_"
                                    f"{job.apply_link}"
                                )
                            ):

                                if manager.apply_job(
                                    job,
                                    user_id
                                ):

                                    st.success(
                                        "Job marked as applied!"
                                    )

                                    st.rerun()

                                else:

                                    st.info(
                                        "You have already "
                                        "applied to this job."
                                    )


            # ==================================================
            # BOTTOM PAGINATION
            # ==================================================

            previous_col, page_col, next_col = (
                st.columns([1, 2, 1])
            )


            with previous_col:

                if st.button(
                    "← Previous",
                    disabled=(
                        st.session_state.page == 1
                    ),
                    key="previous_bottom"
                ):

                    st.session_state.page -= 1

                    st.rerun()


            with page_col:

                st.markdown(
                    f"<div style='text-align: center;'>"
                    f"<b>Page "
                    f"{st.session_state.page} "
                    f"of {total_pages}</b>"
                    f"</div>",
                    unsafe_allow_html=True
                )


            with next_col:

                if st.button(
                    "Next →",
                    disabled=(
                        st.session_state.page
                        == total_pages
                    ),
                    key="next_bottom"
                ):

                    st.session_state.page += 1

                    st.rerun()


# ==================================================
# SAVED JOBS
# ==================================================

elif page == "Saved Jobs":

    st.header("⭐ Saved Jobs")

    manager.load_saved_jobs(
        user_id
    )


    if not manager.saved_jobs:

        st.info(
            "You haven't saved any jobs yet."
        )


    else:

        st.success(
            f"You have saved "
            f"{len(manager.saved_jobs)} job(s)."
        )


        for index, job in enumerate(
            manager.saved_jobs,
            start=1
        ):

            with st.container(
                border=True
            ):

                st.subheader(
                    f"{index}. {job['title']}"
                )


                st.write(
                    f"**Company:** {job['company']}"
                )


                st.write(
                    f"**Location:** {job['location']}"
                )


                st.write(
                    f"**Source:** {job['source']}"
                )


                st.write(
                    f"**Saved:** {job['saved_at']}"
                )


                description = (
                    job["description"]
                    or ""
                )


                if description:

                    with st.expander(
                        "📄 View Job Description"
                    ):

                        st.write(
                            description
                        )


                action_col, remove_col = (
                    st.columns([1, 1])
                )


                with action_col:

                    st.link_button(
                        "Open Job",
                        job["apply_link"]
                    )


                with remove_col:

                    if st.button(
                        "Remove Saved",
                        key=(
                            f"remove_saved_{index}_"
                            f"{job['apply_link']}"
                        )
                    ):

                        cursor = (
                            manager.connection.cursor()
                        )

                        cursor.execute(
                            """
                            DELETE FROM saved_jobs
                            WHERE user_id = ?
                            AND apply_link = ?
                            """,
                            (
                                user_id,
                                job["apply_link"]
                            )
                        )

                        manager.connection.commit()

                        st.rerun()


# ==================================================
# APPLIED JOBS
# ==================================================

else:

    st.header("📋 Applied Jobs")

    manager.load_applied_jobs(
        user_id
    )


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

            with st.container(
                border=True
            ):

                st.subheader(
                    f"{index}. {job['title']}"
                )


                st.write(
                    f"**Company:** {job['company']}"
                )


                st.write(
                    f"**Location:** {job['location']}"
                )


                st.write(
                    f"**Source:** {job['source']}"
                )


                st.write(
                    f"**Applied:** {job['applied_at']}"
                )


                description = (
                    job["description"]
                    or ""
                )


                if description:

                    with st.expander(
                        "📄 View Job Description"
                    ):

                        st.write(
                            description
                        )


                st.link_button(
                    "Open Job",
                    job["apply_link"]
                )