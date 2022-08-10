#!/usr/bin/env python
# coding: utf-8

# In[41]:


import pandas as pd
import urllib.parse
import requests
import geopandas as gpd
from bs4 import BeautifulSoup as bs
import requests
import pyproj
import numpy as np
from shapely.geometry import Point, Polygon, mapping
from shapely.ops import transform




# Übersicht Funktionen
# -openfilenfile()
# -cleanfile()
# -cord_finder()
# -cord_checker()
# -cord_fixer()
# -city_finder()
# -brw_finder()

# Notwendige Dateien:
# dataframe_immo_2.csv
# plz-gebiete.shp
# PLZ-Deutschland.xlsx
# Boris NRW/BRW_2022_Polygon.shp
# br0200001-Hamburg2022.csv


# In[4]:


#Funktion, um gespeicherten DataFrame zu öffnen

def openfile():

    df = pd.read_csv("dataframe_immo_2.csv",sep=';',parse_dates=['Datum'], decimal=",",thousands=None,                     dtype={"Preis/m² (Kalt)":"float64",                            "Preis/m² (Nebenkosten)":"float64","Preis/m² (Warm)":"float64",                            "Wohnungslage":"category","Ausstattung":"category",                            "Gebäudetyp":"category", "Kategorie":"category", "Effizienzklasse":"category"}
                    )
    #Grundlegende Datenbereinigung
    df.drop(columns=["Unnamed: 0","Unnamed: 0.1", "Unnamed: 0.2"],errors='ignore', inplace=True)
    df["Größe"] = df["Größe"].astype(str).apply(lambda x:pd.to_numeric(x.replace(",","."),errors="coerce"))
    df["Zimmer"] = df["Zimmer"].astype(str).apply(lambda x:pd.to_numeric(x.replace(",","."),errors="coerce"))

    #PLZ-Datenreihe bereinigen (als string Datentyp)
    df["PLZ"] = df["PLZ"].apply(lambda x: x.split(" ")[0] if isinstance(x, str) else x)
    df["PLZ"] = df["PLZ"].apply(str)
    df["PLZ"] = df["PLZ"].apply(lambda x: x[:5] if len(x)==7 else x)
    df["PLZ"] = df["PLZ"].apply(lambda x: "0"+x[:4] if len(x)==6 else x)

    #Vollständige Adresse zusammensetzen
    df.loc[~df["Straße"].str.contains("Straße nicht freigegeben"),"Request_Adresse"] = "Germany, "+df["PLZ"].apply(lambda x: '{0:0>5}'.format(x))+", "+df["Straße"]

    df["PLZ"] = pd.to_numeric(df["PLZ"],errors='coerce')
    df.loc[df["PLZ"].isna(),"PLZ"] = 0
    df["PLZ"] = df["PLZ"].apply(int)

    pd.set_option("display.max_columns", None)
    return(df)


# In[58]:


#Funktion zur weiteren Bereinigung des Dataframes
def cleanfile(dataframeobject):
    try:
        #Baujahr, BRW bereinigen
        df = dataframeobject
        df["Baujahr"] = df["Baujahr"].apply(str)
        df["Baujahr"] = df["Baujahr"].apply(lambda x: x.replace("/"," ").replace(")","").split()[0])
        df['Baujahr'] = np.floor(pd.to_numeric(df['Baujahr'], errors='coerce')).astype('Int64')

        df["BRW"] = df["BRW"].astype("float64")

        df["Baujahr laut Energieausweis"] = df["Baujahr laut Energieausweis"].apply(lambda x: str(x).replace("/"," ").replace(")","").split()[0])
        df["Baujahr laut Energieausweis"] = pd.to_numeric(df["Baujahr laut Energieausweis"],downcast='integer',errors="coerce").astype("Int64")
    except:
        pass
    return df


# In[65]:


