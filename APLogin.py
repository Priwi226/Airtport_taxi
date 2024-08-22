#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 23:32:13 2023

@author: priwi
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import spravy
import os 
import Nadstavenia

user = os.getlogin()

            # DOPLNPVACKY
# EMAIL = "info@premium-limo-service.com"
# PASS = "Hchbqz4544!"



# chrome_driver = ("/home/{user}/selenium/chromedriver")

# driver = webdriver.Firefox()

# driver.get("https://city-airport-taxis.com/provider/login")

# LOG IN ######################################

def log (driver):
    
    try: 
            # Najdenie pola "USER NAME"
        Log_email = driver.find_element(By.ID, "gps_provider_user")
    
            # Zaslenie neznamej "EMAIL" do pola
        Log_email.send_keys(Nadstavenia.MENO)
    
        Log_pass = driver.find_element(By.ID, "gps_provider_paswd")
    
            # Zaslanie neznamej PASS do pola 
        Log_pass.send_keys(Nadstavenia.HESLO)
    
            # identifikovanie tlacidla SING IN
        Login_button = driver.find_element(By.XPATH, "//button[@class='btn btn-book btn-mobile mb' and contains(text(), 'Sign In')]")
    
            # Jeho potvrdenie 
        Login_button.click()
        time.sleep(10)
        
    except NoSuchElementException:
        telegram = ("Airport TAXI\nLogin nieje mozny!!")
        print(telegram)
        spravy.me_send_to_telegram(telegram)
