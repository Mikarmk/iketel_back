import sqlalchemy as sa
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from data import config

#переписал для sqlite


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    nickname = Column(String, default='noname')

    def __repr__(self):
        return f"<User(id={self.id}, nickname='{self.nickname}')>"

engine = sa.create_engine(config.SQLITE_URI)
Session = sessionmaker(bind=engine)

def main():
    Base.metadata.create_all(engine)

    session = Session()

    user = User(nickname='John')
    session.add(user)
    session.commit()

    print(user)

    session.close()

if __name__ == '__main__':
    main()