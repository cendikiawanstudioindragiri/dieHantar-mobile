# tests/test_blueprints_get.py

import pytest


@pytest.fixture
def client():
    """Create and configure a test client for the Flask app."""
    from main import create_app
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# Tests for broadcasts blueprint
def test_get_broadcasts(client):
    """Test GET /api/v1/broadcasts endpoint."""
    response = client.get('/api/v1/broadcasts/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'data' in data


# Tests for configs blueprint
def test_get_splash_config(client):
    """Test GET /api/v1/configs/splash endpoint."""
    response = client.get('/api/v1/configs/splash')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'data' in data


def test_get_popup_config(client):
    """Test GET /api/v1/configs/popup endpoint."""
    response = client.get('/api/v1/configs/popup')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'data' in data


def test_get_welcome_config(client):
    """Test GET /api/v1/configs/welcome endpoint."""
    response = client.get('/api/v1/configs/welcome')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'data' in data


def test_get_ads_config(client):
    """Test GET /api/v1/configs/ads endpoint."""
    response = client.get('/api/v1/configs/ads')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'data' in data


def test_get_map_config(client):
    """Test GET /api/v1/configs/map endpoint."""
    response = client.get('/api/v1/configs/map')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'data' in data


def test_get_brand_config(client):
    """Test GET /api/v1/configs/brand endpoint."""
    response = client.get('/api/v1/configs/brand')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'data' in data


# Tests for partners blueprint
def test_get_partners(client):
    """Test GET /api/v1/partners/ endpoint."""
    response = client.get('/api/v1/partners/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'data' in data


def test_get_partner_by_id(client):
    """Test GET /api/v1/partners/<id> endpoint."""
    response = client.get('/api/v1/partners/test-partner-id')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'data' in data
    assert data['data']['id'] == 'test-partner-id'


# Note: Wallet endpoints require authentication, so they need a valid token
# These tests will verify the endpoint exists but may return 401 without token
def test_get_wallet_balance_requires_auth(client):
    """Test GET /api/v1/wallet/balance endpoint requires authentication."""
    response = client.get('/api/v1/wallet/balance')
    # Should return 401 (Unauthorized) without token
    assert response.status_code in [401, 403]


def test_get_wallet_transactions_requires_auth(client):
    """Test GET /api/v1/wallet/transactions endpoint requires authentication."""
    response = client.get('/api/v1/wallet/transactions')
    # Should return 401 (Unauthorized) without token
    assert response.status_code in [401, 403]
