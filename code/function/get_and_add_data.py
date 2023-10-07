import requests
import sqlite3
from bs4 import BeautifulSoup

con = sqlite3.connect("requested_data.sqlite", check_same_thread=False)
cur = con.cursor()

def CreateNewTable():
	cur.execute("CREATE TABLE IF NOT EXISTS saved_profile(username, profile_img, last_year_contrib, total_stars, used_language_count_dict)")

def QueryFromSQLite(username):
	return cur.execute(f"SELECT * FROM saved_profile WHERE login='{username}'").fetchone()

def GetSQLiteData(username):
	context = {}
	query = QueryFromSQLite(username)
	context['username'], context['profile_img'], context['last_year_contrib'], context['total_stars'], context['used_language_count_dict'] = query

	return context

def InsertApiData(username):

	url = "https://github.com"
	response = requests.get(f'{url}/{username}')
	
	if response.status_code != 200:
		return {'username': username, 'message': response.status_code}

	else:
		soup = BeautifulSoup(response.content, "html.parser")

		profile_img = soup.find("img", class_="avatar-user")["src"]
		last_year_contrib = soup.find("div", class_="js-yearly-contributions").find("h2").text.split("\n")[1].strip()

		repo_url_response = requests.get(f'{url}/{username}/?tab=repositories&sort=stargazers')
		
		if repo_url_response.status_code != 200:
			return {'username': username, 'message': response.status_code}
		
		else:
			repo_soup = BeautifulSoup(repo_url_response.content, "html.parser")
			repo_elem_list = repo_soup.find(id="user-repositories-list").find_all("li")

			used_language_count_dict = {}
			test = []
			total_stars = 0
			total_amounts = 0

			i = 0
			for repo_elem in repo_elem_list:

				# Top 10 repo by stargazer
				if i>=10:
					break

				else:
					repo = repo_elem.find("a")["href"]
					repo_url_response = requests.get(f'{url}/{repo}')
					if repo_url_response.status_code != 200:
						return {'username': username, 'message': response.status_code}

					else:
						repo_soup = BeautifulSoup(repo_url_response.content, "html.parser")
						total_stars += int(repo_soup.find(id="repo-stars-counter-star").text)
						for used_language_elem in repo_soup.find_all("a", class_="d-inline-flex"):
							language, amount = used_language_elem.find_all("span")
							try:
								used_language_count_dict[language.text] += float(amount.text[0:-1])
								total_amounts += float(amount.text[0:-1])
							except:
								used_language_count_dict[language.text] = float(amount.text[0:-1])
								total_amounts += float(amount.text[0:-1])

				i+=1

			for language in used_language_count_dict:
				used_language_count_dict[language] = str(round(used_language_count_dict[language]/total_amounts*100, 2))

		try:
			cur.execute("""
				INSERT INTO saved_profile(username, profile_img, last_year_contrib, total_stars, used_language_count_dict) 
				VALUES (?, ?, ?, ?, ?);
				""", 
				(
					username, 
					profile_img, 
					last_year_contrib, 
					total_stars,
					used_language_count_dict
					)
				)
		except:
			cur.execute("""
				INSERT INTO saved_profile(username, profile_img, last_year_contrib, total_stars, used_language_count_dict) 
				VALUES (?, ?, ?, ?, ?);
				""", 
				(
					username, 
					'', 
					'', 
					'',
					''
					)
				)

		con.commit()