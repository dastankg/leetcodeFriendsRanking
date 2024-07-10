from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from config.config_file import load_config, Config

config: Config = load_config()
conn_string = f"postgresql://{config.db.db_username}:{config.db.db_password}@{config.db.db_host}/{config.db.database}"
engine = create_engine(conn_string)
Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    login = Column(String(255))


# Определение модели для таблицы friends
class Friends(Base):
    __tablename__ = 'friends'
    friends_id = Column(Integer, primary_key=True)
    user_name = Column(String(255))
    id = Column(Integer, ForeignKey('users.user_id'))


Session = sessionmaker(bind=engine)
session = Session()



