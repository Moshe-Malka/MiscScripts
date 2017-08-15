from selenium import webdriver
from selenium import common
from selenium.common.exceptions import *
from time import sleep
from sys import exit
def initWebdriver():
    try:
        w_driver = webdriver.PhantomJS()
        w_driver.set_window_size(1920, 1080)
        return w_driver
    except WebDriverException as err:
        print "[!] Web Driver Exception. [initWebdriver]"
        exit(1)

def login(w_driver,emailAddress,password):
    try:
        passw = w_driver.find_element_by_id("login-password") 
        email = w_driver.find_element_by_id("login-email")
        email.send_keys(emailAddress)
        sleep(1.5)
        passw.send_keys(password)
        sleep(1.5)
        w_driver.find_element_by_id("login-submit").click()
        w_driver.save_screenshot("linkedin_after_login.png")
    except NoSuchElementException as err:
        print "[!] No Such Element. [login]"
        exit(1)

def check_exists_by_css_selector(w_driver,css):
    try:
        w_driver.find_element_by_css_selector(css)
    except NoSuchElementException:
        return False
    return True

def trySearch(w_driver,baseUrl,searchUrl,keyword):
    try:
        w_driver.get(baseUrl+searchUrl+keyword)
        sleep(3)
        w_driver.save_screenshot('linkedin_searchResults.png')
        return check_exists_by_css_selector(w_driver,".search-no-results__message--muted-no-type")
    except WebDriverException as err:
        print "[!] Web Driver Exception. [trySearch]"
        exit(1)

def getListing(w_driver):
    try:
        res = w_driver.find_elements_by_css_selector(".results-list li.search-result")
        return res
    except WebDriverException as err:
        print "[!] Web Driver Exception. [getListing]"
        exit(1)

def printResults(results):
    for result in results:
        try:
            print result.find_element_by_css_selector("a h3").text
            print result.find_element_by_css_selector("a").get_attribute("href")
            print result.find_element_by_css_selector(".subline-level-1").text
            print result.find_element_by_css_selector(".subline-level-2").text
        except NoSuchElementException as err:
            pass
        print "#"*50

if __name__ == "__main__":
    ########### constents ########### 
    baseUrl = "https://www.linkedin.com"
    searchUrl = "/search/results/companies/?keywords="
    #################################
    m_driver = initWebdriver()
    m_driver.get(baseUrl)
    login(m_driver,"moshemalka2014@gmail.com","kiko7287")
    m_driver.save_screenshot('linkedin_loggedIn.png')
    sleep(1.5)
    keyword = raw_input("[>] please enter company name : ")
    flag = trySearch(m_driver,baseUrl,searchUrl,keyword)
    if(not flag):
        results = getListing(m_driver)
        printResults(results)
    else:
        print "[!] Company name was not found in Linkedin."
        print "[!] see screenshot named 'linkedin_searchResults.png' for queries."
    m_driver.quit()



















# ################################ Options : ################################
# #1
# jobs_btn = w_driver.find_element_by_id("jobs-tab-icon").click()

# #2
# my_network_btn = w_driver.find_element_by_id("mynetwork-tab-icon").click()
# # scroll down to infinity
# SCROLL_PAUSE_TIME = 0.5
# # Get scroll height
# last_height = driver.execute_script("return document.body.scrollHeight")
# while True:
#     # Scroll down to bottom
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     # Wait to load page
#     time.sleep(SCROLL_PAUSE_TIME)
#     # Calculate new scroll height and compare with last scroll height
#     new_height = driver.execute_script("return document.body.scrollHeight")
#     if new_height == last_height:
#         break
#     last_height = new_height
# connect_links = w_driver.find_elements_by_class_name("button-secondary-small")
# names = w_driver.find_elements_by_class_name("mn-person-info__name").text

# for link, name in connect_links, names:
#     print "[#] Sent Connection Invite To : " + str(name).strip()
#     link.click()