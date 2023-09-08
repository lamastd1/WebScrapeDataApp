from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random
import chromedriver_binary
import time
import numpy as np
import json

def scroll_up(press_count):
     # press down on the down arrow 50 times
    time.sleep(random.randint(2, 5))
    for i in range(press_count):
        actions.send_keys(Keys.ARROW_UP).perform()

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
            print(fields_sep_by_comma)
            if (len(fields_sep_by_comma) > 2):
                HM = fields_sep_by_comma[2].split(" ")
            return_dict['Badge'] = badge[1]
            return_dict['TM'] = fields_sep_by_comma[1]
            if (len(fields_sep_by_comma) > 2):
                return_dict['HM'] = HM[3]

    return return_dict

def collect_number_of_pokemon(xpath):
    time.sleep(random.randint(2, 5))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    fields = element.text.split(" ")
    number_of_pokemon = len(fields) - 3
    for i in range(len(fields)):
        if ("." in fields[i]):
            number_of_pokemon = number_of_pokemon - 1
    return number_of_pokemon

def collect_pokemon_name(xpath):
    time.sleep(random.randint(2, 5))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    return element.text

def collect_pokemon_level(xpath):
    time.sleep(random.randint(2, 5))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    fields = element.text.split(" ")
    return fields[1]

def collect_pokemon_types(xpath):
    time.sleep(random.randint(2, 5))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    link = element.get_attribute("href")
    link = link[:-6]
    link_parts = link.split("/")
    return link_parts[len(link_parts) - 1]

def collect_pokemon_moveset(xpath):
    time.sleep(random.randint(2, 5))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    fields = element.text.split("\n")
    return fields[1:]

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

    region = collect_region('//*[@id="rbar"]/div[6]/ul/li[2]/a')
    region_dict[region] = []

    for i in range(2, 17, 2):

        gym_dict = {}

        gym_dict['Pokemon'] = []
        # xpath = '//*[@id="content"]/main/table/tbody/tr[1]/td/font'
        # //*[@id="content"]/main/table/tbody/tr[3]/td/font
        gym_dict['Gym_Number'] = collect_gym_name('//*[@id="content"]/main/table/tbody/tr[' + str(i - 1) + ']/td/font')

        #print(region_dict)

        gym_dict.update(collect_metadata('//*[@id="content"]/main/table/tbody/tr[' + str(i) + ']/td[1]/p[1]'))

        number_of_pokemon = collect_number_of_pokemon('//*[@id="content"]/main/table/tbody/tr[' + str(i) + ']/td[1]/table/tbody/tr[2]')

        # //*[@id="content"]/main/table/tbody/tr[2]/td[1]/table/tbody/tr[3]/td[2]
        # //*[@id="content"]/main/table/tbody/tr[2]/td[1]/table/tbody/tr[3]/td[3]
        # //*[@id="content"]/main/table/tbody/tr[2]/td[1]/table/tbody/tr[4]/td[1]
        # //*[@id="content"]/main/table/tbody/tr[2]/td[1]/table/tbody/tr[4]/td[2]
        # //*[@id="content"]/main/table/tbody/tr[2]/td[1]/table/tbody/tr[5]/td[1]
        # //*[@id="content"]/main/table/tbody/tr[2]/td[1]/table/tbody/tr[5]/td[2]

        # geodude 1st type
        # //*[@id="content"]/main/table/tbody/tr[2]/td[1]/table/tbody/tr[4]/td[1]/a[1]

        for j in range(number_of_pokemon):

            pokemon_dict = {}
            # //*[@id="content"]/main/table/tbody/tr[2]/td[1]/table/tbody/tr[2]/td[3]/a
            # //*[@id="content"]/main/table/tbody/tr[4]/td[1]/table/tbody/tr[2]/td[2]/a
            # //*[@id="content"]/main/table/tbody/tr[6]/td[1]/table/tbody/tr[2]/td[2]/a
            # //*[@id="content"]/main/table/tbody/tr[6]/td[1]/table/tbody/tr[2]/td[3]/a
            # //*[@id="content"]/main/table/tbody/tr[6]/td[1]/table/tbody/tr[2]/td[4]/a
            # print(number_of_pokemon)
            # print(i)
            # print(j + 2)
            pokemon_dict['Name'] = collect_pokemon_name('//*[@id="content"]/main/table/tbody/tr[' + str(i) + ']/td[1]/table/tbody/tr[2]/td[' + str(j + 2) + ']/a')

            # //*[@id="content"]/main/table/tbody/tr[4]/td[1]/table/tbody/tr[3]/td[2]
            pokemon_dict['Level'] = collect_pokemon_level('//*[@id="content"]/main/table/tbody/tr[' + str(i) + ']/td[1]/table/tbody/tr[3]/td[' + str(j + 2) + ']')

            # //*[@id="content"]/main/table/tbody/tr[2]/td[1]/table/tbody/tr[4]/td[1]/a[1]
            # //*[@id="content"]/main/table/tbody/tr[2]/td[1]/table/tbody/tr[4]/td[1]/a[2]
            # //*[@id="content"]/main/table/tbody/tr[4]/td[1]/table/tbody/tr[4]/td[1]/a
            pokemon_dict['Types'] = []
            
            pokemon_dict['Types'].append(collect_pokemon_types('//*[@id="content"]/main/table/tbody/tr[' + str(i) + ']/td[1]/table/tbody/tr[4]/td[' + str(j + 1) + ']/a'))

            try: 
                pokemon_dict['Types'].append(collect_pokemon_types('//*[@id="content"]/main/table/tbody/tr[' + str(i) + ']/td[1]/table/tbody/tr[4]/td[' + str(j + 1) + ']/a[2]'))
            except:
                pass

            pokemon_dict['Moveset'] = collect_pokemon_moveset('//*[@id="content"]/main/table/tbody/tr[' + str(i) + ']/td[1]/table/tbody/tr[5]/td[' + str(j + 1) + ']')

            gym_dict['Pokemon'].append(pokemon_dict)   

        region_dict[region].append(gym_dict)
        # print(region_dict)
        # element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="rbar"]/div[6]/ul/li[9]/a'))).click()

    json_data = json.dumps(region_dict, indent=2)
    print(json_data)