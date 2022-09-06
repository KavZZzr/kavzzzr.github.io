from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
 
#--| Setup
options = Options()
#options.add_argument("--headless")
#options.add_argument("--window-size=1980,1020")
browser = webdriver.Chrome(executable_path=r'C:/Users/61420/anaconda3/chromedriver.exe', options=options)
#--| Parse or automation
url = "https://www.youtube.com/results?search_query=python"
browser.get(url)
time.sleep(2)
 
# Use Bs to Parse
soup = BeautifulSoup(browser.page_source, 'lxml')
first_title = soup.find('a', id="video-title")
print(first_title.text.strip())
 
print('-' * 50)
# Use Selenium to parse
second_title_sel = browser.find_elements_by_xpath('//*[@id="video-title"]')
print(second_title_sel[1].text)