import os
import tempfile
import pytest

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    client = app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_home_page(client):
    """Test that the home page loads correctly."""
    print("Testing home page loading...")
    response = client.get('/')
    assert response.status_code == 200
    assert b'Gadget Generator Chat' in response.data
    print("Home page test passed!")


def test_reset(client):
    """Test the reset functionality."""
    print("Testing reset functionality...")
    with client.session_transaction() as sess:
        sess['conversation'] = ['some content']
    response = client.post('/', data={'reset': True}, follow_redirects=True)
    assert response.status_code == 200
    print("Reset functionality test passed!")


def test_approval_flow(client):
    """Test the approval flow."""
    print("Testing approval flow...")
    with client.session_transaction() as session:
        session['code'] = 'some code'
        session['components'] = ['component1', 'component2']
    response = client.post('/approve', data={'submit': 'true'}, follow_redirects=True)
    assert response.status_code == 200
    print("Approval flow test passed!")
