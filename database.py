import pandas as pd
import numpy as np

def get_dashboard_data():
    # Idősor generálása 2021 és 2026 között
    dates = pd.date_range(start="2021-01-01", end="2026-05-01", freq="ME")
    n_months = len(dates)
    
    # 1. Brent Olajár (USD)
    brent_prices = [55.0 + (i * 1.2) if i < 15 else 95.0 - ((i-15) * 0.4) for i in range(n_months)]
    brent_prices = [p + np.random.normal(0, 3) for p in brent_prices]
    
    # 2. USD/RON és EUR/RON árfolyamok
    usd_ron = [4.1 + (i * 0.01) + np.random.normal(0, 0.05) for i in range(n_months)]
    eur_ron = [4.9 + (i * 0.002) + np.random.normal(0, 0.01) for i in range(n_months)]
    
    # 3. Romániai üzemanyagárak (RON/liter)
    benzin_prices = [4.8 + (p * 0.035) * (u / 4.2) for p, u in zip(brent_prices, usd_ron)]
    motorina_prices = [p + 0.4 + np.random.normal(0, 0.1) for p in benzin_prices]
    
    # 4. Romániai Inflációs ráta (%)
    inflation_rate = [3.5 + (i * 0.6) if i < 18 else 14.5 - ((i-18) * 0.3) for i in range(n_months)]
    inflation_rate = [max(2.0, inf + np.random.normal(0, 0.5)) for inf in inflation_rate]
    
    # 5. Nettó átlagkereset Romániában (RON) és Vásárlóerő index
    base_salary = 3400
    salary = [base_salary + (i * 45) + np.random.normal(0, 30) for i in range(n_months)]
    purchasing_power = [100 + (i * 0.2) - (inf * 0.5) for i, inf in enumerate(inflation_rate)]

    df = pd.DataFrame({
        'Dátum': dates,
        'Brent_Olaj_USD': brent_prices,
        'USD_RON': usd_ron,
        'EUR_RON': eur_ron,
        'Benzin_RON': benzin_prices,
        'Motorina_RON': motorina_prices,
        'Inflacio_Szazalek': inflation_rate,
        'Netto_Atlagber_RON': salary,
        'Vasarloero_Index': purchasing_power
    })
    
    return df