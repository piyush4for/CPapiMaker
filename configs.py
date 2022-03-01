from selenium import webdriver
import sys

DIRECTORY = 'reports'

codechefURL = "https://www.codechef.com/contests"
codeforceURL = "codeforces"
hackerearthURL = "hackerearth"
leetcodeURL = "leetcode"

def get_chrome_web_driver(options):
    return webdriver.Chrome('./chromedriver',chrome_options=options)

#used one line function instead just one line becoz its a good prcatice
def get_web_driver_options():
    return webdriver.ChromeOptions()

#i got from stackoverflow thats the best way to run Selenium
def set_ignore_certificate_error(options):
    options.add_argument('--ignore-certificate-errors')

def set_browser_as_incognito(options):
    options.add_argument('--incognito')