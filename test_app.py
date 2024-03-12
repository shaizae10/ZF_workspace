import os
import tempfile
import pytest

from app import app
print('test')
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
    print(f"Response status code: {response.status_code}")
    assert response.status_code == 200
    assert b'main.html' in response.data  # Check for specific content if necessary
    print("Home page loaded successfully.")

def test_reset(client):
    """Test the reset functionality."""
    print("Testing reset functionality...")
    response = client.post('/reset', follow_redirects=True)
    print(f"Response status code: {response.status_code}")
    assert response.status_code == 200
    # Add more assertions based on the expected outcome of the reset
    print("Reset functionality works as expected.")

def test_approval_flow(client):
    """Test the approval flow."""
    print("Testing approval flow...")
    # Setup the session or mock data as required for the test
    with client.session_transaction() as session:
        session['code'] = 'some code'
        session['components'] = ['component1', 'component2']
    
    response = client.post('/approve', data={'submit': True}, follow_redirects=True)
    print(f"Response status code: {response.status_code}")
    assert response.status_code == 200
    # Assert that the files are created or other outcomes as expected
    print("Approval flow executed successfully.")
