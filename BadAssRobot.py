import SubscriptionPage
import threading
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import random

class Liker(threading.Thread):

	def __init__(self,username,password,tags,comments,active):
		threading.Thread.__init__(self)
		self.username = username
		self.password = password
		self.tags = tags
		self.comments = comments
		self.active = active

	def run(self):
		liker(self.username, self.password, self.tags, self.comments, self.active)


def liker(username, password, tags, comments, active):
	print "Starting Firefox for "+username
	driver = webdriver.Firefox()
	#driver = webdriver.PhantomJS("/Users/JohnLecomte/Documents/python/instagram/phantomjs")
	print "Firefox opened for "+ username
	driver.get("https://www.instagram.com/accounts/login/")
	user_box = WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.NAME, "username")))
	user_box.send_keys(username)
	pass_box = driver.find_element_by_name("password")
	pass_box.send_keys(password)
	pass_box.send_keys(Keys.RETURN)
	wait_for_sign_in = WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.CLASS_NAME, "coreSpriteDesktopNavLogoAndWordmark")))

	following_list = []

	while True:
		main_urls = []
		if len(following_list) > 15:
			for url in following_list:
				driver.get(url)
				time.sleep(3)
				try:
					unfollow = driver.find_element_by_tag_name("button").click()
					following_list.remove(url)
					time.sleep(60)
				except:
					pass
		for item in tags:
			driver.get("https://www.instagram.com/explore/tags/"+item+"/")
			element = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.TAG_NAME,'a')))
			for links in driver.find_elements_by_tag_name("a"):
				if "/explore/tags/"+item+"/?max_id" in links.get_attribute("href"):
					links.click()
			time.sleep(10)
			count = 0
			lastHeight = driver.execute_script("return document.body.scrollHeight")
			while True:
					driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
					time.sleep(1)
					newHeight = driver.execute_script("return document.body.scrollHeight")
					if newHeight == lastHeight or count == 4:
						break
					lastHeight = newHeight
					count += 1	
			time.sleep(2)
			
			photo_urls = []
			for tagName in driver.find_elements_by_tag_name("a"):
				if "/p/" in tagName.get_attribute("href"):
					photo_urls.append(tagName.get_attribute("href"))
			photo_urls = set(photo_urls)
			main_urls.extend(photo_urls)
			time.sleep(3)
			print username + " is done loading urls for : "+ item
		
		print username +" is liking ", len(main_urls), " photos with tags: ", tags
		liker_Options = ["liker","liker/commenter","liker/commenter/follower"]
		if active == "follower":
			for url in main_urls:
				driver.get(url)
				try:
					follow = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.TAG_NAME,'button'))).click()
					following_list.append(url)
					time.sleep(45)
				except TimeoutException:
					pass
		elif active in liker_Options:
			count = 0
			for url in main_urls:
				driver.get(url)
				try:
					count += 1
					element = WebDriverWait(driver,2).until( EC.presence_of_element_located((By.CLASS_NAME, 'coreSpriteHeartOpen'))).click()
					if count >= 3 and (active == "liker/commenter" or active =="liker/commenter/follower"):
						for links in driver.find_elements_by_tag_name("input"):
							if "Add a comment" in links.get_attribute("placeholder"):
								randomComment = random.choice(comments)
								links.send_keys(randomComment)
								links.send_keys(Keys.RETURN)
								count = 0
					if count == 2 and active == "liker/commenter/follower":
						follow = driver.find_element_by_tag_name("button").click()
						following_list.append(url)
					time.sleep(15)
				except TimeoutException:
					pass
		else:
			for thread in threads:
				if thread[0] == username:
					threads.remove(thread)
				for username in usernameDatabase:
					usernameDatabase.remove(username)
			break
		
		new_file = open('/Users/JohnLecomte/Documents/python/instagram/users.txt')

		for new_line in new_file:
			new_row = new_line.strip().split(":")
			new_username = new_row[0]
			new_password = new_row[1]
			new_tags = new_row[2].split(",")
			new_comments = new_row[3].split(",")
			new_active = new_row[4]
			if new_username == username:
				tags = new_tags
				comments = new_comments
				active = new_active
				if password != new_password:
					password = new_password
					driver.get("https://www.instagram.com/accounts/login/")
					user_box = WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.NAME, "username")))
					user_box.send_keys(username)
					pass_box = driver.find_element_by_name("password")
					pass_box.send_keys(password)
					pass_box.send_keys(Keys.RETURN)
					wait_for_sign_in = WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.CLASS_NAME, "coreSpriteDesktopNavLogoAndWordmark")))
