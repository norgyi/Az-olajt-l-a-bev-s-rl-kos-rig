import yfinance as yf
import pandas as pd
import numpy as np

def get_dashboard_data():
    tickers = ["BZ=F", "USDRON=X", "EURRON=X"]
    
    # Valós piaci adatok letöltése a Yahoo Finance-ről
    raw_data = yf.download(tickers, start="2021-01-01")
    
    # Biztonságos oszlopkiválasztás (a yfinance gyakran MultiIndexet ad vissza)
    if isinstance(raw_data.columns, pd.MultiIndex):
        data = raw_data['Close'].copy()
    else:
        data = raw_data.copy()
        
    # Átnevezzük az oszlopokat a mi neveinkre
    data = data.rename(columns={"BZ=F": "Brent_Olaj_USD", "USDRON=X": "USD_RON", "EURRON=X": "EUR_RON"})
    
    # Dátumok és hiányzó adatok kezelése (Modern Pandas 2.0+ szintaxis)
    data = data.resample('ME').mean() 
    data = data.bfill().ffill() # Először visszafelé, majd előrefelé tölti ki a lyukakat a hibátlan grafikonért
    
    # Infláció és Bér adatok (trendszimuláció a valós INSSE adatok mintájára)
    n = len(data)
    data['Inflacio_Szazalek'] = [3.0 + (i*0.2) + np.random.normal(0, 0.5) for i in range(n)]
    data['Netto_Atlagber_RON'] = [3500 + (i * 50) + np.random.normal(0, 50) for i in range(n)]
    data['Vasarloero_Index'] = [100 - (inf * 0.3) for inf in data['Inflacio_Szazalek']]
    
    # Index reset és a 'Dátum' oszlop biztosítása
    data = data.reset_index()
    if 'Date' in data.columns:
        data = data.rename(columns={'Date': 'Dátum'})
    elif 'index' in data.columns:
        data = data.rename(columns={'index': 'Dátum'})
        
    # Üzemanyagárak számítása a valós Brent és Deviza adatokból (korreláció)
    data['Benzin_RON'] = (data['Brent_Olaj_USD'] * 0.05) + (data['USD_RON'] * 0.5) + np.random.normal(0, 0.1, n)
    data['Motorina_RON'] = data['Benzin_RON'] + 0.3
    
    return data
