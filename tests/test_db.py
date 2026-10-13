import pytest
import mongomock
import mongoengine as me
from mongoengine import ValidationError
from app.models.user import User

# Setup an in-memory test database fixture
