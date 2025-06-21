import pytest
from datetime import datetime
from app import app
from models import db, Message

@pytest.fixture
def db_setup():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()

class TestMessage:
    '''Message model in models.py'''

    def test_has_correct_columns(self, db_setup):
        '''has columns for message body, username, and creation time.'''
        with app.app_context():
            message = Message(
                body="Test message",
                username="Tester")
            
            db.session.add(message)
            db.session.commit()

            assert message.body == "Test message"
            assert message.username == "Tester"
            assert isinstance(message.created_at, datetime)

    def test_message_serialization(self, db_setup):
        '''can be serialized to JSON format.'''
        with app.app_context():
            message = Message(
                body="Serialization test",
                username="Serializer")
            
            db.session.add(message)
            db.session.commit()

            serialized = message.to_dict()
            assert serialized['body'] == "Serialization test"
            assert serialized['username'] == "Serializer"
            assert 'created_at' in serialized