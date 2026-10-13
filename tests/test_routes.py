import pytest
from unittest.mock import patch
from app.routes.routes import toggle_state


def test_home_page(client):
    """Test that the home page loads successfully."""
    response = client.get("/")

    assert response.status_code == 200

def test_about_page(client):
    """Test that the about page loads successfully."""
    response = client.get("/about")

    assert response.status_code == 200

def test_start_page_toggle_false(client):
    """Test the start page when toggle_state['active'] is False."""
    toggle_state["active"] = False
    response = client.get("/start")
    assert response.status_code == 200

def test_start_page_toggle_true(client):
    """Test the start page when toggle_state['active'] is True."""
    toggle_state["active"] = True
    response = client.get("/start")
    assert response.status_code == 200

@patch("app.routes.routes.DataManager")
def test_get_partial(mock_data_manager, client):
    """Test partial question route with mocked DataManager response."""
    mock_instance = mock_data_manager.return_value
    mock_data_manager.getQuestions.return_value = {"question_text": "What is Python?"}

    response = client.get("/get-partial/question/some-view-name")

    assert response.status_code == 200
    mock_instance.getQuestion.assert_called_once_with("some-view-name")

@patch("app.routes.routes.DataGenerator")
def test_fetch_data(mock_data_generator, client):
    """Test fetch data route with mocked DataGenerator response."""
    # Mock the return value of the generate_data
    mock_instance = mock_data_generator.return_value
    mock_instance.generate_data.return_value = ["Item1", "Item2", "Item3"]

    response = client.get("/fetch/data")

    assert response.status_code == 200
    mock_instance.generate_data.assert_called_once_with("external", True)
