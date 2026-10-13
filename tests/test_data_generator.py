import pytest
from unittest.mock import MagicMock, patch
from faker import Faker

from app.services.datagenerator import DataGenerator
from app.models.user import User

@pytest.fixture
def app_context(app):
    """Push an application context for the duration of the test."""
    with app.app_context():
        yield

@pytest.fixture
def generator():
    """Provide a clean instance of DataGenerator for each test."""
    return DataGenerator()

@pytest.fixture
def mock_fake():
    """Mock Faker to return predictable names and domains."""
    fake = MagicMock()
    fake.name.side_effect = [f"User {i}" for i in range(20)]
    fake.domain.side_effect = [f"domain{i}.com" for i in range(100)]
    return fake

@pytest.fixture
def sample_payload():
    """Provide a structured dictionary representing parsed generator output."""
    return {
        "Alice": ["alice.com", "corporate.com", "alice-personal.org"],
         "Bob": ["bob.net"]
    }

class TestDataGenerator:
    @patch('app.services.datagenerator.random.randint', return_value=2)
    @patch('app.services.datagenerator.Faker')
    def test_generate_data_internal_success(self, mock_faker_class, mock_randint, generator, mock_fake):
        """Test internal generation returns exactly 10 inique elements with status success."""
        mock_faker_class.return_value = mock_fake

        result = generator.generate_data(source="internal", toDb=False)
        assert result["status"] == "Success"
        assert result["target"] == "page"
        assert len(result["data"]) == 10

        # Verify structure: keys are names, values are a list of domains.
        for name, domains in result["data"].items():
            assert name.startswith("User")
            assert len(domains) == 2  # Fixed to 2 by mock_randint
            assert domains[0].endswith(".com")

    @patch('app.services.datagenerator.get_google_service_client')
    def test_generate_data_external_spreadsheet(self, mock_get_client, app_context, generator):
        """Test spreadsheet loading parses names, splits domains and merges duplicate rows."""
        # Setup mock data returned from Google Spreadsheet
        mock_sheet = MagicMock()
        # Mock rows: [Name, Domains separated by comma]
        mock_sheet.sheet1.get_all_values.return_value = [
            ["Alice", "alice.com, corporate.com"],
            ["", "alice-personal.org"], # Empty name uses previous name
            ["Bob", "bob.net"],
            ["Alice", "new-domain.com"] # Duplicate name should append
        ]

        mock_client = MagicMock()
        mock_client.open_by_key.return_value = mock_sheet
        mock_get_client.return_value = mock_client

        result = generator.generate_data(source="external", toDb=False)

        mock_client.open_by_key.assert_called_with("dummy_sheet_id_123")

        expected_data = {
            "Alice": ["alice.com", "corporate.com", "alice-personal.org", "new-domain.com"],
            "Bob": ["bob.net"]
        }
        assert result["data"] == expected_data

    @patch('app.services.datagenerator.User')
    def test_load_database_saves_all_documents(self, mock_user_cls, generator, sample_payload):
        """Test that __load_database creates User instances and saves each to MongoDB."""

        # Setup mock instances returned by the User constructor
        mock_user_alice = MagicMock(spec=User)
        mock_user_bob = MagicMock(spec=User)
        mock_user_cls.side_effect = [mock_user_alice, mock_user_bob]

        # Execute the private name-mangled method
        generator._DataGenerator__load_database(sample_payload)

        # 3. Assertions: Verify constructors were called with correct fields
        assert mock_user_cls.call_count == 2
        mock_user_cls.assert_any_call(name="Alice", domains=sample_payload["Alice"])
        mock_user_cls.assert_any_call(name="Bob", domains=sample_payload["Bob"])

        # 4. Assertions: Verify .save() was executed on each document instance
        mock_user_alice.save.assert_called_once()
        mock_user_bob.save.assert_called_once()

    @patch('app.services.datagenerator.User')
    def test_load_database_with_empty_payload(self, mock_user_cls, generator):
        """Test that an empty dictionary payload gracefully returns without actions."""

        generator._DataGenerator__load_database({})

        mock_user_cls.assert_not_called()

    def test_generate_data_to_db_flow(self, generator):
        """Test that setting toDb calls internal database preparation and load methods."""
        dummy_data = {"Jane Doe": ["jane-doe.com"]}

        # Patch the mangled private methods directly on DataGenerator
        with patch.object(DataGenerator, '_DataGenerator__clear_database') as mock_clear, \
             patch.object(DataGenerator, '_DataGenerator__load_database', return_value="DB Load Success") as mock_load, \
             patch.object(DataGenerator, '_DataGenerator__load_spreadsheet_data', return_value=dummy_data):

            result = generator.generate_data(source="external", toDb=True)

            mock_clear.assert_called_once()
            mock_load.assert_called_once_with(dummy_data)
            assert result == "DB Load Success"

