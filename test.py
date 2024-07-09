import requests

username = "pratovv"
# url = "https://leetcode.com/graphql"
# query = """
#    {
#      matchedUser(username: "%s") {
#        submitStats: submitStatsGlobal {
#          acSubmissionNum {
#            difficulty
#            count
#            submissions
#          }
#        }
#      }
#    }
#    """ % username
# response = requests.post(url, json={'query': query})
#
# if response.status_code == 200:
#     data = response.json()
#     print(data)
# else:
#     print(f"Error: {response.status_code}")

#
# url = "https://leetcode.com/graphql"
# query = """
#            {
#                userContestRanking(username:  "%s")  {
#                     rating
#                 }
#            }
#            """ % username
#
# response = requests.post(url, json={'query': query})
# print(response.json())


from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from config.config_file import load_config, Config

config: Config = load_config()
conn_string = (f"postgresql://{config.db.db_username}:{config.db.db_password}@{config.db.db_host}/{config.db.database}")
engine = create_engine(conn_string)
Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    login = Column(String)


Session = sessionmaker(bind=engine)
session = Session()

users = session.query(Users).all()
for user in users:
    print(user.user_id, user.login)
