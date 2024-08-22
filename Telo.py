#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 20 23:09:51 2023
@author: priwi
"""

from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import time
import re
from spravy import kiwi_send_to_telegram
import zapis_citanie_api_databaza
import pocitanie_trasy
import Nadstavenia


def Telo(driver, Posledna_zakazka, Adresa_vyzdvyhnutia, Adresa_vylozenia, old_tab):

    old = set()
    data_list = []

    posledna_zakazka = None

    while True:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("\nHľadám nové objednávky -", current_time, "")
        if posledna_zakazka is not None:
            print(posledna_zakazka)
        time.sleep(30)
        try:
            table = driver.find_element(By.CLASS_NAME, "booking_list")
            rows = table.find_elements(By.TAG_NAME, "tr")
            new_data_list = []

            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) > 9:
                    ID = cells[0].text
                    Pick_up = cells[1].text
                    Drop_off = cells[2].text
                    Datum_time = cells[3].text
                    Preis = cells[5].text
                    Status = cells[8].text
                    
                    print("ID: " + ID)
                    print("Pick up: " + Pick_up)
                    print("Drop off: " + Drop_off)
                    print("Datum a cas: " + Datum_time)
                    print("Preis: " + Preis)
                    print("Status: " + Status)

                    # Najděte hypertextový odkaz ve sloupci 9
                    button = cells[10].find_element(By.ID, "btn_edit_booking")

                    neu_tab = (ID, Pick_up, Drop_off)
                    new_data_list.append(neu_tab)

                    if neu_tab in old:
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print("\nHľadám nové objednávky -", current_time, "")
                        if posledna_zakazka is not None:
                            print(posledna_zakazka)
                
                        time.sleep(10)
                        continue
                    else: 
                        old.add(neu_tab)
                        
                        button.click()
    
                        summary_table = driver.find_element(By.CLASS_NAME, "summary")                    
                        # Najděte element div pro "Vehicle Type"
                        vehicle_type_element = summary_table.find_element(By.XPATH, "//div[span[contains(text(), 'Vehicle Type')]]/strong")
                        client_name_element = summary_table.find_element(By.XPATH, "//div[span[contains(text(), 'Client Name')]]/strong")
                        mobile_phone_element = summary_table.find_element(By.XPATH, "//div[span[contains(text(), 'Mobile Phone')]]/strong")
                        home_phone_element = summary_table.find_element(By.XPATH, "//div[span[contains(text(), 'Mobile Phone')]]/strong")
                        try:
                            fligh_nummber_element = summary_table.find_element(By.XPATH, "//div[span[contains(text(), 'Flight Number')]]/strong")
                        except NoSuchElementException as e:
                            print("aa")
                        # Získání textu pro Vehicle Type
                        sluzba = vehicle_type_element.text
                        client_name = client_name_element.text
                        phone_nummber = mobile_phone_element.text
                        home_phone = home_phone_element.text
                        fligh_nummber = fligh_nummber_element.text
                        driver.back()
                        
                        if phone_nummber == None:
                            phone_nummber = home_phone
                        if phone_nummber == None:
                            phone_nummber = "None"
                        
                        print("Sluzba: " + sluzba)
                        print("Meno Zakaznika: " + client_name)
                        print("Telefonne 1 cislo: " + phone_nummber)
                        print("Telefonne 2 cislo: "  )
                        print("Cislo Letu: " + fligh_nummber)
                        
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print("\nAIRPORT TAXI\nHľadám nové objednávky -", current_time, "")
                        if posledna_zakazka is not None:
                            print(posledna_zakazka)
            
                            time.sleep(10)
                        else:
                            print("Zmena v tabuľke. Vykonávam príslušné akcie.")
                            old.add(neu_tab)
                            
                            # Predefinovanie neznamych "koli naslednemu scriptu"  --- Lenivost neopustaj ma 
                            
                            Adresa_Vyzdvyhnutia = Pick_up
                            Adresa_vylozenia = Drop_off
                                
                            #   Zistovanie konkretnych adries na zaklade google API 
                                # Pouzitie pomocneho scriptu "zapis_citanie_api_databaza.najdi_adresu"
                            id_address, total_address, link, source = zapis_citanie_api_databaza.najdi_adresu(Adresa_Vyzdvyhnutia)
                            Adresa_Vyzdvyhnutia = total_address
                            start_link = link
                            # Kontrola priradenich neznamich 
                                
                            if start_link == None:
                                start_link = ("http://maps.google.com/maps?q=" + Adresa_Vyzdvyhnutia)
                                
                            source_vyzdvyhnutie = source
                            
                            if source_vyzdvyhnutie == None:
                                source_vyzdvyhnutie = ("vstup")
                                
                            # Premenna premmennych na NONE
                            id_address = None
                            total_address = None
                            link = None
                            source = None
                            
                                ##################################################
                                
                            id_address, total_address, link, source = zapis_citanie_api_databaza.najdi_adresu(Adresa_vylozenia)
                            
                            ciel_link = link
                            
                            Adresa_Vylozenia = total_address
                            
                            if Adresa_Vylozenia == None:
                                Adresa_Vylozenia = Adresa_vylozenia
                                ciel_link = link
                                
                            if ciel_link == None:
                                ciel_link = ("http://maps.google.com/maps?q=" + Adresa_Vylozenia)
                                
                            source_vylozenia = source
                            
                            if source_vylozenia == None:
                                source_vylozenia = "vstup"
                                
                            
                            total_address = None
                            link = None
                            source = None
                            
                            if source == None:
                                source = "vstup"
                            ##################################################  Pocitanie trasy        
                            vzdialenost, cas, cesta_link, source = ( 
                                pocitanie_trasy.spracovat_adresy(Adresa_Vyzdvyhnutia, Adresa_Vylozenia, 
                                Nadstavenia.Google_on_api, Nadstavenia.Googleapi)
                                )
                            
                            # Extrahujte hodiny a minúty pomocou regulárneho výrazu
                            try:
                                 vysledok = re.findall(r'\d+', cas)
                                 pocet_prvkov = len(vysledok)
                             
                                 if pocet_prvkov == 1:
                                     minuty = int(vysledok[0])
                                     celkove_minuty = minuty
                                     
                                 else:
                                     hodiny = int(vysledok[0])
                                     minuty = int(vysledok[1])
                                     celkove_minuty = hodiny * 60 + minuty
                             
                                 cas_cesty = celkove_minuty
                                                              
                            except:
                                 cas_cesty = None
                            
                            # sources = source
                            
                            if vzdialenost == None:
                                vzdialenost = "Km"
                                                
                            if cesta_link == None:
                                cesta_link = f"https://www.google.com/maps/dir/?api=1&origin={Adresa_Vyzdvyhnutia}&destination={Adresa_Vylozenia}&travelmode=car"
                                
                            vzdialenost = vzdialenost.replace("KM", "").replace ("Km", "").replace ("km", "").replace("m", "")
                            
                            if vzdialenost > str(0):
                                vzdialenost = float (vzdialenost)
                                cena_km_o = float(Preis)/float(vzdialenost)
                                cena_km = round(cena_km_o, 2)
                                vzdialenost = str(vzdialenost)
                                cas_cesty = str(cas_cesty)
                                
                            if vzdialenost == None or 0:
                                vzdialenost = float(1)
                                cena_km = float(1)
                                
                            #   Potvrdenie ceny nizka / ok    
                                
                            if 1.3 <= float(cena_km):
                                if "Micro" in sluzba:
                                    cena_ok = "OK"
                            else:
                                cena_ok = "NIZKA"    
                            
                            if 1.3 <= float(cena_km):
                                if "Economy" in sluzba:
                                    cena_ok = "OK"
                            else:
                                cena_ok = "NIZKA"
                            
                            if 1.3 <= float(cena_km):
                                if "Comfort" in sluzba:
                                    cena_ok = "OK"
                            else:
                                cena_ok = "NIZKA"
                                
                            if 1.7 <= float(cena_km):
                                if "Business" in sluzba:
                                    cena_ok = "OK"
                            else:
                                cena_ok = "NIZKA"
                                
                            if 1.7 <= float(cena_km):
                                if "Minibus" in sluzba:
                                    cena_ok = "OK"
                            else:
                                cena_ok = "NIZKA"
                                
                            if 1.7 <= float(cena_km):
                                if "Premium Minibus" in sluzba:
                                    cena_ok = "OK"
                            else:
                                cena_ok = "NIZKA"
                                cena_ok_r = float(cena_km) - 1.7
                                cena_ok_r = round(cena_ok_r, 2)
                                cena_ok_r = str(cena_ok_r)
                            
                            cena_percenta = float(Preis) / 0.7
                            cena_percenta = round(cena_percenta, 2)
                            if phone_nummber == None:
                                cislo = home_phone
                            
                                
                            
                            # Vytvorenie tela Telegram spravy     
                            
                            telegram_message = ("<b> AIRPORT TAXI \n" 
                                                + str(Preis) + "€   ;   " + str(cena_km) + "€   ;   </b>" +
                                                "\nAuftrags nummer: " + ID + 
                                                "\n" + Datum_time + 
                                                "\n Dienst: " + sluzba + 
                                                "\nUmsatz: " + str(cena_percenta) + " €" + 
                                                "\nReichweiter: <a href='" + cesta_link + "'>" + str(vzdialenost) + "</a>" +
                                                "\nAbholung: \n   <a href='" + start_link + "'>" + Pick_up + "</a>"
                                                "\n ------- >\n" +
                                                "\n Ziel: \n   <a href='" + ciel_link + "'>" + Drop_off + "</a>" +
                                                "\n<b>Auftrags Daten</b>" +
                                                "\nName:\n   " + client_name +
                                                "\nTelefon nummer:\n   " + phone_nummber +
                                                "\nFlugnummer:\n   " + fligh_nummber
                                                )
                            
                            print (telegram_message)
                            
                            # Odoslanie telegram spravy 
                            
                            kiwi_send_to_telegram(telegram_message)
                            
                            # Vytvorenie tela poslednej zakazky
                            
                            posledna_zakazka = (
                                "Posledna zakazka:\n" + ID + "\n    " + Datum_time + "\n          " + 
                                Adresa_Vyzdvyhnutia + "   -->   " + Adresa_vylozenia + ", " + sluzba + "\n" + str(Preis)
                                )
                            
                            # Anulovanie vsetkych premennych na hodnotu None pre spravny chod programu 
                            
                            Datum_time = None
                            ID = None
                            Adresa_vylozenia = None
                            phone_nummber = None
                            sluzba = None
                            client_cash = None
                            contractor = None
                            my_profit = None
                            Adresa_Vyzdvyhnutia = None
                            Adresa_Vylozenia = None
                            vzdialenost == None
                            client_cash == None
                            contractor == None
                            my_profit == None
                            continue
                        
        
        except StaleElementReferenceException:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("\nHľadám nové objednávky -", current_time, "")
            if posledna_zakazka is not None:
                print(posledna_zakazka)
            time.sleep(5)
            continue  # Pokračovat od začátku smyčky