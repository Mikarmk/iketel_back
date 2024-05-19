from utils.db_api.db_gino import TimedBaseModel
from gino import Gino
from typing import List
import datetime
from data import config
from loguru import logger
from sqlalchemy import Column, Integer, String, Text, ForeignKey, BigInteger

db = Gino()

class User(TimedBaseModel):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(40), unique=True)
    _email = Column(String(40), unique=True)
    teacher_password = Column(String(100), nullable=False)

class Story(TimedBaseModel):
    __tablename__ = 'stories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    story_code = Column(String(8), unique=True)
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete='CASCADE'))
    story_name = Column(String(30))
    story_desc = Column(Text)

class StoryList(TimedBaseModel):
    __tablename__ = 'story_list'
    id = Column(Integer, primary_key=True, autoincrement=True)
    story_id = Column(Integer, ForeignKey('stories.id', ondelete='CASCADE'))
    story_index = Column(Integer, nullable=False)
    quest_text = Column(Text)

class Character(TimedBaseModel):
    __tablename__ = 'characters'
    name = Column(String(100))
    id = Column(Integer, primary_key=True, autoincrement=True)
    story_id = Column(Integer, ForeignKey('stories.id', ondelete='CASCADE'))
    character_desc = Column(Text)
    image_path = Column(String(100))

class Quest(TimedBaseModel):
    __tablename__ = 'quests'
    id = Column(Integer, primary_key=True, autoincrement=True)
    story_id = Column(Integer, ForeignKey('stories.id', ondelete='CASCADE'))
    quest_name = Column(String(30), nullable=False)
    quest_theme = Column(String(30), nullable=False)
    quest_index = Column(Integer, nullable=False)
    character_id = Column(Integer, ForeignKey('characters.id'))
    quest_text = Column(Text)
    character_text = Column(Text)

class Task(TimedBaseModel):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    quests_id = Column(Integer, ForeignKey('quests.id', ondelete='CASCADE'))
    content = Column(Text, nullable=False)
    answer = Column(String(200))
    task_index = Column(Integer, nullable=False)
    task_type = Column(String(20), nullable=False)

class UsersTask(TimedBaseModel):
    __tablename__ = 'users_tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(30))
    story_id = Column(Integer, ForeignKey('stories.id', ondelete='CASCADE'))
    correct_tasks = Column(Integer, nullable=False)
    not_correct_tasks = Column(Integer, nullable=False)