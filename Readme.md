# Immowelt - Dataenerfassung und Datenanalyse


#Requirenments:
- BeautifulSoup version: 4.9.3
- Requests version: 2.25.1
- Numpy version: 1.20.1
- Pandas version: 1.3.4
- Seaborn version: 0.11.1
- Folium version: 0.12.1.post1
- Matplotlib version: 3.3.4



#Externe verwendete Datenquellen:
- PLZ-Deutschland.xlsx (https://excel-karte.de/wp-content/uploads/2016/12/Liste-der-PLZ-in-Excel-Karte-Deutschland-Postleitzahlen.xlsx)
- plz-gebiete.shp (https://www.suche-postleitzahl.org/download_files/public/plz-gebiete.shp.zip)
- plz-gebiete.shx
- plz-gebiete.dbf
- Boris NRW/BRW_2022_Polygon.shp (https://ckan.open.nrw.de/dataset/ce127d47-27d1-4f49-a4dc-65cc1dac339e)
- br0200001-Hamburg2022.csv (https://daten-hamburg.de/infrastruktur_bauen_wohnen/bodenrichtwerte/br0200001-Hamburg2022.zip)

# Beschreibung




Privates Projekt, bestehend aus:

Webscraper.py
1) Webscraper, der einen automatisierten Abruf von Wohnungsinseraten der Seite https://www.immowelt.de/ ermöglicht und in einer Pandas-Datenbank als CSV-Datei abspeichert. Als Suchbegriffe können Städtenamen oder ganze Bundesländer verwendet werden. Über einen Loop, der die 16 deutschen Bundesländer abruft, können so sämtliche Wohnungsinserate in Deutschland abgespeichert werden. 

Core.py und Datafunctions.py
2) Datenanreicherung: Der gesammelte Datenbestand wird in core.py um weitere externe Datenquellen ergänzt. Einerseits wird den Datenbankeinträgen über eine API-Abfrage eine eindeutige Punkt-Koordinate zugeordnet. Andererseits wird den Punkt-Koordinaten anschließend ein aktueller marktüblicher Bodenrichtwert aus den BORIS-Datenbanken zugeordnet. 

Analytics.jpny
3) Explorative Datenanalyse bestehend aus: Datenbereinigung, Analyse der zugrundeliegenden Verteilung der wesentlichen Beobachtungsmerkmale (Kaltmiete, Baujahr, etc), Ermittlung von Korrelationen, Visualisierung von Durchschnittswerten auf einer Deutschlandkarte.
Im nächsten Schritt könnten darauf aufbauend können weiterführende Bibliotheken zur Vorhersage von Mietpreisentwicklungen herangezogen werden.



```python
#Nachfolgend ist eine Auflistung der gespeicherten Informationen ersichtlich

import pandas as pd
pd.read_csv("dataframe_immo_2.csv",sep=';',parse_dates=['Datum'], decimal=",",thousands=None,low_memory=False).columns
```




    Index(['Unnamed: 0', 'Datum', 'ID', 'Größe', 'Zimmer', 'Kaltmiete',
           'Nebenkosten', 'Heizkosten', 'Warmmiete', 'Stellplatz', 'Preis/m²',
           'Straße', 'PLZ', 'Kategorie', 'Wohnungslage', 'Bezug',
           'Derzeitige Nutzung', 'Sonstiges', 'Weitere Räume', 'Zustand',
           'Baujahr', 'Böden', 'Fenster', 'Anschlüsse', 'Ausstattung',
           'Warmmiete inkl. Nebenkosten', 'Kaltmiete zzgl. Nebenkosten',
           'Ausblick', 'Serviceleistungen', 'Wellness', 'Sicherheitstechnik',
           'Kaltmiete Verhandlungsbasis',
           'Kaltmiete Mindestpreis, Vermietung gegen Angebot', 'Hausgeld',
           'Street_Loc', 'Preis/m² (Kalt)', 'Preis/m² (Nebenkosten)',
           'Preis/m² (Warm)', 'Energieausweistyp', 'Gebäudetyp',
           'Baujahr laut Energieausweis', 'Effizienzklasse', 'Endenergieverbrauch',
           'Gültigkeit', 'Endenergiebedarf', 'Wesentliche Energieträger',
           'Endenergiebedarf (Wärme)', 'Endenergiebedarf (Strom)',
           'Endenergieverbrauch (Wärme)', 'Endenergieverbrauch (Strom)',
           'Request_Adresse', 'Boris_NRW_ID', 'Stadt', 'BORIS_NRW', 'BRW',
           'BRW-Anteil', 'Kaltmiete inkl. Nebenkosten',
           'Kaltmiete Verhandlungsbasis, zzgl. Nebenkosten',
           'Kaltmiete Mindestpreis, Vermietung gegen Angebot, zzgl. Nebenkosten',
           'Warmmiete Mindestpreis, Vermietung gegen Angebot, inkl. Nebenkosten',
           'Nettomiete Mindestpreis, Vermietung gegen Angebot', 'BORIS_ID',
           'Unnamed: 62', 'Unnamed: 63'],
          dtype='object')




