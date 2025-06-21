import pytest
from datetime import datetime
from app import app
from models import db, Message

@pytest.fixture
def client():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with app.app_context():
        db.create_all()
        # Add initial test data
        test_msg = Message(body="Original message", username="Tester")
        db.session.add(test_msg)
        db.session.commit()
    
    yield app.test_client()
    
    with app.app_context():
        db.drop_all()

class TestApp:
    '''Flask application in app.py'''

    def test_returns_list_of_json_objects(self, client):
        '''returns a list of JSON objects for all messages in the database.'''
        response = client.get('/messages')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        data = response.json
        assert isinstance(data, list)
        assert any(msg['body'] == "Original message" for msg in data)

    def test_creates_new_message(self, client):
        '''creates a new message in the database.'''
        response = client.post(
            '/messages',
            json={"body": "New message", "username": "Creator"}
        )
        assert response.status_code == 201
        assert response.json['body'] == "New message"

    def test_updates_message(self, client):
        '''updates the body of a message in the database.'''
        with app.app_context():
            message = Message.query.first()
            response = client.patch(
                f'/messages/{message.id}',
                json={"body": "Updated message"}
            )
            assert response.status_code == 200
            assert response.json['body'] == "Updated message"

    def test_deletes_message(self, client):
        '''deletes the message from the database.'''
        with app.app_context():
            message = Message.query.first()
            response = client.delete(f'/messages/{message.id}')
            assert response.status_code == 200
            assert Message.query.get(message.id) is None