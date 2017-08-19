from selenium import webdriver
from selenium import common
from selenium.common.exceptions import *
from time import sleep
from sys import exit
import json
import argparse

def initWebdriver():
    try:
        w_driver = webdriver.PhantomJS()
        w_driver.set_window_size(1920, 1080)
        print "[#] new WebDriver Initialized."
        return w_driver
    except WebDriverException as err:
        print "[!] Web Driver Exception. [initWebdriver]"
        exit(1)

def check_exists_by_css_selector(w_driver,css):
    try:
        w_driver.find_element_by_css_selector(css)
    except NoSuchElementException:
        return False
        print "[#] Could Not Find Results."
    return True

def login(w_driver,emailAddress,password):
    try:
        passw = w_driver.find_element_by_id("login-password")
        email = w_driver.find_element_by_id("login-email")
        email.send_keys(emailAddress)
        sleep(1.5)
        passw.send_keys(password)
        sleep(1.5)
        w_driver.find_element_by_id("login-submit").click()
        sleep(5)
        if(check_exists_by_css_selector(w_driver,".core-rail")):
            w_driver.save_screenshot("linkedin_after_login.png")
            print "[#] Login Successfull."
        else:
            raise Exception
    except NoSuchElementException as err1:
        print "[!] No Such Element. [login]"
        w_driver.quit()
        exit(1)
    except Exception as err2:
        print "[!] Login Failed! [login]"
        w_driver.save_screenshot("linkedin_login_failed.png")
        w_driver.quit()
        exit(1)

def doSearch(w_driver,baseUrl,searchUrl,keyword):
    try:
        print "[#] Searching - "+keyword+" ....."
        w_driver.get(baseUrl+searchUrl+keyword)
        sleep(3)
        w_driver.save_screenshot('linkedin_searchResults.png')
        return check_exists_by_css_selector(w_driver,".search-no-results__message--muted-no-type")
    except WebDriverException as err:
        print "[!] Web Driver Exception. [trySearch]"
        w_driver.quit()
        exit(1)

def getListing(w_driver):
    try:
        res = w_driver.find_elements_by_css_selector(".results-list li.search-result")
        return res
    except WebDriverException as err:
        print "[!] Web Driver Exception. [getListing]"
        w_driver.quit()
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
        print "------------------------------------------------"
# def scrapeEmployeesPageRec(driver):
#     try:
#         global output_array
#         workers_wrapper = driver.find_elements_by_css_selector(".search-result.search-result__occluded-item.ember-view")
#         for worker in workers_wrapper:
#             tmp_arr=[]
#             tmp_arr.append(worker.find_element_by_css_selector("span.name-and-icon > span:not(.premium-icon)").text)  #full name
#             tmp_arr.append(worker.find_element_by_css_selector("p.subline-level-1.search-result__truncate").text)  #position
#             tmp_arr.append(worker.find_element_by_css_selector(".subline-level-2.search-result__truncate").text)  #location
#             tmp_arr.append(worker.find_element_by_css_selector(".search-result__image-wrapper .search-result__result-link").get_attribute("href"))  #link to profile
#             if(check_exists_by_css_selector(driver,".search-result__image .lazy-image.ghost-person")):
#                 tmp_arr.append("no thumbnail available")
#             else:
#                 tmp_arr.append(driver.find_element_by_css_selector("figure > img").get_attribute("src"))
#             output_array.append(temp_arr)
#         sleep(1.5)
#         if(check_exists_by_css_selector(driver,"button.next")):
#             driver.find_element_by_css_selector("button.next").click()
#             sleep(10)
#             m_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             sleep(10)
#             scrapeEmployeesPage(driver)
#         else:
#             return output_array
#     except Exception as e:
#         print "[!] Exception Accourred - [scrapeEmployeesPageRec]"
#         print e.message
#         m_driver.quit()
#         exit(1)
def scrapeEmployeesPageRec(driver):
    global output_array
    page_count=1
    try:
        while(True):
            workers_wrapper = driver.find_elements_by_css_selector(".search-result.search-result__occluded-item.ember-view")
            for worker in workers_wrapper:
                full_name = worker.find_element_by_css_selector("span.name-and-icon > span:not(.premium-icon)").text  #full name
                pos = worker.find_element_by_css_selector("p.subline-level-1.search-result__truncate").text  #position
                loc = worker.find_element_by_css_selector(".subline-level-2.search-result__truncate").text  #location
                link = worker.find_element_by_css_selector(".search-result__image-wrapper .search-result__result-link").get_attribute("href")  #link to profile
                if(check_exists_by_css_selector(driver,".search-result__image .lazy-image.ghost-person")):
                    photo = "no thumbnail available"
                else:
                    photo = driver.find_element_by_css_selector("figure > img").get_attribute("src")
                output_array.append(json.dumps({'Full Name':full_name,'Position':pos,'Location':loc,'Link':link,'Profile Photo':photo}))
            sleep(1.5)
            if(check_exists_by_css_selector(driver,"button.next")):
                driver.find_element_by_css_selector("button.next").click()
                sleep(10)
                m_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(5)
                m_driver.save_screenshot("linkedin_workers_page_number_"+str(page_count)+".png")
                page_count+=1
            else:
                break
        return output_array
    except Exception as e:
        print "[!] Exception Accourred - [scrapeEmployeesPageRec]"
        print e.message
        m_driver.quit()
        exit(1)
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="the username for Linkedin account which will be used for scraping.", default="")
    parser.add_argument("password", help="the password for Linkedin account which will be used for scraping.", default="")
    args = parser.parse_args()
    ########### constents ###########
    baseUrl = "https://www.linkedin.com"
    searchUrl = "/search/results/companies/?keywords="
    outputFilename = "LinkesinScraper_results_"
    output_array=[]
    ########### constents ###########
    m_driver = initWebdriver()
    m_driver.get(baseUrl)
    print "[#] Logging in with: " + str(args.username) + " | " + str(args.password)
    login(m_driver,args.username,args.password)
    m_driver.save_screenshot('linkedin_loggedIn.png')
    sleep(1.5)
    keyword = raw_input("[>] please enter company name : ")
    flag = doSearch(m_driver,baseUrl,searchUrl,keyword)
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
            print "[!] must be a number greater or equal to one! try again..."
    choice=int(choice)-1
    nextLink = results[choice].find_element_by_css_selector("a").get_attribute("href")
    m_driver.save_screenshot('linkedin_before_next_hop.png')
    sleep(2)
    m_driver.get(nextLink)
    sleep(2)
    m_driver.save_screenshot('linkedin_after_next_hop.png')
    try:
        elem = m_driver.find_element_by_css_selector(".org-company-employees-snackbar__details-highlight.snackbar-description-see-all-link")
    except NoSuchElementException as e:
        print "[!] No Such Element - .org-company-employees-snackbar__details-highlight.snackbar-description-see-all-link"
        m_driver.quit()
        exit(1)
    elem.click()
    m_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(5)
    m_driver.save_screenshot('linkedin_workers_listing.png')
    amount_of_workers = str(m_driver.find_element_by_css_selector("h3.search-results__total").text).split("Showing ")[1].split(" ")[0].strip()
    print "[#] Found " + amount_of_workers + " Workers."

    res=scrapeEmployeesPageRec(m_driver)
    print "[#] Finished Scraping : " + str(len(res)) + " Workers."
    for r in res:
        print r




    m_driver.quit()
    exit(1)
