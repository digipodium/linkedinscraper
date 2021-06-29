from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from linkedin_scraper import Person, actions
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(ChromeDriverManager().install())



email = "wasimprince252@gmail.com"
password = "Qwerty#000"
actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
person = Person("https://www.linkedin.com/in/adrian0350", contacts=[], driver=driver)

print("Person: " + person.name)
print("Person contacts: ")
time.sleep(10)

for contact in person.contacts:
	print("Contact: " + contact.name + " - " + contact.occupation + " -> " + contact.url)