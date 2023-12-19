from faker import Faker
from sqlalchemy.orm import Session
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from database.connection import get_db
from tables import Tasks, Users, MediaTypes, Medias, Chats, Messages

   

fake = Faker()

def seed_users(session: Session, num_users=5):
    users = []
    for _ in range(num_users):
        user = Users(
            username=fake.user_name(),
            email=fake.email(),
            hashed_password=fake.uuid4(),
        )
        users.append(user)
    session.add_all(users)
    session.commit()
 
  
def seed_media_types(session: Session):
    image_type = MediaTypes(name="Image")
    video_type = MediaTypes(name="Video")
    session.add_all([image_type, video_type])
    session.commit()


def seed_tasks(session: Session):
    tasks = []
    for task in ["Translation", "Summarization", "Chat"]:
        tasks.append(Tasks(name=task))
    session.add_all(tasks)
    session.commit()

def seed_medias(session: Session, num_medias=10):
    medias = []
    for _ in range(num_medias):
        media = Medias(
            user_id=fake.random_element(session.query(Users.id).all())[0],
            media_type_id=fake.random_element(session.query(MediaTypes.id).all())[0],
            title=fake.text(max_nb_chars=20),
        )
        medias.append(media)
    session.add_all(medias)
    session.commit()

def seed_chats(session: Session, num_chats=15):
    chats = []
    for _ in range(num_chats):
        chat = Chats(
            task_id=fake.random_element(session.query(Tasks.id).all())[0],
            media_id=fake.random_element(session.query(Medias.id).all())[0])
        chats.append(chat)
    session.add_all(chats)
    session.commit()

def seed_chat_messages(session: Session, num_messages=30):
    messages = []
    for _ in range(num_messages):
        message = Messages(
            chat_id=fake.random_element(session.query(Chats.id).all())[0],
            human_question=fake.sentence(),
            bot_answer=fake.sentence(),
        )
        messages.append(message)
    session.add_all(messages)
    session.commit()

def seed_data():
    # Create database tables

    # Get the database session using get_db
    db = next(get_db())

    try:
        seed_users(db)
        seed_media_types(db)
        seed_tasks(db)
        seed_medias(db)
        seed_chats(db)
        seed_chat_messages(db)

    finally:
        db.close()

if __name__ == "__main__":
   seed_data()
