from selenium import webdriver
from selenium import common
from selenium.common.exceptions import *
from time import sleep
from sys import exit
import argparse

def init_webdriver():
    try:
        driver = webdriver.PhantomJS()
        driver.set_window_size(1920, 1080)
        print "[#] new WebDriver Initialized."
        return driver
    except WebDriverException:
        print "[!] Web Driver Exception. [initWebdriver]"
        exit(1)

def exit_gracefully(driver, custom_message, error_message=None):
    try:
        if error_message != None:
            print error_message
        print custom_message
        driver.quit()
    except Exception:
        pass
    exit(1)

def check_exists_by_css_selector(driver, css):
    try:
        driver.find_element_by_css_selector(css)
    except NoSuchElementException:
        return False
        print "[#] Could Not Find Results."
    return True

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("password", help="the password for InstaBotPy account which will be used for scraping.", default="")
    args = parser.parse_args()
    return args.password

def login(driver, username, password):
    try:
        usernameInputObj = driver.find_element_by_css_selector('input[name="username"]')
        usernameInputObj.send_keys(username)
        passwordInputObj = driver.find_element_by_css_selector('input[name="password"]')
        passwordInputObj.send_keys(password)
        driver.save_screenshot("instabotpy_before_clicking_login_button.png")
        buttonObj = driver.find_element_by_css_selector('button').click()
        sleep(3)
    except NoSuchElementException as err:
        exit_gracefully(driver, "[!] Error while trying to log in. [login]", err.msg)
    if check_exists_by_css_selector(driver, '#slfErrorAlert'):
        return False
    else:
        sleep(5)
        driver.save_screenshot("instabotpy_after_login.png")
        return True

# all search results after typing in main search bar :
# [role="navigation"] a[href]:not([class*="coreSpriteDesktopNav"])

# wrapper selector for all suggestions (need to ignore first) :
# #mainFeed ul li

# when in a profile page :
        # 1) get number of fallowers :
        # header ul li:nth-child(2) a span ['title']
        #
        # 2) fallow this person : 
        # header button:not(.coreSpriteOptionsEllipsis) (it will return an array of 2 objects - get the first)
        #
        # 3) check if the username is listed to a gmail account with the same suername.
        # h1 (get text)
        # run it against our gmail checker.
        #
        # 4) click to see all fallowers, than get all of them :
        # header ul li:nth-child(2) a  (click)
        # .......scroll to infinity......
        # div[role="dialog"] ul li a[title] (link to each profile)
        # div[role="dialog"] ul li button (link to follw each user)
        #
        # 5) press the "Load More" button and scroll all the person's photos until you reach the end,
        # then get all links to photos in feed : 
        # article > div > a (load more button)
        # article div div div div a (array of links)

def main(loginPage, username):
    password = parse_args()
    m_driver = init_webdriver()
    m_driver.get(loginPage)
    m_driver.save_screenshot("instabotpy_page_upload.png")

    if not login(m_driver, username, password):
        exit_gracefully(m_driver, "[#] Please check your username and password and try again.")


    exit_gracefully(m_driver, "[#] End Of Program")

if __name__ == '__main__':
    loginPage = "https://www.instagram.com/accounts/login/"
    m_username = "instabotpy@gmail.com"
    main(loginPage, m_username)