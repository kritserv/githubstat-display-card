import sqlite3
from get_and_add_data import ScrapDataFromGithub
import time

def UpdateUserData(updated_data, cur, con):
	try:
		username, profile_img, last_year_contrib, total_stars, used_language_count_dict, date_ = updated_data
		cur.execute(
			"UPDATE saved_profile SET image = ?, contrib = ?, all_stars = ?, all_lang = ?, latest_update = ? WHERE usr = ?", 
			(profile_img, last_year_contrib, total_stars, used_language_count_dict, date_, username)
			)
		con.commit()
	except:
		print("UPDATE FAILED!")

def UpdateSQLiteDatabase():
	start_time = time.time()
	con = sqlite3.connect("app/backend/data/requested_data.sqlite", check_same_thread=False)
	cur = con.cursor()
	cur.execute("SELECT usr FROM saved_profile")
	usernames = [row[0] for row in cur.fetchall()]
	for username in usernames:
		github_data = ScrapDataFromGithub(username)
		UpdateUserData(github_data, cur, con)
		print(f"Data updated for {username}")
	end_time = time.time()
	print(f"Total time taken: {end_time-start_time:.2f} seconds")


if __name__ == '__main__':
	UpdateSQLiteDatabase()