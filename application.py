from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random
import chromedriver_binary
import time
import re
import numpy as np

# creates the pokemon objects
class Pokemon: 
    
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

    leader_name = ""
    leader_type = ""
    party = []
    is_single_battle = True
    items = []

    def __init__(self):

        self.leader_name = ""
        self.leader_type = ""
        self.party = []
        self.is_single_battle = True
        self.items = []
    
    def __init__(self, leader_name = "", leader_type = "", party = [], is_single_battle = True, items = []):
        
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

def scroll_down(press_count):

    # press down on the down arrow 50 times
    time.sleep(random.randint(2, 5))
    for i in range(press_count):
        actions.send_keys(Keys.ARROW_DOWN).perform()

def make_click(xpath):

    # click an element
    time.sleep(random.randint(2, 5))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

def collect_all_data(xpath):

    # getting data from xpath gyms
    time.sleep(random.randint(2, 5))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))

    gym_data = np.array(element.text.split('\n'), dtype=object)
    gym = Gym()
    for i in range(gym_data.size):
        gym_data[i] = np.char.split(gym_data[i])
    print(gym_data)
    for i in range(gym_data.size):
        for j in range(gym_data[i].size):
            if (j == 0 and gym_data[i].size > 3):
                if (gym_data[i][j] == 'Gym' and gym_data[i][j + 1] == 'Leader'):
                    gym.set_leader_name(gym_data[i][j + 2])


if __name__ == "__main__":

    # init driver object
    driver = webdriver.Chrome()

    # navigate to the data page
    driver.get("https://www.serebii.net/")

    # init an action chains object
    actions = ActionChains(driver)

    scroll_down(50)

    make_click('//*[@id="lbar_ul"]/li[3]/ul/li[104]/a')

    make_click('//*[@id="rbar"]/div[6]/ul/li[8]/a')

    collect_all_data('//*[@id="content"]/main/table/tbody/tr[2]/td[1]/table/tbody')

    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="rbar"]/div[6]/ul/li[9]/a'))).click()
    print(driver.title)