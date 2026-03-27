import pytest
import urllib.request
import urllib.error
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_valid_response():
    response = MagicMock()
    response.status = 200
    return response


@pytest.fixture
def mock_invalid_response():
    return urllib.error.HTTPError(
        url=None, code=401, msg="Unauthorized", hdrs=None, fp=None
    )


def test_valid_login(mock_valid_response):
    with patch("urllib.request.urlopen", return_value=mock_valid_response):
        response = urllib.request.urlopen(
            "http://127.0.0.1:8000/users/?username=admin&password=qwerty"
        )
        assert response.status == 200


def test_invalid_login(mock_invalid_response):
    with patch("urllib.request.urlopen", side_effect=mock_invalid_response):
        try:
            urllib.request.urlopen(
                "http://127.0.0.1:8000/users/?username=admin&password=admin"
            )
            assert False, "Expected HTTP 401 but got 200"
        except urllib.error.HTTPError as e:
            assert e.code == 401
