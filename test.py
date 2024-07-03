import requests

nick = 'SatoruGodjo1'
# Define the URL
url = f"https://leetcode-api-faisalshohag.vercel.app/{nick}"
s = 'https://leetcode.com/graphql?query=query { userContestRanking(username:' + '"' +nick+'"' + ') { attendedContestsCount rating globalRanking totalParticipants topPercentage } }'
# Send a GET request to the URL
response = requests.get(url)
response1 = requests.get(s)

# Get the JSON data from the response
data = response.json()
data1 = response1.json()

print('errors' in data)
print(data)
