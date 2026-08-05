import pytest
from fastapi.testclient import TestClient


EXPECTED_V1_ROUTES = [
    "/api/v1/health",
    "/api/v1/interviews",
]


@pytest.fixture(scope="module")
def openapi_paths(client: TestClient) -> set[str]:
    response = client.get("/openapi.json")
    assert response.status_code == 200
    return set(response.json()["paths"])


@pytest.mark.parametrize("route_path", EXPECTED_V1_ROUTES)
def test_openapi_includes_expected_v1_routes(
    openapi_paths: set[str], route_path: str
) -> None:
    assert route_path in openapi_paths