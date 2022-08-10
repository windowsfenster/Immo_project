#!/usr/bin/env python
# coding: utf-8

# In[3]:


from Webscraper import extract_data
from Datafunctions import*


# # Funktionsabruf

# In[4]:


#Loop zum Abruf der Scraper-Funktion. Es können einzelne Städte als auch gesamte Bundesländer abgefragt werden


ortsliste1 =["osnabrueck", "duesseldorf", "berlin", "hamburg", "muenchen", 
          "koeln", "essen", "dortmund", "bonn", "stuttgart", "frankfurt-am-main",
           "bremen", "potsdam", "hannover", "bielefeld", "bochum", "dresden", "duisburg",
           "leipzig", "mannheim","nuernberg", "wuppertal"]

ortsliste2=["bl-bayern","bl-baden-wuerttemberg","bremen"]

ortsliste3=["bergkamen"]
            
for ort in ortsliste3:
    try:
        extract_data(ort)
        print("Funktioniert bei", ort)
    except:
        print("Fehler bei", ort)
        


# In[ ]:


#Öffnen des bestehenden dataframes

df = openfile()


# In[ ]:


#Bodenrichtwerte ermitteln

brw_finder("Niedersachsen")


# In[ ]:


#Letzte Einträge mit Punkt-Koordinaten ermitteln

print(f"Last ID with cord entry is: {max(df.loc[~df['Street_Loc'].isna()].index)}")
print(f"Last ID in list is: {max(df.index)}")


# In[ ]:


#Punkt-Koordinaten im Intervallbereich ermitteln

cord_finder(175209,175215,df)


# In[ ]:


#Prüffunktion der Punkt-Koordinaten

cord_checker(df)


# In[ ]:


#Korrekturfunktion der Punkt-Koordinaten

cord_fixer(df)


# In[ ]:


#Speichern des Dataframes

df.to_csv("dataframe_immo_2.csv",sep=';', decimal=",", encoding="utf-8-sig")

