import httpx

API_URL = "http://127.0.0.1:8000"


class ApiError(Exception):
    """Raised with a message that is safe to show the user."""


def _error_message(response: httpx.Response) -> str:
    try:
        detail = response.json().get("detail")
    except ValueError:
        return "Unexpected response from the server."
    if isinstance(detail, list):  # FastAPI validation errors
        return str(detail[0].get("msg", "Invalid input."))
    return str(detail)


def _request(method: str, path: str, **kwargs):
    try:
        response = httpx.request(method, f"{API_URL}{path}", timeout=5, **kwargs)
    except httpx.RequestError:
        raise ApiError("Could not reach the server. Is the backend running?") from None
    if response.status_code >= 400:
        raise ApiError(_error_message(response))
    return response.json()


def register(email: str, password: str) -> dict:
    return _request("POST", "/auth/register", json={"email": email, "password": password})


def login(email: str, password: str) -> dict:
    return _request("POST", "/auth/login", json={"email": email, "password": password})


def get_resources(q: str = "", category: str = "") -> list[dict]:
    return _request("GET", "/resources", params={"q": q, "category": category})

def reset_password(email: str, new_password: str) -> dict:
    return _request("POST", "/auth/reset-password", json={"email": email, "password": new_password})