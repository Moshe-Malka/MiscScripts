from time import sleep
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
    "(KHTML, like Gecko) Chrome/15.0.87"
)

base = "https://www.facebook.com"
w_driver = webdriver.PhantomJS(desired_capabilities=dcap)
w_driver.set_window_size(1124, 850)
w_driver.get(base)
# print w_driver.page_source
sleep(2)


w_driver.save_screenshot('login_page.png')

email = w_driver.find_element_by_id("email")
sleep(1.5)
passw = w_driver.find_element_by_id("pass") 
sleep(1.5)
email.send_keys("***********@*******.*******")
sleep(1.5)
passw.send_keys("***************")
sleep(1.5)
w_driver.save_screenshot('entered_keys.png')

submit = w_driver.find_element_by_id("u_0_r")
sleep(1.5)
submit.click()
sleep(5)
w_driver.save_screenshot('looged_in.png')
try:
    w_driver.find_element_by_css_selector("._4rbf._53ij > a")   # error selector - if we see it we are NOT logged in.
    print "Login Failed !"
except Exception:
    print "Login Succeeded !"



'''
Logout
'''
sleep(3)
w_driver.find_element_by_class_name("_w0d").click()
sleep(1.5)
w_driver.save_screenshot('logeed_out.png')

w_driver.close()
