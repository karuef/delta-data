import requests
import pandas as pd
from datetime import datetime

url = "https://www.deribit.com/api/v2/public/get_book_summary_by_currency"
params = {
    "currency": "BTC",
    "kind": "option"
}
response = requests.get(url, params=params)
data = response.json()["result"]

rows = []
for d in data:
    instrument_name = d['instrument_name']
    mark_price = d['mark_price']
    greeks = d.get('greeks', {})
    if not greeks:
        continue
    delta = greeks.get('delta')
    gamma = greeks.get('gamma')

    if delta is None or gamma is None:
        continue

    parts = instrument_name.split("-")
    if len(parts) >= 3:
        try:
            strike = int(parts[2])
        except:
            continue
        rows.append({
            "strike": strike,
            "delta": delta,
            "gamma": gamma,
            "instrument_name": instrument_name,
            "mark_price": mark_price,
            "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        })

df = pd.DataFrame(rows)
df.to_csv("signals.csv", index=False)
print("signals.csv başarıyla oluşturuldu.")
