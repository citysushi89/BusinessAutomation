import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.common.keys
import selenium.common.exceptions
from bs4 import BeautifulSoup as bs
import os
from dotenv import load_dotenv

# Program logs into instragram and cycles through hashtags liking pictures if haven't liked them yet


# BASIC Background Stuff
s = Service("C:/Users/Owen/Documents/Personal Info/Independent Courses/Python Learning/chromedriver")
driver = webdriver.Chrome(service=s)
# instagram_username = os.environ["INSTAGRAM_USERNAME"]
load_dotenv()
instagram_username = os.getenv("INSTAGRAM_USERNAME")
instagram_password = os.getenv("INSTAGRAM_PASSWORD")
# print(instagram_username)
INSTA_HOME_URL = "https://www.instagram.com/"
driver.get(INSTA_HOME_URL)
# Maybe change later to select from a list of concealed carry-related hashtags?
HASHTAG_LIST = ["concealedcarry", "concealcarry", "ccw", "edc", "everydaycarry", "secondamendment", "2ndamendment",
                "gun", "guns", "concealedcarrynation", "gunsofinstagram", "firearmsafety", "selfdefense", "iwb", "owb",
                "aiwb", "ccwfashion", "ccwstyle", "edcgear", "shallnot", "girlswhocarry", "guntraining", "basicccw",
                "2A", "gunrightsarewomensrights", "firearms", "Pro2A", "MadeInTheUSA", "responsiblyarmed",
                "concealedcarrylife", "edccommunity"]



# Variables to Change
# Randomly select hashtag from list to run
index_options = len(HASHTAG_LIST)
random_index_selection = random.randint(0, index_options - 1)

# HASHTAG_TO_SEARCH = HASHTAG_LIST[random_index_selection]

# Pick an item to run the report for
# HASHTAG_TO_SEARCH = HASHTAG_LIST[1]
# Below just selects the top posts, which avoids most of the weird posts
number_of_posts_to_click_through = 24



def sleep_random():
    time.sleep(random.randint(1, 5))


def sleep_small():
    standard_little_sleep_time = .5
    time.sleep(standard_little_sleep_time)


def sleep_medium():
    standard_little_sleep_time = 2
    time.sleep(standard_little_sleep_time)


def sleep_big():
    standard_little_sleep_time = 5
    time.sleep(standard_little_sleep_time)


def sleep_bigger():
    standard_bigger_sleep_time = 10
    time.sleep(standard_bigger_sleep_time)

def sleep_huge():
    standard_bigger_sleep_time = 20
    time.sleep(standard_bigger_sleep_time)


# Logging in
def login():
    sleep_random()
    username_box = driver.find_element(By.NAME, "username")
    username_box.send_keys(instagram_username)
    sleep_random()
    password_box = driver.find_element(By.NAME, "password")
    password_box.send_keys(instagram_password)
    sleep_random()
    password_box.send_keys(Keys.ENTER)

    sleep_random()


def disable_popup(xpath_of_button):
    sleep_big()
    not_now = driver.find_element(By.XPATH, xpath_of_button)
    sleep_small()
    not_now.click()


def search_hashtag():
    sleep_big()
    driver.get(hashtag_search_url)
    sleep_small()


def click_first_post():
    sleep_huge()
    try:
        first_post = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/article/div[1]/div/div/div[1]/div[1]")
        sleep_small()
        first_post.click()
    except selenium.common.exceptions.NoSuchElementException:
        sleep_bigger()
        sleep_bigger()
        first_post = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/article/div[1]/div/div/div[1]/div[1]/a")
        sleep_small()
        first_post.click()

    like_picture()

# Below also skips the picture if it is already liked
def like_picture():
    time.sleep(2)
    like = driver.find_element(By.CLASS_NAME, '_aamw')
    soup = bs(like.get_attribute('innerHTML'), 'html.parser')
    tag = soup.find(name="svg")
    like_status = tag.get("aria-label")
    # Below likes or skips the like button on pictures based on the aria-label
    if like_status == "Like":
        sleep_small()
        like.click()
    elif like_status == "Unlike":
        sleep_small()
        pass
    else:
        print("else triggered, something went wrong with like_status")
    sleep_medium()

def click_next_first_picture():
    sleep_medium()
    next_picture = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[1]/div/div/div")
    sleep_small()
    next_picture.click()
    sleep_medium()


def click_next_picture():
    sleep_medium()
    next_picture = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[1]/div/div/div[2]")
    sleep_small()
    next_picture.click()



def click_through_including_top_posts():
    counter = 0
    for i in range(1, number_of_posts_to_click_through):
        if i == 1:
            counter += 1
            click_next_first_picture()
            like_picture()
        else:
            click_next_picture()
            like_picture()
            counter += 1



def click_through_just_recent_posts():
    counter = 0
    for i in range(1, number_of_posts_to_click_through):
        click_next_picture()
        like_picture()
        counter += 1



login()
# For remembering password
try:
    disable_popup("/html/body/div[1]/div/div/section/main/div/div/div/div/button")
except selenium.common.exceptions.NoSuchElementException:
    pass
# For turning on notifications
try:
    disable_popup(
    "/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[3]/button[2]")
except selenium.common.exceptions.NoSuchElementException:
    pass



for hashtag in HASHTAG_LIST:
    hashtag_search_url = f"https://www.instagram.com/explore/tags/{hashtag}/"
    print(f"Searched for hashtag: {hashtag}")
    search_hashtag()
    click_first_post()
    try:
        click_through_including_top_posts()
    except:
        continue


