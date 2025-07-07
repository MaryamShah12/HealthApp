from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

mysql_url='mysql+mysqlconnector://root:@localhost/healthapp'

engine=create_engine(mysql_url)

Base=declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    # Relationships
    meals = relationship("Meal", back_populates="user")
    moods = relationship("Mood", back_populates="user")
    sleeps = relationship("Sleep", back_populates="user")
    waters = relationship("Water", back_populates="user")
    exercises = relationship("Exercise", back_populates="user")


class Meal(Base):
    __tablename__ = 'meals'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    food_name = Column(String(100), nullable=False)
    calories = Column(Integer, nullable=False)
    carbs = Column(DECIMAL(5, 2))
    protein = Column(DECIMAL(5, 2))
    fat = Column(DECIMAL(5, 2))
    timestamp = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="meals")


class Mood(Base):
    __tablename__ = 'mood'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    rating = Column(String(50))
    date = Column(DateTime)
    note = Column(Text)

    user = relationship("User", back_populates="moods")


class Sleep(Base):
    __tablename__ = 'sleep'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    hours = Column(DECIMAL(4, 2))
    date = Column(DateTime)
    quality_rating = Column(String(50), nullable=False)

    user = relationship("User", back_populates="sleeps")


class Water(Base):
    __tablename__ = 'water'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount_ml = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="waters")


class Exercise(Base):
    __tablename__ = 'exercise'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    activity = Column(String(100), nullable=False)
    duration_mins = Column(Integer, nullable=False)
    calories_b = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="exercises")