import requests
from collections import Counter
from datetime import date

username = "kritserv"

session = requests.Session()
#session.headers.update({"Authorization": "kritserv {token}"})
response = session.get("https://api.github.com/users/"+username)
print(response)
profile_data = response.json()
followers_count = profile_data["followers"]

if followers_count > 999:
    followers_count = str(round(followers_count / 1000, 2)) + "k"
else:
    followers_count = str(followers_count)

response = session.get("https://api.github.com/users/"+username+"/repos")
print(response)


all_repo_data = response.json()

total_stars = 0
all_languages_urls = []

for repo_data in all_repo_data:
    all_languages_urls.append(repo_data["languages_url"])
    total_stars += repo_data["stargazers_count"]
    
if total_stars > 999:
    total_stars = str(round(total_stars / 1000, 2)) + "k"
else:
    total_stars = str(total_stars)
    
all_language_data = []
language_counter = Counter()

for language_url in all_languages_urls:
    response = session.get(language_url)
    print(response)
    all_language_data.append(response.json())
    
for language in all_language_data:
    language_counter.update(language)

language_counter = dict(language_counter)

total_language_amount = sum(language_counter.values())

language_percentage = {}
for key, val in language_counter.items():
    pct = val * 100.0 / total_language_amount
    pct = round(pct, 2)
    language_percentage[key] = pct

sorted_language_by_percentage = sorted(language_percentage.items(), key=lambda item: item[1])
print(sorted_language_by_percentage)

sorted_language_by_percentage = str(sorted_language_by_percentage)
print(sorted_language_by_percentage)

sorted_language_by_percentage = sorted_language_by_percentage.replace("[(","{")
print(sorted_language_by_percentage)
sorted_language_by_percentage = sorted_language_by_percentage.replace(")]","}")
print(sorted_language_by_percentage)
sorted_language_by_percentage = sorted_language_by_percentage.replace("',","': '")
print(sorted_language_by_percentage)
sorted_language_by_percentage = sorted_language_by_percentage.replace(")","'")
print(sorted_language_by_percentage)

print(username)
print(followers_count)
print(total_stars)
print(sorted_language_by_percentage)
print(str(date.today()))

output = open("output.txt", "w")
output_lines = [username+'\n', followers_count+'\n', total_stars+'\n', sorted_language_by_percentage+'\n', str(date.today())+'\n']
output.writelines(output_lines)
output.close()
