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
from collections import defaultdict

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
    # print(gym_data)
    for i in range(gym_data.size):
        for j in range(gym_data[i].size):
            if (j == 0 and gym_data[i].size > 3):
                if (gym_data[i][j] == 'Gym' and gym_data[i][j + 1] == 'Leader'):
                    gym.set_leader_name(gym_data[i][j + 2])

def collect_region(xpath):
    time.sleep(random.randint(2, 5))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    words = element.text.split(" ")
    return words[2]

def collect_gym_name(xpath):
    time.sleep(random.randint(2, 5))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    words = element.text.split(" ")
    return words[1]

def collect_metadata(xpath):

    return_dict = {}
    time.sleep(random.randint(2, 5))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    hold = element.text.split("\n")
    for i in range(len(hold)):
        if (hold[i].startswith("Location") or hold[i].startswith("Gym Leader") or hold[i].startswith("Specialty")):
            fields = hold[i].split(": ")
            return_dict[fields[0]] = fields[1]
        elif (hold[i].startswith("Reward")):
            fields_sep_by_comma = hold[i].split(",")
            badge = fields_sep_by_comma[0].split("Reward: ")
            HM = fields_sep_by_comma[2].split(" ")
            return_dict['Badge'] = badge[1]
            return_dict['TM'] = fields_sep_by_comma[1]
            return_dict['HM'] = HM[3]

    return return_dict

def collect_number_of_pokemon(xpath):
    time.sleep(random.randint(2, 5))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    fields = element.text.split(" ")
    return len(fields) - 3
    
    


if __name__ == "__main__":

    region_dict = {}

    # init driver object
    driver = webdriver.Chrome()

    # navigate to the data page
    driver.get("https://www.serebii.net/")

    # init an action chains object
    actions = ActionChains(driver)

    scroll_down(50)

    make_click('//*[@id="lbar_ul"]/li[3]/ul/li[104]/a')

    make_click('//*[@id="rbar"]/div[6]/ul/li[8]/a')

    # collect_all_data('//*[@id="content"]/main/table/tbody/tr[2]/td[1]/table/tbody')

    text = collect_region('//*[@id="rbar"]/div[6]/ul/li[2]/a')

    region_dict[text] = {
    }

    gym_dict = {}
    xpath = '//*[@id="content"]/main/table/tbody/tr[1]/td/font'
    gym_dict['gym_number'] = collect_gym_name(xpath)

    #print(region_dict)

    text = collect_metadata('//*[@id="content"]/main/table/tbody/tr[2]/td[1]/p[1]')

    text = collect_number_of_pokemon('//*[@id="content"]/main/table/tbody/tr[2]/td[1]/table/tbody/tr[2]')
    print(text)

    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="rbar"]/div[6]/ul/li[9]/a'))).click()
    #print(driver.title)