#Funktion zur Ermittlung von Punkt-Koordinaten zu den Inseraten
def cord_finder(minR,maxR,dataframeobject):
    df = dataframeobject

    #Inner-Function zum Aufruf der nominatim-API
    def cord_finder2(adresse):

        address = adresse
        print(address)
        try:
            url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
            response = requests.get(url)
            if response.status_code == 200:
                response = response.json()
                a=""
                b=""
                a =float(response[0]["lat"])
                b =float(response[0]["lon"])
                print(a,b)
                return(a,b)
            else:
                print("nan")
                return np.nan
        except:
            print("nan")
            return np.nan
        
    df.loc[~(df["Request_Adresse"].isnull())&(df["Street_Loc"].isnull())&(df.index>minR)&(df.index<=maxR),"Street_Loc"] = df.loc[~(df["Request_Adresse"].isnull())&(df["Street_Loc"].isnull())&(df.index>minR)&(df.index<=maxR),"Request_Adresse"].apply(lambda x:cord_finder2(x))
    return df


# In[60]:


#Prüffunktion, um sicherzustellen, dass die abgefragten Punkt-Koordinaten innerhalb des PLZ-Bereichs des Inserats liegen
def cord_checker(dataframeobject):
    
    df = dataframeobject
    shapefile1 = 'plz-gebiete.shp'
    shapeDF = gpd.read_file(shapefile1,encoding="utf-8")
    shapeDF.note.dropna(how="any",inplace=True)
    shapeDF.note = shapeDF.note.apply(lambda x:x[6:] if x is not None else x)
    shapeDF.drop_duplicates(subset="plz", inplace=True)

    #Inner-Function
    def cord_checker2(point_input,plz_input):
        print(point_input, plz_input)
        plz_input = '{0:0>5}'.format(plz_input)
        if isinstance(point_input,str):
            point_formatted= (Point(eval(point_input)[1],eval(point_input)[0]))
        else:
            point_formatted= Point(point_input[1],point_input[0])
        try:
            x = (shapeDF.loc[shapeDF["plz"]==plz_input,"geometry"].contains(point_formatted))
            if x.item():
                print(x.item())
                return(point_input)
            else:
                print("Fehler1")
                return("Fehler")
        except:
            print("Fehler2")
            return("Fehler")

    df.loc[~(df["Street_Loc"].isna())&~(df["Street_Loc"]=="Fehler"),"Street_Loc"] = df.loc[~(df["Street_Loc"].isna())&~(df["Street_Loc"]=="Fehler"),["Street_Loc","PLZ"]].apply(lambda x:cord_checker2(x["Street_Loc"], x["PLZ"]), axis=1)
    return df


# In[66]:


#Funktion, um fehlerhafte Punkt-Koordinaten erneut zu laden

def cord_fixer(dataframeobject):
    
    df = dataframeobject
    
    def cord_fixer2(adresse):

        address = adresse
        print(address)
        try:
            url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
            response = requests.get(url)
            if response.status_code == 200:
                response = response.json()
                a=""
                b=""
                a =float(response[0]["lat"])
                b =float(response[0]["lon"])
                print(a,b)
                return(a,b)
            else:
                print("nan")
                return np.nan
        except:
            print("nan")
            return np.nan
    df.loc[~(df["Request_Adresse"].isnull())&(df["Street_Loc"]=="Fehler"),"Street_Loc"] = df.loc[~(df["Request_Adresse"].isnull())&(df["Street_Loc"]=="Fehler"),"Request_Adresse"].apply(lambda x:cord_fixer2(x))
    return df


# In[62]:


#Funktion um PLZ zu Städtenamen zu aggregieren: (Bspw. "Hamburg Alonta" -> "Hamburg")
def city_finder(dataframeobject):
    
    df = dataframeobject
    shapefile1 = 'plz-gebiete.shp'
    shapeDF = gpd.read_file(shapefile1,encoding="utf-8")
    shapeDF.note.dropna(how="any",inplace=True)
    shapeDF.note = shapeDF.note.apply(lambda x:x[6:] if x is not None else x)
    shapeDF.drop_duplicates(subset="plz", inplace=True)
    shapeDF.set_index("plz",inplace=True)
    df["Stadt"] = df["PLZ"].apply(lambda x: '{0:0>5}'.format(x)).map(shapeDF["note"])
    df.loc[[int(str(x).find("Berlin")) > -1 for x in df["Stadt"]],"Stadt"] ="Berlin"
    return df


