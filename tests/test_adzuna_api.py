import requests

from services.adzuna_api import get_job_info


def test_adzuna_success(monkeypatch):

    class MockResponse:

        def raise_for_status(self):
            pass

        def json(self):
            return {
                "results": [
                    {
                        "title": "Python Developer",
                        "company": {
                            "display_name": "ABC"
                        },
                        "location": {
                            "display_name": "India"
                        },
                        "description": "Python backend job",
                        "redirect_url": "https://example.com/job"
                    }
                ]
            }

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(
        requests,
        "get",
        mock_get
    )

    jobs = get_job_info(
        "python",
        "in",
        "",
        1
    )

    assert len(jobs) == 1
    assert jobs[0].title == "Python Developer"
    assert jobs[0].company == "ABC"
    assert jobs[0].location == "India"
    assert jobs[0].source == "Adzuna"


def test_adzuna_timeout(monkeypatch):

    def mock_get(*args, **kwargs):

        raise requests.exceptions.Timeout

    monkeypatch.setattr(
        requests,
        "get",
        mock_get
    )

    jobs = get_job_info(
        "python",
        "in",
        "",
        1
    )

    assert jobs == []


def test_adzuna_connection_error(monkeypatch):

    def mock_get(*args, **kwargs):

        raise requests.exceptions.ConnectionError

    monkeypatch.setattr(
        requests,
        "get",
        mock_get
    )

    jobs = get_job_info(
        "python",
        "in",
        "",
        1
    )

    assert jobs == []


def test_adzuna_http_error(monkeypatch):

    class MockResponse:

        status_code = 429

        def raise_for_status(self):

            raise requests.exceptions.HTTPError(
                response=self
            )

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(
        requests,
        "get",
        mock_get
    )

    jobs = get_job_info(
        "python",
        "in",
        "",
        1
    )

    assert jobs == []


def test_adzuna_invalid_json(monkeypatch):

    class MockResponse:

        def raise_for_status(self):
            pass

        def json(self):

            raise requests.exceptions.JSONDecodeError(
                "Invalid JSON",
                "",
                0
            )

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(
        requests,
        "get",
        mock_get
    )

    jobs = get_job_info(
        "python",
        "in",
        "",
        1
    )

    assert jobs == []