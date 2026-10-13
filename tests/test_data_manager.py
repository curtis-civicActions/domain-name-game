import random
from unittest.mock import MagicMock
import pytest

from app.services.datamanager import DataManager


@pytest.fixture
def mock_users():
    """Provide a sample list of user data mirroring MongoDB structure."""
    return [
        {"name": "Alice", "domains": ["alice.com", "alice.net"]},
        {"name": "Bob", "domains": ["bob.org"]},
        {"name": "Charlie", "domains": ["charlie.co", "charlie.io"]},
        {"name": "Diana", "domains": ["diana.dev"]},
    ]

@pytest.fixture
def data_manager():
    """Initializes the dataManager instance for testing."""
    return DataManager()

def test_get_question_by_name(monkeypatch, data_manager, mock_users):
    """Test getting a question when the subject is 'name'."""
    # Mock DB and random utilities
    mock_user_model = MagicMock()
    mock_user_model.objects.aggregate.return_value = mock_users
    monkeypatch.setattr("app.services.datamanager.User", mock_user_model)

    # Mock random.choice safely for both list sequences and list of tuples
    def mock_choice(seq):
        if len(seq) > 1 and isinstance(seq[0], tuple):
            return seq[1]
        return seq[0]

    # Force choice to always pick the first domain in the list
    monkeypatch.setattr(random, "choice", mock_choice)

    result = data_manager.getQuestion(subject="name")

    expected_choices = ["alice.com", "bob.org", "charlie.co", "diana.dev"]
    assert result["subject"] == "Bob"
    assert result["choices"] == expected_choices
    assert result["index"] == 1
    assert result["question"] == "Select the correct domain owned by Bob"

def test_get_question_by_domain(monkeypatch, data_manager, mock_users):
    """Test getting a question when the subject is 'domain'."""
    # Mock DB and random utilities
    mock_user_model = MagicMock()
    mock_user_model.objects.aggregate.return_value = mock_users
    monkeypatch.setattr("app.services.datamanager.User", mock_user_model)

    # Mock random.choice safely for both list sequences and list of tuples
    def mock_choice(seq):
        if len(seq) > 1 and isinstance(seq[0], tuple):
            return seq[2]
        return seq[0]

    monkeypatch.setattr(random, "choice", mock_choice)

    result = data_manager.getQuestion(subject="domain")

    expected_choices = ["Alice", "Bob", "Charlie", "Diana"]
    assert result["subject"] == "charlie.co"
    assert result["choices"] == expected_choices
    assert result["index"] == 2
    assert result["question"] == "Select who owns the domain charlie.co"

def test_pipeline_structure(monkeypatch, data_manager, mock_users):
    """Verify the new MongoDB aggregation pipeline filters and samples correctly."""
    mock_user_model = MagicMock()
    mock_user_model.objects.aggregate.return_value = mock_users
    monkeypatch.setattr("app.services.datamanager.User", mock_user_model)

    monkeypatch.setattr(random, "choice", lambda seq: seq[0] if seq else None)

    # Adjust parameter to default valid view state ("name") to avoid KeyError
    data_manager.getQuestion(subject="name")

    stage1 = {"$match": {"domains": {"$exists": True, "$ne": []}}}
    stage2 = {"$sample": {"size": 4}}

    # Verify the pipeline argument structure
    mock_user_model.objects.aggregate.assert_called_once_with(stage1, stage2)