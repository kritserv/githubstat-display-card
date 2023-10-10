import requests
import sqlite3
from bs4 import BeautifulSoup

con = sqlite3.connect("requested_data.sqlite", check_same_thread=False)
cur = con.cursor()

def CreateNewTable():
	cur.execute("CREATE TABLE IF NOT EXISTS saved_profile(usr, image, contrib, all_stars, all_lang)")

def QueryFromSQLite(username):
	return cur.execute(f"SELECT * FROM saved_profile WHERE usr='{username}'").fetchone()

def GetSQLiteData(username):
	context = {}
	query = QueryFromSQLite(username)
	context['username'], context['image'], context['contrib'], context['all_stars'], context['all_lang'] = query

	return context

def ScrapDataFromGithub(username):

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
						repo_star = repo_soup.find(id="repo-stars-counter-star").text
						if 'k' in repo_star:
							repo_star = repo_star[0:-1]
							repo_star = float(repo_star)*1000
						else:
							repo_star = float(repo_star)
						total_stars += repo_star
						for used_language_elem in repo_soup.find_all("a", class_="d-inline-flex"):
							language, amount = used_language_elem.find_all("span")
							try:
								used_language_count_dict[language.text] += float(amount.text[0:-1])
								total_amounts += float(amount.text[0:-1])
							except:
								used_language_count_dict[language.text] = float(amount.text[0:-1])
								total_amounts += float(amount.text[0:-1])

				i+=1

			if total_stars > 999:
				total_stars = str(round(total_stars/1000, 2)) + 'k'
			for language in used_language_count_dict:
				used_language_count_dict[language] = str(round(used_language_count_dict[language]/total_amounts*100, 2))

			return (username, profile_img, last_year_contrib, total_stars, str(used_language_count_dict))

def AddNewDataToSQLite(username, newdata):
	try:
		cur.execute("INSERT INTO saved_profile VALUES (?, ?, ?, ?, ?)", newdata)

	except:
		pass

	con.commit()