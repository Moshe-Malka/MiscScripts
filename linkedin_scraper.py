from selenium import webdriver
from selenium import common
from selenium.common.exceptions import *
from time import sleep
from sys import exit
import json
def initWebdriver():
    try:
        w_driver = webdriver.PhantomJS()
        w_driver.set_window_size(1920, 1080)
        print "[#] new WebDriver Initialized."
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
        print "[#] Login Successfull."
    except NoSuchElementException as err:
        print "[!] No Such Element. [login]"
        exit(1)

def check_exists_by_css_selector(w_driver,css):
    try:
        w_driver.find_element_by_css_selector(css)
    except NoSuchElementException:
        return False
        print "[#] Could Not Find Results."
    print "[#] Found Results."
    return True

def trySearch(w_driver,baseUrl,searchUrl,keyword):
    try:
        print "[#] Searching -  "+keyword+" ....."
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
    i=1
    for result in results:
        try:
            print "------------------["+str(i)+"]------------------"
            print result.find_element_by_css_selector("a h3").text
            print result.find_element_by_css_selector("a").get_attribute("href")
            print result.find_element_by_css_selector(".subline-level-1").text
            print result.find_element_by_css_selector(".subline-level-2").text
        except NoSuchElementException as err:
            pass
        i+=1
        print "#"*50
def scrapeEmployeesPageRec(driver):
    global output_array
    workers_wrapper = driver.find_elements_by_css_selector(".search-result.search-result__occluded-item.ember-view")    
    for worker in workers_wrapper:
        tmp_arr[0] = worker.find_element_by_css_selector(".name.actor-name").text  #full name
        tmp_arr[1] = worker.find_element_by_css_selector(".subline-level-1.search-result__truncate").text  #position
        tmp_arr[2] = worker.find_element_by_css_selector(".subline-level-2.search-result__truncate").text  #location
        tmp_arr[3] = worker.find_element_by_css_selector(".search-result__image-wrapper .search-result__result-link").get_attribute("href")  #link to profile
        if(check_exists_by_css_selector(".search-result__image .lazy-image.ghost-person")):
            tmp_arr[4] = "no thumbnail available"
        else:
            tmp_arr[4] = driver.find_element_by_css_selector(".search-result__image .lazy-image.loaded").get_attribute("src")
        output_array.append(temp_arr)
    sleep(1.5)
    if(check_exists_by_css_selector(driver,"button.next")):
        driver.find_element_by_css_selector("button.next").click()
        scrapeEmployeesPage(driver)
    else:
        return output_array

if __name__ == "__main__":
    ########### constents ########### 
    baseUrl = "https://www.linkedin.com"
    searchUrl = "/search/results/companies/?keywords="
    outputFilename = "LinkesinScraper_results_"
    output_array=[]

    m_driver = initWebdriver()
    m_driver.get(baseUrl)
    login(m_driver,"**************","************")
    m_driver.save_screenshot('linkedin_loggedIn.png')
    sleep(1.5)
    keyword = raw_input("[>] please enter company name : ")
    flag = trySearch(m_driver,baseUrl,searchUrl,keyword)
    results=[]
    if(not flag):
        results = getListing(m_driver)
        printResults(results)
    else:
        print "[!] Company name was not found in Linkedin."
        print "[!] see screenshot named 'linkedin_searchResults.png' for queries."
    while(True):
        try:
            choice = raw_input("[>] please choose a company listed above : ")
            int(choice)
            if(int(choice)<1<len(results)): 
                raise Exception
            break
        except Exception as err:
            print "[!] must be a number !. try again..."
    choice=int(choice)-1
    nextLink = results[choice].find_element_by_css_selector("a").get_attribute("href")
    
    m_driver.quit()
    m2_driver = initWebdriver()
    m2_driver.get(nextLink)
    m2_driver.save_screenshot('linkedin_companyPage.png')
    m2_driver.find_element_by_css_selector(".snackbar-description-see-all-link").click()
    sleep(2)
    amount_of_workers = str(m2_driver.find_elements_by_css_selector("h3.search-results__total").text).split("Showing ")[1].strip()
    m2_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print "[#] Starting to scrape " + amount_of_workers + " workers........"
    scrapeEmployeesPageRec(m2_driver)
        
    


    m2_driver.quit()
