import os
import pytest
from dotenv import load_dotenv


def pytest_configure():
    # Load the .env file for all tests
    env_path = os.path.join(os.path.dirname(__file__),
                            '..', 'src', 'config', 'credentials.env')
    load_dotenv(env_path)


@pytest.fixture
def data_folder():
    # Assuming the data folder is located in the same directory as conftest.py
    return os.path.join(os.path.dirname(__file__), '..', '.data')
