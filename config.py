import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")

DATABASE_PATH = os.path.join(DATA_DIR, "jobs.db")

try:

    import streamlit as st

    APP_ID = st.secrets.get(
        "APP_ID",
        os.getenv("APP_ID")
    )

    APP_KEY = st.secrets.get(
        "APP_KEY",
        os.getenv("APP_KEY")
    )

except Exception:

    APP_ID = os.getenv("APP_ID")
    APP_KEY = os.getenv("APP_KEY")

RESULTS_PER_PAGE = 50

COUNTRIES = {
    "1": ("India", "in"),
    "2": ("United States", "us"),
    "3": ("United Kingdom", "gb"),
    "4": ("Canada", "ca"),
    "5": ("Australia", "au"),
    "6": ("Germany", "de"),
    "7": ("France", "fr"),
    "8": ("Netherlands", "nl"),
    "9": ("Poland", "pl"),
    "10": ("Singapore", "sg"),
    "11": ("Brazil", "br"),
    "12": ("Mexico", "mx"),
}


ALL_COUNTRIES = [
    "in",
    "us",
    "gb",
    "ca",
    "au",
    "de",
    "fr",
    "nl",
    "pl",
    "sg",
    "br",
    "mx",
]