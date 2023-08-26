from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random
import chromedriver_binary
import time

# creates the pokemon objects
class pokemon: 
    
    def __init__(self, name, level, moveset):
        
        # defines the name of the pokemon 
        self.name = name

        # defines the lvel of the pokemon
        self.level = level

        # defines the moveset of the pokemon
        self.moveset = moveset

    def get_name(self):
        return self.name
    
    def get_level(self):
        return self.level
    
    def get_moveset(self):
        return self.moveset

    def set_name(self, name):
      self.name = name

    def set_level(self, level):
        self.level = level
    
    def set_moveset(self, moveset):
        self.moveset = moveset
            
class Gym:
    
    def __init__(self, leader_name, leader_type, party, is_single_battle, items):
        
        # defines the gym leader's name
        self.leader_name = leader_name

        # defines the gym leader's type
        self.leader_type = leader_type

        # defines the party of the gym leader
        self.party = party

        # defines if the gym leader battle type is a single battle
        self.is_single_battle = is_single_battle

        # defines any items the gym leader carries
        self.items = items

    def get_leader_name(self):
        return self.leader_name
    
    def get_leader_type(self):
        return self.leader_type
    
    def get_party(self):
        return self.party
    
    def get_is_single_battle(self):
        return self.is_single_battle
    
    def get_items(self):
        return self.items
    
    def set_leader_name(self, leader_name):
        self.leader_name = leader_name

    def set_leader_type(self, leader_type):
        self.leader_type = leader_type

    def set_party(self, party):
        self.party = party

    def set_is_single_battle(self, is_single_battle):
        self.is_single_battle = is_single_battle

    def set_items(self, items):
        self.items = items

# init driver object
driver = webdriver.Chrome()

# navigate to the data page
driver.get("https://www.serebii.net/")

# init an action chains object
actions = ActionChains(driver)

# press down on the down arrow 50 times
time.sleep(random.randint(2, 5))
for i in range(50):
    actions.send_keys(Keys.ARROW_DOWN).perform()

# click an element
time.sleep(random.randint(2, 5))
element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="lbar_ul"]/li[3]/ul/li[104]/a'))).click()

# click an element
time.sleep(random.randint(2, 5))
element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="rbar"]/div[6]/ul/li[8]/a'))).click()

# getting data from xpath gyms
# for i in range(1, 9):
time.sleep(random.randint(2, 5))
element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/main/table/tbody/tr[2]/td[1]/table/tbody')))
print(element.text)
print(type(element.text))
gym_data = element.text.split(" ")
print(gym_data)
element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="rbar"]/div[6]/ul/li[9]/a'))).click()
print(driver.title)