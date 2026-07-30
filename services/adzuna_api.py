import requests

from config import APP_ID, APP_KEY, RESULTS_PER_PAGE


def get_job_info(search_term, location, country):
    base_url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"

    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "what": search_term,
        "where": location,
        "results_per_page": RESULTS_PER_PAGE
    }

    try:
        response = requests.get(base_url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException:
        print("Network error")
        return None