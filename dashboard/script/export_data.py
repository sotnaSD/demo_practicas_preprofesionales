import sqlite3
import pandas as pd
import re

def quick_crean(text):
    try:
        clean = re.sub("\n[\ \t]+","\n",text)
        clean = re.sub("\n"," ",clean)
        clean = re.sub("\*+","*",clean)
        clean = re.sub("\.+",".",clean)
        clean = re.sub("\_+","-",clean)
        clean = re.sub("\s+"," ",clean)
        clean = re.sub('\"',"",clean)
        clean = clean.lstrip(' ')
        return clean
    except:
        return False
    

con = sqlite3.connect("db.sqlite3")

cur = con.cursor()

data = {"Docs": []}

for row in cur.execute('SELECT descripcion FROM mercadolibre_scraping_productomercadolibre;'):
    if row[0] == " " or row[0] == "":
        continue
    
    clean_texto = quick_crean(row[0])
    if clean_texto  == False or clean_texto ==  " ":
        continue   
    
    data["Docs"].append(clean_texto)
    
for row in cur.execute('SELECT descripcion FROM amazon_productoamazon;'):
    if row[0] == " " or row[0] == "" or row[0] == None:
        continue
    
    clean_texto = quick_crean(row[0])
    if clean_texto  == False or clean_texto ==  " ":
        continue   
    
    data["Docs"].append(clean_texto)
    
for row in cur.execute('SELECT descripcion FROM olx_productoolx;'):
    if row[0] == " " or row[0] == "" or row[0] == None:
        continue
    
    clean_texto = quick_crean(row[0])
    if clean_texto  == False or clean_texto ==  " ":
        continue   
    
    data["Docs"].append(clean_texto) 
         
for row in cur.execute('SELECT tweet FROM twitter_tweet;'):
    if row[0] == " " or row[0] == "" or row[0] == None:
        continue
    
    clean_texto = quick_crean(row[0])
    if clean_texto  == False or clean_texto ==  " ":
        continue   
    
    data["Docs"].append(clean_texto)
    
for row in cur.execute('SELECT comentario FROM pinterest_productopinterestcomentario;'):
    if row[0] == " " or row[0] == "" or row[0] == None:
        continue
    
    clean_texto = quick_crean(row[0])
    if clean_texto  == False or clean_texto ==  " ":
        continue   
    
    data["Docs"].append(clean_texto)
        
df = pd.DataFrame.from_dict(data)


df.to_csv('tesingDocs.csv', index=False)
