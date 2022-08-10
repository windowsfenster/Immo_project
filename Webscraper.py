#!/usr/bin/env python
# coding: utf-8

# In[27]:


from bs4 import BeautifulSoup as bs
from datetime import datetime
from datetime import date
import requests
import os
import numpy as np
import unicodedata
import time
import pandas as pd

def extract_data(ort_input):

        #Inner-function zum Anhängen des generierten Dataframes an den bereits bestehenden Dataframe
        def csv_append_func(dataframeobject, filename):
            if os.path.isfile(filename):
                cache_df = pd.read_csv(filename,sep=';', decimal=",", dtype={"Sicherheitstechnik":str, "Hausgeld":str, "Preis/m² (Warm)":float})
                cache_df = cache_df.iloc[: , 1:]
                cache_df = cache_df.append(dataframeobject)
                cache_df.reset_index(inplace=True)
                cache_df.drop(columns="index", inplace=True)
                cache_df.to_csv(filename,sep=';', decimal=",", encoding="utf-8-sig")
                print("Speicherprozess beendet: ",datetime.now())
            else:
                print("Keinen bestehenden Dataframe gefunden: Erstelle neuen Dataframe")
                dataframeobject.to_csv(filename,sep=';', decimal=",", encoding="utf-8-sig")
                print("Speicherprozess beendet: ",datetime.now())

        #Reset der temporären Variablen
        link_list=list()
        link_set=()
        loop1={}
        loop2={}
        loop3={}
        loop4={}
        loop5={}
        loop6={}
        street=""
        plz=""
        liste_loop1=[]
        liste_loop2=[]
        liste_loop3=[]
        liste_loop4=[]
        liste_loop5=[]
        liste_loop6=[]
        liste_loop7=[]
    
        ort = ort_input
    
        #Erstellen einer Liste mit sämtlichen URLs (Inserate Mietwohnungen) für den gewählten Suchort
        url_total = f"https://www.immowelt.de/liste/{ort}/wohnungen/mieten?d=true&sd=DESC&sf=TIMESTAMP&sp=1"
        soup_total = bs(requests.get(url_total).content,"html.parser")
        y_total = int(soup_total.select("h1", class_="MatchNumber-a225f")[0].text.split()[0].replace(".",""))
        print(f"Es wurden insgesamt {y_total} links für {ort} gefunden")
        y_total = int(round(max(1,y_total/20),0))
        print(f"Dies entspricht {y_total} Seiten")
        
        #Loop durch jeden Eintrag der URL-Liste 
        for y in range(y_total):
            url = f"https://www.immowelt.de/liste/{ort}/wohnungen/mieten?d=true&sd=DESC&sf=TIMESTAMP&sp={y}"
            data = requests.get(url)
            soup = bs(data.content,"html.parser")
            link_data = soup.find_all("a")
            for x in link_data:
                link_list.append(x.get("href"))
    
        #Filter by "repsone" and remove duplicates
        link_list = [i for i in link_list if "expose" in i]
        link_list = [i for i in link_list if "projekte" not in i]
        link_set=set(link_list)
        link_list=list(link_list)
    
        #Überprüfung, ob der Dataframe bereits Eintrge zur ID des Inserates beinhaltet
        try:
            exisiting_df = pd.read_csv("dataframe_immo_2_rec.csv",sep=';')
            exisisting = pd.Series(exisiting_df["ID"])
        except:
            exisisting = pd.Series()
        
        #Loop zum Abruf der einzelnen Datenitems    
        for i in range(len(link_list)):
            try:
                #URL-Eintrag überspringen, sofern bereits in Dataframe vorhanden
                if link_list[i].split("/")[-1] in exisisting.values:
                    print(i)
                    print("Schon vorhanden")
                    liste_loop7.append(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                    
                else:
                    print(i)
                    print("Noch nicht vorhanden")
                    liste_loop7.append(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                    data = requests.get(link_list[i])
                    soup = bs(data.content,"html.parser")
                    if (soup.head.find("meta").get("name") is not None) or (soup.head.title.text == "Expose nicht verfügbar"):
                        pass
                    else:
                        expose_data = soup.find_all("div", class_="hardfact ng-star-inserted")
    
    
                        #1 Datenabruf (Keyfacts unter Überschrift: Warmmiete, m², Zimmeranzahl)
                        loop1.update({"Datum":datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
                        loop1.update({"ID":link_list[i].split("/")[-1]})
                        loop1.update({"Größe":expose_data[1].text.split()[0].strip()})
                        loop1.update({"Zimmer":expose_data[2].text.split()[0].strip()})
    
    
                        #2 Datenabruf (Adresse, sofern verfügbar)
                        expose_data = soup.find_all("sd-cell-col", class_="cell__col is-center-v")
                        for x in expose_data:
                            street = (x.find("span").text.strip())
                            plz = (x.find("span").find_next_sibling().text.strip())

                        loop3.update({"Straße":street, "PLZ":plz})
    
    
                        #3 Datenabruf (Preisinformationen aus 1. Tabelle (Stellplatz, Heizkosten, Nebenkosten))
                        expose_data = soup.find_all("sd-cell-row", class_="cell-size-100 cell__row ng-star-inserted")
                        for x in expose_data:
                                a= (x.find("sd-cell-col").text.strip())
                                b= (x.find("sd-cell-col").find_next_sibling().text.strip())
                                b = unicodedata.normalize("NFKD", b)

                                if "Stellplätze" in a or "Stellplatz" in a:
                                    loop2.update({"Stellplatz":b})
                                else:
                                    if "Heizkosten" in a:
                                        loop2.update({"Heizkosten":b})
                                    else:
                                        loop2.update({a:b})
                        #Reset der temporären Variable
                        a=""
                        b=""
    
    
                        #4 Datenabruf (Sonstige Wohnungsinformationen aus 2. Tabelle (Ausstattungsmerkmale))
                        expose_data = soup.find("app-estate-object-informations", id="aImmobilie").find_all("sd-cell", class_="cell ng-star-inserted")
                        for x in expose_data:
                                a= (x.find("p").text.strip())
                                b=(x.find("p").find_next_sibling().text.strip())
                                loop4.update({a:b})
                        #Reset der temporären Variable
                        a=""
                        b=""
    
    
                        #5 Datenabruf (Sonstige Wohnungsinformationen aus 3. Tabelle (Kategorie, Baujahr, Zustand etc.))
                        expose_data = soup.find("app-estate-object-informations", id="aImmobilie").find_all("div", class_="textlist textlist--icon card-content ng-star-inserted")
                        for x in expose_data:
                            for y in x.find_all("li"):
                                cache = y.text.split(":")
                                try: #Fehleranfälliger Abschnitt
                                    if "Stellplatz" in cache[0] or "Stellplätze" in cache[0]:
                                        pass
                                    elif "Stellplatz" in cache or "Stellplätze" in cache:
                                        pass                                
                                    else:
                                        if len(cache)<2:
                                            if "Sonstiges" in loop5.keys():
                                                loop5["Sonstiges"].append(cache[0])
                                            else:
                                                loop5.update({"Sonstiges":[cache[0]]})
                                        else:
                                            loop5.update({cache[0]:cache[1]})
                                except:
                                        pass
                                    
                        #6 Datenabruf (Informationen zum Energieausweis)
                        try:
                            expose_data = soup.find("div",class_="energy_information ng-star-inserted").find_all("sd-cell", class_="cell ng-star-inserted")
                            for x in expose_data:
                                a=(x.find("p").text.strip())
                                b=(x.find("p").find_next_sibling().text.strip())
                                loop6.update({a:b})
    
                            #Weitere Energiedaten (Heizungsart)
                            expose_data = soup.find("div",class_="energy_information ng-star-inserted").find_all("sd-cell", class_="card__cell pb-100 pb-75:400")
                            for x in expose_data:
                                c=(x.find("p").text.strip())
                                d=(x.find("p").find_next_sibling().text.strip())
                                loop6.update({c:d})
                            #Reset der temporären Variable
                            a=""
                            b=""
                            c=""
                            d=""
                        except:
                            pass
                        
                        
                        # Nach jedem URL-Durchlauf: Anhängen des erfolgten Datenabrufs in einer Liste
                        liste_loop1.append(loop1)
                        liste_loop2.append(loop2)
                        liste_loop3.append(loop3)
                        liste_loop4.append(loop4)
                        liste_loop5.append(loop5)
                        liste_loop6.append(loop6)

    
                        # Temporäre Liste leeren vor Beginn der neuen Iteration
                        loop1={}
                        loop2={}
                        loop3={}  
                        loop4={}
                        loop5={}
                        loop6={}
            except:
                         # Temporäre Liste leeren vor Beginn der neuen Iteration
                        loop1={}
                        loop2={}
                        loop3={}  
                        loop4={}
                        loop5={}
                        loop6={}
                        
                        #Download-Log wieder entfernen, sofern fehlerhafter Durchlauf
                        liste_loop7[-1]=None
                        print("Loop fehlerhaft")
    
    
        #Nach Durchlauf aller URL-Einträge: Erstellen des finalen Dataframes
        print("Erstelle Dataframe für Ort")
        
        #Zusammenfassen der einzelnen Speicherlisten zu einem Dataframe mit den neuen Daten ("df_final")
        df_final = pd.concat([pd.DataFrame(liste_loop1),pd.DataFrame(liste_loop2),pd.DataFrame(liste_loop3),pd.DataFrame(liste_loop4),pd.DataFrame(liste_loop5),pd.DataFrame(liste_loop6)], axis = 1)
        
        if df_final.shape[0] == 0:
            print("Keine neue Daten")
            
        else:
            if "Größe" in df_final.columns:
                df_final["Größe"] = pd.to_numeric(df_final["Größe"].apply(lambda x:x.replace(",",".")),errors="coerce")
                df_final["Zimmer"] = pd.to_numeric(df_final["Zimmer"].apply(lambda x: x.replace(",",".")),errors="coerce")
                
                df_final.loc[~df_final["Kaltmiete"].isnull(),"Kaltmiete"] = df_final.loc[~df_final["Kaltmiete"].isnull(),"Kaltmiete"].apply(lambda x: x.replace("€", "").replace(".","").replace(",", ".").replace(" ","").strip())
                df_final["Kaltmiete"] = pd.to_numeric(df_final["Kaltmiete"],errors="coerce")
                
                df_final.loc[~df_final["Nebenkosten"].isnull(),"Nebenkosten"] = df_final.loc[~df_final["Nebenkosten"].isnull(),"Nebenkosten"].apply(lambda x: x.replace("€", "").replace(".","").replace(",", ".").replace(" ","").strip())
                df_final["Nebenkosten"] = pd.to_numeric(df_final["Nebenkosten"],errors="coerce")  
            
    
            #Warmmiete und Stellplatz kann Nan enthalten. Restliche Werte replacen und dann gesamte Series konverten
            if "Warmmiete" in df_final.columns:
                df_final.loc[~df_final["Warmmiete"].isnull(),"Warmmiete"] = df_final.loc[~df_final["Warmmiete"].isnull(),"Warmmiete"].apply(lambda x: x.replace("€", "").replace(".","").replace(",", ".").replace(" ","").strip())
                df_final["Warmmiete"] = pd.to_numeric(df_final["Warmmiete"],errors="coerce")   
            if "Stellplatz" in df_final.columns:
                df_final.loc[~df_final["Stellplatz"].isnull(),"Stellplatz"] = df_final.loc[~df_final["Stellplatz"].isnull(),"Stellplatz"].apply(lambda x: unicodedata.normalize("NFKD", x.replace("€", "")))
            if "Heizkosten" in df_final.columns:
                filter =(df_final["Heizkosten"].str.contains("€", na=False))
                df_final.loc[filter, "Heizkosten"] = df_final.loc[filter,"Heizkosten"].apply(lambda x: x.replace("€", "").replace(".","").replace(",",".")).astype(float)
        
        
        print("Beginne Speicherprozess")
        print(datetime.now())
        
        #Abspeichern der Inserats-ID sowie Abrufdatum in einem zweiten Dataframe ("df_recurring"), um zukünftig sicherzustellen zu können, dass keine Doppelerfassung von Inseraten erfolgt
        link_list=[x.split("/")[-1] for x in link_list]
        df_recurring=pd.concat([pd.DataFrame(link_list), pd.DataFrame(liste_loop7)],axis=1)
        df_recurring.columns = ['ID', 'Zeitpunkt']
        df_recurring.loc[df_recurring["Zeitpunkt"] == None,"ID"]=None

        #Einfügen der beiden neuen Dataframes ("df_final" und "df_recurring") in den bereits bestehenden Dataframe
        csv_append_func(df_final, "dataframe_immo_2.csv")
        csv_append_func(df_recurring, "dataframe_immo_2_rec.csv")


    

