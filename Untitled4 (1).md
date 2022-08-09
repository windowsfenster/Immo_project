# Immowelt - Dataenerfassung und Datenanalyse


<!-- Requirenments -->
BeautifulSoup version: 4.9.3
Requests version: 2.25.1
Numpy version: 1.20.1
Pandas version: 1.3.4
Seaborn version: 0.11.1
Folium version: 0.12.1.post1
Matplotlib version: 3.3.4



# Beschreibung





```python
Privates Projekt, bestehend aus:
1) Webscraper, der einen automatisierten Abruf von Wohnungsinseraten der Seite https://www.immowelt.de/ ermöglicht und in einer Pandas-Datenbank als CSV-Datei abspeichert. Als Suchbegriffe können Städtenamen oder ganze Bundesländer verwendet werden. Über einen Loop, der die 16 deutschen Bundesländer abruft, können so sämtliche Wohnungsinserate in Deutschland abgespeichert werden. Es 
   

```


      File "<ipython-input-31-a82af6e79651>", line 1
        Privates Projekt, bestehend aus:
                 ^
    SyntaxError: invalid syntax
    



```python
import pandas as pd
pd.read_csv("dataframe_immo_2.csv",sep=';',parse_dates=['Datum'], decimal=",",thousands=None).columns
```

    C:\Users\morit\anaconda3\lib\site-packages\IPython\core\interactiveshell.py:3437: DtypeWarning: Columns (12,31,32,33,34,38,39,40,41,42,43,44,45,46,47,48,49,54,56,57,58,59,60,63) have mixed types.Specify dtype option on import or set low_memory=False.
      exec(code_obj, self.user_global_ns, self.user_ns)
    




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

2) Datenanalysen zum bestehenden Datenbestand. Darauf aufbauend können weiterführende Bibliotheken zur Vorhersage von Mietpreisentwicklungen herangezogen werden.
```

    0.12.1.post1
    1.3.4
    


```python

```
