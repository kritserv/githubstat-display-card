import requests
import sqlite3
from bs4 import BeautifulSoup
import os
import sys
code = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(code)
from function.get_and_add_data import ScrapDataFromGithub, AddNewDataToSQLite
import time

def UpdateUserData(updated_data, cur):
	username, profile_img, last_year_contrib, total_stars, used_language_count_dict = updated_data
	cur.execute(
		"UPDATE saved_profile SET image = ?, contrib = ?, all_stars = ?, all_lang = ? WHERE usr = ?", 
		(profile_img, last_year_contrib, total_stars, used_language_count_dict, username)
		)

def UpdateSQLiteDatabase():
	start_time = time.time()
	con = sqlite3.connect("requested_data.sqlite", check_same_thread=False)
	cur = con.cursor()
	cur.execute("SELECT usr FROM saved_profile")
	usernames = [row[0] for row in cur.fetchall()]
	for username in usernames:
		github_data = ScrapDataFromGithub(username)
		UpdateUserData(github_data, cur)
		print(f"Data updated for {username}")
	end_time = time.time()
	print(f"Total time taken: {end_time-start_time:.2f} seconds")


if __name__ == '__main__':
	UpdateSQLiteDatabase()