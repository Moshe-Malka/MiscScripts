from selenium import webdriver
from selenium import common
import datetime, time

main_url = "http://www.gatherproxy.com/proxylist/anonymity/?t=Elite"
m_driver = webdriver.PhantomJS()
m_driver.set_window_size(1920, 1080)

m_driver.get(main_url)
ts = time.time()
t = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d-%H_%M_%S')
m_driver.save_screenshot("proxy_list_"+str(t)+".png")

proxies_list = m_driver.find_elements_by_css_selector('tr[class^="proxy"]')
for proxy in proxies_list:
    print "[#] Proxy : {0}      From : {1}".format(str(proxy.get_attribute("prx")),str(proxy.get_attribute("country")))
    print "-"*100