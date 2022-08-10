# Immowelt - Dataenerfassung und Datenanalyse

#Requirements:
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


1) Webscraper (Webscraper.py), der einen automatisierten Abruf von Wohnungsinseraten der Seite https://www.immowelt.de/ ermöglicht und in einer Pandas-Datenbank als CSV-Datei abspeichert. Als Suchbegriffe können Städtenamen oder ganze Bundesländer verwendet werden. Über einen Loop, der die 16 deutschen Bundesländer abruft, können so sämtliche Wohnungsinserate in Deutschland abgespeichert werden. 


2) Datenanreicherung (Datafunctions.py): Der gesammelte Datenbestand wird in core.py um weitere externe Datenquellen ergänzt. Einerseits wird den Datenbankeinträgen über eine API-Abfrage eine eindeutige Punkt-Koordinate zugeordnet. Andererseits wird den Punkt-Koordinaten anschließend ein aktueller marktüblicher Bodenrichtwert aus den BORIS-Datenbanken zugeordnet. 

3) Explorative Datenanalyse (Analytics.ipynb) bestehend aus: Datenbereinigung, Analyse der zugrundeliegenden Verteilung der wesentlichen Beobachtungsmerkmale (Kaltmiete, Baujahr, etc), Ermittlung von Korrelationen, Visualisierung von Durchschnittswerten auf einer Deutschlandkarte. Im nächsten Schritt könnten darauf aufbauend können weiterführende Bibliotheken zur Vorhersage von Mietpreisentwicklungen herangezogen werden.



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




