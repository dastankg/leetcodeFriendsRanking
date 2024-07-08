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


url = "https://leetcode.com/graphql"
query = """
           {
               userContestRanking(username:  "%s")  {
                    rating
                }
           }
           """ % username

response = requests.post(url, json={'query': query})
print(response.json())