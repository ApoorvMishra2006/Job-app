import requests

from services.remotive_api import get_remotive_jobs


def test_remotive_success(monkeypatch):

    class MockResponse:

        def raise_for_status(self):
            pass

        def json(self):
            return {
                "jobs": [
                    {
                        "title": "Python Developer",
                        "company_name": "ABC",
                        "candidate_required_location": "Remote",
                        "description": "Python backend job",
                        "url": "https://example.com/job"
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

    jobs = get_remotive_jobs("python")

    assert len(jobs) == 1
    assert jobs[0].title == "Python Developer"
    assert jobs[0].company == "ABC"
    assert jobs[0].location == "Remote"
    assert jobs[0].source == "Remotive"


def test_remotive_timeout(monkeypatch):

    def mock_get(*args, **kwargs):

        raise requests.exceptions.Timeout

    monkeypatch.setattr(
        requests,
        "get",
        mock_get
    )

    jobs = get_remotive_jobs("python")

    assert jobs == []


def test_remotive_connection_error(monkeypatch):

    def mock_get(*args, **kwargs):

        raise requests.exceptions.ConnectionError

    monkeypatch.setattr(
        requests,
        "get",
        mock_get
    )

    jobs = get_remotive_jobs("python")

    assert jobs == []


def test_remotive_http_error(monkeypatch):

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

    jobs = get_remotive_jobs("python")

    assert jobs == []


def test_remotive_invalid_json(monkeypatch):

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

    jobs = get_remotive_jobs("python")

    assert jobs == []