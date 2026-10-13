import pytest
import mongoengine as me
from mongoengine import ValidationError
from app.models.user import User


# Setup an in-memory test database fixture
@pytest.fixture(scope="function", autouse=True)
def test_db():
    """Connects to a mock MongoDB instance before each test and cleans up."""
    connection = me.connect('mongoenginetest', host='mongomock://localhost')
    yield connection
    # Clean up collections after each test run
    User.drop_collection()
    connection.close()

def test_create_valid_user():
    """Ensure a user with valid name and domains can be successfully saved."""
    user_data = {
        "name": "Jane Doe",
        "domain": ["example.com", "test.org"]
    }

    user = User(**user_data).save()

    # Assert
    assert user.id is not None
    assert user.name == "Jane Doe"
    assert "example.com" in user.domains
    assert User.objects.count() == 1

def test_create_user_missing_required_name():
    """Ensure saving a user without a name raises a ValidationError."""
    user = User(domains = ["example.com", "test.org"])

    with pytest.raises(ValidationError) as exc_info:
        user.save()

    # Assert
    assert "Field is required: ['name']" in str(exc_info.value)

def test_create_user_name_exceeds_max_length():
    """Ensure a name longer than 100 characters raises a ValidationError."""
    long_name = "a" * 101
    user = User(name=long_name, domains=["example.com"])

    with pytest.raises(ValidationError) as exc_info:
        user.save()

    # Assert
    assert "String value is too long" in str(exc_info.value)

def test_domain_list_field_meets_min_length():
    """Ensure field passes validation when the list length equals min_length."""
    user = User(name="Jane Doe", domains=["onlyone.com"])

    user.save()

    # Assert
    assert User.objects.count() == 1

def test_domain_list_field_violates_min_length():
    """Ensure an empty domain list raises the custom min_length ValidationError."""
    user = User(name="Jane Doe", domains=[])

    with pytest.raises(ValidationError) as exc_info:
        user.save()

    # Assert
    assert "List must contain at least 1 items." in str(exc_info.value)

def test_domain_list_field_invalid_element_type():
    """Ensure adding non-string items raises a validation error (since it expects me.StringField)."""
    user = User(name="Jane Doe", domains=[123, 456])

    with pytest.reises(ValidationError) as exc_info:
        user.save()

    # Assert
    assert "ValidationError" in str(exc_info.value)

