# tests/conftest.py

import pytest
from unittest.mock import MagicMock, patch
import sys

# Mock Firebase before any imports
@pytest.fixture(scope='session', autouse=True)
def mock_firebase_modules():
    """Mock Firebase modules before imports."""
    # Create mock modules
    mock_firebase_admin = MagicMock()
    mock_firebase_admin._apps = []
    mock_firebase_admin.initialize_app = MagicMock()
    
    # Mock submodules
    mock_firestore = MagicMock()
    mock_auth = MagicMock()
    mock_messaging = MagicMock()
    mock_credentials = MagicMock()
    
    # Set up the module structure
    sys.modules['firebase_admin'] = mock_firebase_admin
    sys.modules['firebase_admin.firestore'] = mock_firestore
    sys.modules['firebase_admin.auth'] = mock_auth
    sys.modules['firebase_admin.messaging'] = mock_messaging
    sys.modules['firebase_admin.credentials'] = mock_credentials
    
    # Mock the client returns
    mock_db = MagicMock()
    mock_firestore.client = MagicMock(return_value=mock_db)
    
    yield {
        'firebase_admin': mock_firebase_admin,
        'firestore': mock_firestore,
        'auth': mock_auth,
        'messaging': mock_messaging,
        'db': mock_db
    }
