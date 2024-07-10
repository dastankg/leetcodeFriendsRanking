from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from config.config_file import load_config, Config

# Load configuration settings
config: Config = load_config()

# Create a connection string for the PostgreSQL database
conn_string = f"postgresql://{config.db.db_username}:{config.db.db_password}@{config.db.db_host}/{config.db.database}"

# Create a SQLAlchemy engine
engine = create_engine(conn_string)

# Create a base class for declarative class definitions
Base = declarative_base()


class Users(Base):
    """
    Represents the Users table in the database.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    login = Column(String(255))


class Friends(Base):
    """
    Represents the Friends table in the database.
    """
    __tablename__ = 'friends'
    friends_id = Column(Integer, primary_key=True)
    user_name = Column(String(255))
    id = Column(Integer, ForeignKey('users.user_id'))


# Create a configured "Session" class
Session = sessionmaker(bind=engine)
