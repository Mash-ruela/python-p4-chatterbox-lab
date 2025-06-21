#!/usr/bin/env python3

from random import choice as rc
from faker import Faker
from app import app
from models import db, Message

fake = Faker()

with app.app_context():
    # Clear existing data
    db.drop_all()
    db.create_all()

    # Create usernames
    usernames = [fake.first_name() for _ in range(4)]
    if "Duane" not in usernames:
        usernames.append("Duane")

    # Create messages
    messages = []
    for _ in range(20):
        message = Message(
            body=fake.sentence(),
            username=rc(usernames),
        )
        messages.append(message)

    db.session.add_all(messages)
    db.session.commit()
    print("Database seeded successfully!")