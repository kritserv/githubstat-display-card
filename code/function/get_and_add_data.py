import requests
import sqlite3

con = sqlite3.connect("requested_data.sqlite", check_same_thread=False)
cur = con.cursor()

def CreateNewTable():
	cur.execute("CREATE TABLE IF NOT EXISTS saved_profile(login, avatar_url, url, hireable, total_stars, total_commits, total_prs)")

def QueryFromSQLite(username):
	return cur.execute(f"SELECT * FROM saved_profile WHERE login='{username}'").fetchone()

def GetSQLiteData(username):
	context = {}
	query = QueryFromSQLite(username)
	context['username'], context['avatar_url'], context['url'], context['hireable'], context['total_stars'], context['total_commits'], context['total_prs'] = query

	return context

def InsertApiData(username, flaskusr, token):
	new_data = requests.get(f'https://api.github.com/users/{username}').json()
	if token:
		requests.Session().auth = (flaskusr, token)

	total_stars = 0
	total_commits = 0
	total_prs = 0

	repos = requests.get(f"{new_data['url']}/repos").json()
	for repo in repos:

		if not repo['fork']:
			total_stars += repo['stargazers_count']

			commits = requests.get(f"{new_data['url']}/{repo['name']}/commits").json()
			total_commits += len(commits)

		pulls = requests.get(f"{new_data['url']}/{repo['name']}/pulls").json()
		total_prs += len(pulls)

	try:
		cur.execute("""
			INSERT INTO saved_profile(login, avatar_url, url, hireable, total_stars, total_commits, total_prs) 
			VALUES (?, ?, ?, ?, ?, ?, ?);
			""", 
			(
				new_data['login'], 
				new_data['avatar_url'], 
				new_data['url'], 
				new_data['hireable'],
				total_stars,
				total_commits,
				total_prs
				)
			)
	except:
		cur.execute("""
			INSERT INTO saved_profile(login, avatar_url, url, hireable, total_stars, total_commits, total_prs) 
			VALUES (?, ?, ?, ?, ?, ?, ?);
			""", 
			(
				username, 
				'', 
				'', 
				'',
				'',
				'',
				''
				)
			)

	con.commit()