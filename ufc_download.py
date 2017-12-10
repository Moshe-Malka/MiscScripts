from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from sys import exit
from time import sleep
import re
import requests

def initWebdriver():
    try:
        # w_driver = webdriver.PhantomJS(desired_capabilities=DesiredCapabilities.CHROME)
        path=r"C:\Users\User\Downloads\chromedriver_win32\chromedriver.exe"
        w_driver = webdriver.Chrome(path)
        w_driver.set_window_size(1920, 1080)
        print "[#] new WebDriver Initialized."
        return w_driver
    except WebDriverException as err:
        print "[!] Web Driver Exception. [initWebdriver]"
        exit(1)

def exitGracefully(driver,custom_message,error_message = None):
    try:
        if(error_message!=None): print error_message
        print custom_message
        driver.quit()
    except Exception:
        pass

def check_exists_by_css_selector(w_driver,css):
    try:
        w_driver.find_element_by_css_selector(css)
    except NoSuchElementException:
        return False
        print "[#] Could Not Find Results."
    return True

def downloadVideo(name, url):
    name=name+".mp4"
    r=requests.get(url)
    print "****Connected****"
    with open(name, 'wb') as f:
        print "Downloading....."
        for chunk in r.iter_content(chunk_size=255): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    print "Done"

def get_current_event_name():
    return "UFC Fight Night 123"

if __name__ == '__main__':
    home = "http://www.allwrestling.org/ufc/"
    m_driver = initWebdriver()
    current_event_name = get_current_event_name()
    m_driver.get(home)

    # go over the links in the main page and find the latest UFC event (check it against a list).
    links = m_driver.find_elements_by_css_selector('div[data-view="grid-mini"] a.clip-link')
    for link in links:
        if re.findall(r'(UFC\s[\d]*)', link.get_attribute("title"), re.M):
            current_link = link
            break
    assert current_link
    print current_link.get_attribute("href")

    # go to the event page
    m_driver.get(current_link.get_attribute("href"))
    sleep(5)
    streamango_links = m_driver.find_element_by_css_selector(
        "p > a.small.cool-blue.vision-button[href^='http://streamango.com']")
    for link in streamango_links:
        if "Full Show" in link.text.strip():
            main_link = link
            break
    assert main_link
    print main_link.get_attribute("href")

    # go to the strmango link
    m_driver.get(main_link.get_attribute("href"))
    sleep(25)
    video_link = m_driver.find_element_by_css_selector(".videocontainer video.vjs-tech").get_attribute("src")
    assert video_link
    fq_link = "http:" + video_link
    print fq_link

    # go to the last page - video download page
    m_driver.get(fq_link)
    sleep(10)
    downloadUrl = m_driver.find_element_by_css_selector("source").get_attribute("src")
    assert downloadUrl
    downloadVideo("test",downloadUrl)



    print "[!] DONE !"


    m_driver.save_screenshot("video_link.png")

    exitGracefully(m_driver, "[*] Exiting...")