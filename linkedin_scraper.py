from selenium import webdriver
from selenium import common
from time import sleep
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
    "(KHTML, like Gecko) Chrome/15.0.87")

baseUrl="https://www.linkedin.com"
w_driver = webdriver.PhantomJS(desired_capabilities=dcap)
w_driver.set_window_size(1124, 850)
w_driver.get(baseUrl)
sleep(2)

passw = w_driver.find_element_by_id("login-password") 
email = w_driver.find_element_by_id("login-email")
email.send_keys("*****@*********.com")
sleep(1.5)
passw.send_keys("***********")

login_btn = w_driver.find_element_by_id("login-submit").click()
sleep(1.5)

w_driver.save_screenshot('entered_keys.png')


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



w_driver.close()
