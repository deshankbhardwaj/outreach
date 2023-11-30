import selenium
import os
import shutil
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.action_chains import ActionChains

df = pd.read_excel("instagram_leads.xlsx")

id = "id_ig"
password = "pass_ig"

base_path = os.path.abspath(os.path.dirname(__file__))
PATH = os.path.join(base_path, 'chromedriver.exe')
driver = webdriver.Chrome(PATH)
actions = ActionChains(driver)

def login():
    url = "https://www.instagram.com/"
    driver.get(url)

    uid_ig = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="loginForm"]/div/div[1]/div/label/input'))
        )
    uid_ig.click()
    uid_ig.send_keys(id)

    pass_ig = driver.find_element(By.XPATH,'//*[@id="loginForm"]/div/div[2]/div/label/input')
    pass_ig.click()
    pass_ig.send_keys(password)

    submit = driver.find_element(By.XPATH,'//*[@id="loginForm"]/div/div[3]/button')
    submit.click()

    time.sleep(30) ## enter the verification code here

def ig_automation(i):
    client_IG_url = df.loc[i,"IG_Url"]
    driver.get(client_IG_url)
    try:
        client_dm = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH,"//div[text()='Message' and @tabindex='0' and @role='button']"))
            )
        
        client_dm.click()
    except:
        print(client_IG_url+" is private.")

    


    try:
        notnow = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH,"//button[text()='Not Now' and @tabindex='0']"))
        )

        notnow.click()

        text_to_type = df.loc[i,"Text_to_type"]
        actions.send_keys(text_to_type)
        actions.send_keys(Keys.RETURN)  # Press Enter key

        # Perform the actions
        actions.perform()

        time.sleep(10)
    except:
        


        text_to_type = df.loc[i,"Text_to_type"]
        actions.send_keys(text_to_type)
        actions.send_keys(Keys.RETURN)  # Press Enter key

        # Perform the actions
        actions.perform()

        time.sleep(10)

#-----------------------------------------------------------Code----------------------------------------------------------------------------#

login()
for i in range(len(df)):
    ig_automation(i)
driver.quit()