```python
#Dataframe:
pd.set_option("display.max_columns", None)
pd.read_csv("dataframe_immo_2.csv",sep=';',parse_dates=['Datum'], decimal=",",thousands=None,low_memory=False)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Unnamed: 0</th>
      <th>Datum</th>
      <th>ID</th>
      <th>Größe</th>
      <th>Zimmer</th>
      <th>Kaltmiete</th>
      <th>Nebenkosten</th>
      <th>Heizkosten</th>
      <th>Warmmiete</th>
      <th>Stellplatz</th>
      <th>Preis/m²</th>
      <th>Straße</th>
      <th>PLZ</th>
      <th>Kategorie</th>
      <th>Wohnungslage</th>
      <th>Bezug</th>
      <th>Derzeitige Nutzung</th>
      <th>Sonstiges</th>
      <th>Weitere Räume</th>
      <th>Zustand</th>
      <th>Baujahr</th>
      <th>Böden</th>
      <th>Fenster</th>
      <th>Anschlüsse</th>
      <th>Ausstattung</th>
      <th>Warmmiete inkl. Nebenkosten</th>
      <th>Kaltmiete zzgl. Nebenkosten</th>
      <th>Ausblick</th>
      <th>Serviceleistungen</th>
      <th>Wellness</th>
      <th>Sicherheitstechnik</th>
      <th>Kaltmiete Verhandlungsbasis</th>
      <th>Kaltmiete Mindestpreis, Vermietung gegen Angebot</th>
      <th>Hausgeld</th>
      <th>Street_Loc</th>
      <th>Preis/m² (Kalt)</th>
      <th>Preis/m² (Nebenkosten)</th>
      <th>Preis/m² (Warm)</th>
      <th>Energieausweistyp</th>
      <th>Gebäudetyp</th>
      <th>Baujahr laut Energieausweis</th>
      <th>Effizienzklasse</th>
      <th>Endenergieverbrauch</th>
      <th>Gültigkeit</th>
      <th>Endenergiebedarf</th>
      <th>Wesentliche Energieträger</th>
      <th>Endenergiebedarf (Wärme)</th>
      <th>Endenergiebedarf (Strom)</th>
      <th>Endenergieverbrauch (Wärme)</th>
      <th>Endenergieverbrauch (Strom)</th>
      <th>Request_Adresse</th>
      <th>Boris_NRW_ID</th>
      <th>Stadt</th>
      <th>BORIS_NRW</th>
      <th>BRW</th>
      <th>BRW-Anteil</th>
      <th>Kaltmiete inkl. Nebenkosten</th>
      <th>Kaltmiete Verhandlungsbasis, zzgl. Nebenkosten</th>
      <th>Kaltmiete Mindestpreis, Vermietung gegen Angebot, zzgl. Nebenkosten</th>
      <th>Warmmiete Mindestpreis, Vermietung gegen Angebot, inkl. Nebenkosten</th>
      <th>Nettomiete Mindestpreis, Vermietung gegen Angebot</th>
      <th>BORIS_ID</th>
      <th>Unnamed: 62</th>
      <th>Unnamed: 63</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>2022-01-03 23:17:00</td>
      <td>23pfx5q</td>
      <td>78.00</td>
      <td>2.0</td>
      <td>695.00</td>
      <td>65.0</td>
      <td>nicht in Warmmiete enthalten</td>
      <td>695.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Straße nicht freigegeben</td>
      <td>49080</td>
      <td>Etagenwohnung</td>
      <td>2. Geschoss</td>
      <td>01.02.2022</td>
      <td>NaN</td>
      <td>['Bad mit Wanne ']</td>
      <td>Kelleranteil</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>8.91</td>
      <td>0.83</td>
      <td>8.91</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Osnabrück</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>2022-01-03 23:17:00</td>
      <td>23lxm5w</td>
      <td>96.70</td>
      <td>3.5</td>
      <td>725.00</td>
      <td>150.0</td>
      <td>NaN</td>
      <td>725.00</td>
      <td>65.0</td>
      <td>NaN</td>
      <td>Straße nicht freigegeben</td>
      <td>49084</td>
      <td>NaN</td>
      <td>Erdgeschoss</td>
      <td>01.03.2022</td>
      <td>NaN</td>
      <td>['Bad mit Wanne, Gäste-WC ', 'Terrasse ', 'Ein...</td>
      <td>NaN</td>
      <td>renoviert</td>
      <td>1995.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>7.50</td>
      <td>1.55</td>
      <td>7.50</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Osnabrück</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>2022-01-03 23:17:00</td>
      <td>228ze5t</td>
      <td>75.00</td>
      <td>3.0</td>
      <td>750.00</td>
      <td>185.0</td>
      <td>in Nebenkosten enthalten</td>
      <td>750.00</td>
      <td>20.0</td>
      <td>NaN</td>
      <td>Pastor-Goudefroy-Straße 4</td>
      <td>49090</td>
      <td>NaN</td>
      <td>2. Geschoss</td>
      <td>15.02.2022</td>
      <td>NaN</td>
      <td>['Bad mit Fenster und Wanne ', 'Balkon, Garten...</td>
      <td>Kelleranteil</td>
      <td>NaN</td>
      <td>2003.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>(52.2980496, 7.9894613)</td>
      <td>10.00</td>
      <td>2.47</td>
      <td>10.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Germany, 49090, Pastor-Goudefroy-Straße 4</td>
      <td>NaN</td>
      <td>Osnabrück</td>
      <td>NaN</td>
      <td>290.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>2022-01-03 23:17:00</td>
      <td>23bdq5v</td>
      <td>41.00</td>
      <td>1.0</td>
      <td>492.00</td>
      <td>158.0</td>
      <td>in Nebenkosten enthalten</td>
      <td>492.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Roonstrasse  3</td>
      <td>49076</td>
      <td>NaN</td>
      <td>1. Geschoss</td>
      <td>15.01.2022</td>
      <td>NaN</td>
      <td>['Bad mit Fenster ', 'Balkon ', 'Einbauküche ']</td>
      <td>Kelleranteil</td>
      <td>renoviert</td>
      <td>1980.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>(52.2767361, 8.0331353)</td>
      <td>12.00</td>
      <td>3.85</td>
      <td>12.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Germany, 49076, Roonstrasse  3</td>
      <td>NaN</td>
      <td>Osnabrück</td>
      <td>NaN</td>
      <td>640.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>2022-01-03 23:17:00</td>
      <td>23eqn5v</td>
      <td>55.41</td>
      <td>3.0</td>
      <td>528.93</td>
      <td>103.0</td>
      <td>nicht in Warmmiete enthalten</td>
      <td>528.93</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Koksche Str. 84</td>
      <td>49080</td>
      <td>NaN</td>
      <td>Erdgeschoss</td>
      <td>04.03.2022</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1950.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>(52.26276824999999, 8.039480737450504)</td>
      <td>9.55</td>
      <td>1.86</td>
      <td>9.55</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Germany, 49080, Koksche Str. 84</td>
      <td>NaN</td>
      <td>Osnabrück</td>
      <td>NaN</td>
      <td>335.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>291657</th>
      <td>291657</td>
      <td>2022-09-08 22:48:17</td>
      <td>26c4j5q</td>
      <td>120.00</td>
      <td>5.0</td>
      <td>680.00</td>
      <td>150.0</td>
      <td>212.0</td>
      <td>1042.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Jahnstraße 106</td>
      <td>59192 Bergkamen</td>
      <td>Maisonette</td>
      <td>NaN</td>
      <td>15.10.2022</td>
      <td>NaN</td>
      <td>['Bad mit Fenster und Wanne ', 'Balkon ', 'Hau...</td>
      <td>Kelleranteil</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>291658</th>
      <td>291658</td>
      <td>2022-09-08 22:48:17</td>
      <td>26rma5p</td>
      <td>84.88</td>
      <td>3.5</td>
      <td>380.78</td>
      <td>183.0</td>
      <td>109.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Freiherr-vom-Stein-Straße 1A</td>
      <td>59192 Bergkamen  (Oberaden)</td>
      <td>NaN</td>
      <td>Erdgeschoss</td>
      <td>sofort</td>
      <td>NaN</td>
      <td>['Bad mit Fenster und Wanne ', 'Balkon ']</td>
      <td>Kelleranteil</td>
      <td>NaN</td>
      <td>1983</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Verbrauchsausweis</td>
      <td>Wohngebäude</td>
      <td>NaN</td>
      <td>D</td>
      <td>107,00 kWh/(m²·a)  - Warmwasser enthalten</td>
      <td>seit 01.07.2018</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>291659</th>
      <td>291659</td>
      <td>2022-09-08 22:48:17</td>
      <td>26z3x5m</td>
      <td>68.14</td>
      <td>3.5</td>
      <td>457.00</td>
      <td>205.0</td>
      <td>87.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Stormstraße 50E</td>
      <td>59192 Bergkamen  (Oberaden)</td>
      <td>NaN</td>
      <td>Erdgeschoss</td>
      <td>01.11.2022</td>
      <td>NaN</td>
      <td>['Bad mit Fenster und Dusche ', 'Balkon ']</td>
      <td>Kelleranteil</td>
      <td>NaN</td>
      <td>1997</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Bedarfsausweis</td>
      <td>Wohngebäude</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>seit 01.03.2014</td>
      <td>289,00 kWh/(m²·a)</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>291660</th>
      <td>291660</td>
      <td>2022-09-08 22:48:17</td>
      <td>26s8w5m</td>
      <td>62.00</td>
      <td>2.0</td>
      <td>460.00</td>
      <td>200.0</td>
      <td>in Warmmiete enthalten</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Straße nicht freigegeben</td>
      <td>59192 Bergkamen  (Mitte)</td>
      <td>NaN</td>
      <td>Dachgeschoss</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>gepflegt</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>291661</th>
      <td>291661</td>
      <td>2022-09-08 22:48:18</td>
      <td>23xs45y</td>
      <td>80.57</td>
      <td>3.0</td>
      <td>689.00</td>
      <td>125.0</td>
      <td>80.0</td>
      <td>894.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Straße nicht freigegeben</td>
      <td>59192 Bergkamen  (Weddinghofen)</td>
      <td>NaN</td>
      <td>3. Geschoss</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>['Balkon ']</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1969</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Kabelanschluss</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Verbrauchsausweis</td>
      <td>Wohngebäude</td>
      <td>NaN</td>
      <td>E</td>
      <td>137,63 kWh/(m²·a)  - Warmwasser enthalten</td>
      <td>bis 16.09.2028</td>
      <td>NaN</td>
      <td>FERN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>291662 rows × 64 columns</p>
</div>


