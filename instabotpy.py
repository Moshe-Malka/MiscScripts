from selenium import webdriver
from selenium import common
from selenium.common.exceptions import *
from time import sleep
from sys import exit
import argparse


def initWebdriver():
    try:
        driver = webdriver.PhantomJS()
        driver.set_window_size(1920, 1080)
        print "[#] new WebDriver Initialized."
        return driver
    except WebDriverException as err:
        print "[!] Web Driver Exception. [initWebdriver]"
        exit(1)

def exitGracefully(driver,custom_message,error_message = None):
    try:
        if(error_message!=None): print e_message
        print custom_message
        driver.quit()
    except Exception:
        pass
    exit(1)

def check_exists_by_css_selector(driver,css):
    try:
        driver.find_element_by_css_selector(css)
    except NoSuchElementException:
        return False
        print "[#] Could Not Find Results."
    return True

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("password", help="the password for InstaBotPy account which will be used for scraping.", default="")
    args = parser.parse_args()
    return args.password

############## Constents ##############
loginPage = "https://www.instagram.com/accounts/login/"
username = "instabotpy@gmail.com"

password = parseArgs()

m_driver = initWebdriver()
m_driver.get(loginPage)
m_driver.save_screenshot("instabotpy_page_upload.png")
sleep(2)
usernameInputObj = m_driver.find_element_by_css_selector('input[name="username"]')
usernameInputObj.send_keys(username)
passwordInputObj = m_driver.find_element_by_css_selector('input[name="password"]')
passwordInputObj.send_keys(password)
m_driver.save_screenshot("instabotpy_before_clicking_login_button.png")
buttonObj = m_driver.find_element_by_css_selector('button').click()
sleep(3)
if(check_exists_by_css_selector(m_driver,'#slfErrorAlert')):
    exitGracefully(m_driver,"[#] The username you entered doesn't belong to an account. Please check your username and try again.")
else:
    sleep(5)
    m_driver.save_screenshot("instabotpy_after_login.png")
    # continue in main scrren






exitGracefully(m_driver,"[#] End Of Program")
