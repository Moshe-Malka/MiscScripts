from selenium import webdriver
from selenium import common
from selenium.common.exceptions import *
from time import sleep
from sys import exit
import json
import csv
import argparse
from time import strftime

def initWebdriver():
    try:
        w_driver = webdriver.PhantomJS()
        w_driver.set_window_size(1920, 1080)
        print "[#] new WebDriver Initialized."
        return w_driver
    except WebDriverException as err:
        print "[!] Web Driver Exception. [initWebdriver]"
        exit(1)

def exitGracefully(driver,custom_message,error_message = None):
    try:
        if(error_message!=None): print e_message
        print custom_message
        driver.quit()
        exit(1)
    except Exception:
        pass

def check_exists_by_css_selector(w_driver,css):
    try:
        w_driver.find_element_by_css_selector(css)
    except NoSuchElementException:
        return False
        print "[#] Could Not Find Results."
    return True

def login(w_driver,emailAddress,password):
    try:
        if(len(emailAddress)==0 or len(password)==0): raise Exception
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
        exitGracefully(w_driver,"[!] No Such Element. [login]")
    except Exception as err2:
        w_driver.save_screenshot("linkedin_login_failed.png")
        exitGracefully(w_driver,"[!] Login Failed! [login]")

def doSearch(w_driver,baseUrl,searchUrl,keyword):
    try:
        print "[#] Searching - "+keyword+" ....."
        w_driver.get(baseUrl+searchUrl+keyword)
        sleep(3)
        w_driver.save_screenshot('linkedin_searchResults.png')
        return check_exists_by_css_selector(w_driver,".search-no-results__message--muted-no-type")
    except WebDriverException as err:
        exitGracefully(w_driver,"[!] Web Driver Exception. [trySearch]")

def getListing(w_driver):
    try:
        res = w_driver.find_elements_by_css_selector(".results-list li.search-result")
        return res
    except WebDriverException as err:
        exitGracefully(w_driver,"[!] Web Driver Exception. [getListing]")

def printResults(results):
    i=1
    for result in results:
        try:
            print "----------------------["+str(i)+"]----------------------"
            print result.find_element_by_css_selector("a h3").text
            # print result.find_element_by_css_selector("a").get_attribute("href")
            print result.find_element_by_css_selector(".subline-level-1").text
            print result.find_element_by_css_selector(".subline-level-2").text
        except NoSuchElementException as err:
            pass
        i+=1
        # print "------------------------------------------------"
def clickAllEmployeesButton(m_driver):
    try:
        m_driver.save_screenshot('linkedin_before_next_hop.png')
        css = ".org-company-employees-snackbar__details-highlight.snackbar-description-see-all-link"
        all_employees_btn = m_driver.find_element_by_css_selector(css).click()
    except NoSuchElementException as e:
        exitGracefully(m_driver,"[!] No Such Element - "+css,e.message)
    except Exception as err:
        exitGracefully(m_driver,"[!] Exception",err.message)
    sleep(5)

def getCompany(m_driver,baseUrl,searchUrl):
    keyword = raw_input("[>] please enter company name : ")
    no_results_flag = doSearch(m_driver,baseUrl,searchUrl,keyword)
    results=[]
    if(not no_results_flag):
        results = getListing(m_driver)
        printResults(results)
    else:
        exitGracefully(m_driver,"[!] Company name was not found in Linkedin.")
    while(True):
        try:
            choice = raw_input("[>] please choose a company listed above : ")
            if( int(choice)<1 or int(choice)>len(results) ):
                raise Exception
            break
        except Exception as err:
            print "[!] ValueError - must be a number greater or equal to one! try again..."
    return results[int(choice)-1],keyword

def preparePageForExtraction(m_driver):
    m_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(5)
    m_driver.save_screenshot('linkedin_workers_listing.png')
    amount_of_workers = m_driver.find_element_by_css_selector("h3.search-results__total").text.split("Showing ")[1].split(" ")[0].strip()
    print "[#] Found " + amount_of_workers + " Workers."

def scrapeEmployeesPage(driver):
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
    except Exception as err:
        exitGracefully(driver,"[!] Exception Accourred - [scrapeEmployeesPageRec]", err.message)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="the username for Linkedin account which will be used for scraping.", default="")
    parser.add_argument("password", help="the password for Linkedin account which will be used for scraping.", default="")
    args = parser.parse_args()
    ########### constents ###########
    baseUrl = "https://www.linkedin.com"
    searchUrl = "/search/results/companies/?keywords="
    ########### constents ###########
    m_driver = initWebdriver()
    m_driver.get(baseUrl)
    print "[#] Logging in with: " + str(args.username) + " | " + str(args.password)
    login(m_driver,args.username,args.password)
    user_choice,companyName = getCompany(m_driver,baseUrl,searchUrl)
    nextLink = user_choice.find_element_by_css_selector("a").get_attribute("href")
    m_driver.get(nextLink)
    clickAllEmployeesButton(m_driver)
    preparePageForExtraction(m_driver)
    data=scrapeEmployeesPage(m_driver)
    print "[#] Finished Scraping : " + str(len(res)) + " Workers."
    outputSelection = raw_input("[>] Output Data To ( JSON file = j , CSV file = c , Output to Screen = o ) : ")
    t = strftime("%d/%m/%Y_%H:%M:%S")
    if(outputSelection == 'j'):
        with open("output_"+companyName+"_"+t+".json", 'w') as outfile:
            json.dump(data, outfile)
    else if(outputSelection == 'c'):
        f = csv.writer(open("output_"+companyName+"_"+t+".csv", "wb+"))
        f.writerow(["Full Name", "Position", "Location", "Link", "Profile Photo"]) #'':full_name,'':pos,'':loc,'':link,''
        for c in data:
            f.writerow([c["Full Name"],
                        c["Position"],
                        c["Location"],
                        c["Link"],
                        c["Profile Photo"]])
    else:
        for o in data:
            print o
    exitGracefully(m_driver,"[#] End Of Program")
