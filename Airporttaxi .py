b#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 10:46:19 2023
potrebne veci:
    najdenie tabulky 
    priradenie dat k neznamim
    spracovanie Google API
    prepocet ceny
    databaza
    priradenie k datumu meno dna
    telegram 
    fartenbuch
    
    

@author: priwi
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

            # DOPLNPVACKY
EMAIL = "info@premium-limo-service.com"
PASS = "Hchbqz4544!"



chrome_driver = ("/home/priwi/chromedriver")

driver = webdriver.Firefox()

driver.get("https://city-airport-taxis.com/provider/login")

# LOG IN ######################################

    # Najdenie pola "USER NAME"
Log_email = driver.find_element(By.ID, "gps_provider_user")

    # Zaslenie neznamej "EMAIL" do pola
Log_email.send_keys(EMAIL)

Log_pass = driver.find_element(By.ID, "gps_provider_paswd")

    # Zaslanie neznamej PASS do pola 
Log_pass.send_keys(PASS)

    # identifikovanie tlacidla SING IN
Login_button = driver.find_element(By.XPATH, "//button[@class='btn btn-book btn-mobile mb' and contains(text(), 'Sign In')]")

    # Jeho potvrdenie 
Login_button.click()
time.sleep(10)

# Hladame Tabulku 

# Najděte tabulku
table = driver.find_element(By.CLASS_NAME, "booking_list")

# Najděte všechny řádky v tabulce
rows = table.find_elements(By.TAG_NAME, "tr")

# Projděte každý řádek a uložte data do proměnných
for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    if len(cells) >= 10:
        ID = cells[0].text
        Pick_up = cells[1].text
        Drop_off = cells[2].text
        Datum_time = cells[3].text
        Preis = cells[5].text
        Status = cells[8].text

        # Najděte hypertextový odkaz ve sloupci 9
        button = cells[10].find_element(By.ID, "btn_edit_booking")
        button.click()
        
        # Najděte tabulku s údaji o rezervaci
        summary_table = driver.find_element(By.CLASS_NAME, "summary")
        
        # Najděte element div pro "Vehicle Type"
        vehicle_type_element = summary_table.find_element(By.XPATH, "//div[span[contains(text(), 'Vehicle Type')]]/strong")
        
        # Získání textu pro Vehicle Type
        vehicle_type = vehicle_type_element.text
        
        # Vytisknutí získaného vozidla
        print("Vehicle Type:", vehicle_type)
        # Zde můžete provádět operace s proměnnými, například tisk
        print("ID:", ID)
        print("Pick_up:", Pick_up)
        print("Drop_off:", Drop_off)
        print("Datum_time:", Datum_time)
        print("Preis:", Preis)
        print("Status:", Status)
        print("--------------") 

        if cena_ok == "OK":
            telegram_message = (
                "<b>AIRPORT_TAXI\n" + str(Datum_time) + "</b> \nSluzba: " + vehicle_type + "\n" + "<b>\nCena: " + Preis + " €\n"+ str(Cena) + 
                " €\nCena Km : " + str(cena_km) + " €\km" + " " + (cena_ok) + "\n<a href='" + cesta_link + "'>" + vzdialenost + " Km" + " / " + cas + "</a> </b>" + "\n" + "<a href='" + start_link + 
                "'>" + Adresa_Vyzdvyhnutia + "</a>\n ---------> \n" + "<a href='" + ciel_link + "'>" + Adresa_Vylozenia + 
                "</a>\n" + source + "\n" + "Order : " + order
                )

        Telegram_mes = ("AIRPORT TAXI\n" + vehicle_type + "\n" + Datum_time + "\n" 
            )
        driver.back()    
    
    