# In[64]:


#Funktion, um externe Bodenrichtwerte (für NRW, HH und NDS) mit den ermittelten Punkt-Koordinaten zu verknüpfen

#complete = False, wenn lediglich diejenigen Punkt-Koordinaten verknüpft werden sollen, zu denen im Dataframe noch kein BRW abgespeichert wurde 
def brw_finder(BL, dataframeobject, complete = False,):

    df = dataframeobject
    #Hilfsdatei zur Zuordnung von PLZs zu Bundesländern
    Buli = pd.read_excel("PLZ-Deutschland.xlsx",usecols=["PLZ","Bundesland"])
    
    #1. BRW-Quelle für Bundesland Niedersachsen
    if BL =="Niedersachsen":
        
        #Inner-Function zum Abruf anhand der Geobasisdaten-API
        def nds_brw_checker(cords):
            cords = cords.replace("(","").replace(")","")
            coords= cords+","+cords
            coords = coords.replace(" ","")
            req = f"https://www.geobasisdaten.niedersachsen.de/doorman/noauth/WFS_boris?VERSION=2.0.0&SERVICE=WFS&REQUEST=GetFeature&TYPENAMES=boris:BR_BodenrichtwertZonal&BBOX={coords},urn:ogc:def:crs:EPSG::4326"
            print(req)
            soup_total = bs(requests.get(req).content,"html.parser")
            #print(float(soup_total.find_all("boris:bodenrichtwert")[0].text))
            if len(soup_total.find_all("boris:bodenrichtwert"))==0:
                return(np.nan)
            else:
                print(float(soup_total.find_all("boris:bodenrichtwert")[0].text))
                return(float(soup_total.find_all("boris:bodenrichtwert")[0].text))
    #API-Abfrage auf 10 Punkt-Koordinaten begrenzen
        i = 10
        filter = df.loc[(df["PLZ"].isin(Buli.loc[Buli["Bundesland"]=="Niedersachsen","PLZ"]))&(~df["Street_Loc"].isna()&(df["BRW"].isna())),"ID"].iloc[:i].values
        df.loc[df["ID"].isin(filter),"BRW"] = df.loc[df["ID"].isin(filter),"Street_Loc"].apply(nds_brw_checker)

               
    else:
        
    #2. BRW-Quelle für Bundesland NRW

        if BL =="NRW":
            shapefile2 = 'Boris NRW/BRW_2022_Polygon.shp'
            shapeDF2 = gpd.read_file(shapefile2,encoding="utf-8")
            shapeDF2 = shapeDF2[["geometry","BRW"]]

            #Umwandeln der Kooridinaten des POLGYONS
            project = pyproj.Transformer.from_proj(
            pyproj.Proj(init='epsg:25832'), # source coordinate system
            pyproj.Proj(init='epsg:4326')) # destination coordinate system
            shapeDF2["geometry"] = shapeDF2["geometry"].apply(lambda x:transform(project.transform, x))
            shapeDF2["BRW"] = shapeDF2["BRW"].apply(lambda x: x.replace(",",".") if isinstance(x,str) else x).astype("float64")

            BL ="Nordrhein-Westfalen"

    #3. BRW-Quelle Bundesland NRW
    
        elif BL =="Hamburg":
            shapefile2 = "br0200001-Hamburg2022.csv"
            shapeDF2 = pd.read_csv(shapefile2, sep="|")
            shapeDF2 = shapeDF2.loc[shapeDF2["ERGNUTA"]=="MFH",["BRW","KOORWERT"]]
            shapeDF2.reset_index(inplace=True)

            from shapely import wkt
            shapeDF2['KOORWERT'] = shapeDF2['KOORWERT'].apply(wkt.loads)
            shapeDF2.rename(columns={"KOORWERT": "geometry"},inplace=True)
            shapeDF2 = gpd.GeoDataFrame(shapeDF2,crs="EPSG:4647")
            shapeDF2.to_crs(epsg=4326,inplace=True)
        else:
            return

        
        #Grenzen des BRW-Polygons bestimmen, um Zuordnung zu den Punkt-Koordinaten zu vereinfachen
        shapeDF2["geometry2"] = shapeDF2["geometry"].apply(lambda x: [x for x in x.bounds])

        #Vorbereitung: Umwandlung der Punkt-Koordinaten (temporärer Austausch der X- und Y-Koordinaten)
        df.loc[~(df["Street_Loc"].isna())&~(df["Street_Loc"]=="Fehler"),"Street_Loc2"] =df.loc[~(df["Street_Loc"].isna())&~(df["Street_Loc"]=="Fehler"),"Street_Loc"].apply(lambda x:eval(x) if isinstance(x[0],str) else x).apply(lambda x:Point(x[1],x[0]))
                                                           
        #Inner-Function: Prüfung, ob Punkt-Koordinaten innerhalb eines Polygons der Quelldatei liegt
        def brw_checker(point_input):
            print(point_input)
            x= point_input.x
            y= point_input.y
            relevantDF= shapeDF2.loc[(shapeDF2["geometry2"].apply(lambda w:w[0])<=x)&(shapeDF2["geometry2"].apply(lambda w:w[2])>=x)&(shapeDF2["geometry2"].apply(lambda w:w[1])<=y)&(shapeDF2["geometry2"].apply(lambda w:w[3])>=y),"geometry"]
            try:
                return_val = (relevantDF.loc[relevantDF.contains(point_input)].index.values)
                print(return_val)
                if len(return_val) > 1:
                    return(int(max(return_val)))
                elif len(return_val) == 1:
                    return(int(return_val[-1]))
                
                else:
                    return(np.nan)
            except:
                pass


        #Abruf der Inner-Function, in Abhängigkeit der eingegebenen PLZ-Bereichs
        if complete:
            #alle BRWs neu laden
            df.loc[(df["PLZ"].isin(Buli.loc[Buli["Bundesland"]==BL,"PLZ"].values))&(~df["Street_Loc"].isna())&~(df["Street_Loc"]=="Fehler"),"BORIS_ID"]=            df.loc[(df["PLZ"].isin(Buli.loc[Buli["Bundesland"]==BL,"PLZ"].values))&(~df["Street_Loc"].isna())&~(df["Street_Loc"]=="Fehler"),"Street_Loc2"].apply(brw_checker)

        else:
            #nur fehlende BRWs laden
            df.loc[(df["PLZ"].isin(Buli.loc[Buli["Bundesland"]==BL,"PLZ"].values))&(~df["Street_Loc"].isna())&~(df["Street_Loc"]=="Fehler")&(df["BRW"].isnull()),"BORIS_ID"]=            df.loc[(df["PLZ"].isin(Buli.loc[Buli["Bundesland"]==BL,"PLZ"].values))&(~df["Street_Loc"].isna())&~(df["Street_Loc"]=="Fehler")&(df["BRW"].isnull()),"Street_Loc2"].apply(brw_checker)

        #Bereinigungen
        df.drop(columns=("Street_Loc2"), inplace=True,errors='ignore')
        df["BORIS_ID"] = np.floor(pd.to_numeric(df["BORIS_ID"],errors="coerce")).astype("Int64")

        #Zuordnung der Quell-ID mit BRW -> Output: BRW
        cache = shapeDF2[["BRW"]].to_dict()
        df.loc[df["PLZ"].isin(Buli.loc[Buli["Bundesland"]==BL,"PLZ"].values),"BRW"] = df.loc[df["PLZ"].isin(Buli.loc[Buli["Bundesland"]==BL,"PLZ"].values),"BORIS_ID"].map(cache.get("BRW"))
        return df


# In[14]:


df = openfile()


# In[56]:


df.to_csv("dataframe_immo_2.csv",sep=';', decimal=",", encoding="utf-8-sig")

