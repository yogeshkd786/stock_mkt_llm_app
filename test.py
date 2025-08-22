import http.client

conn = http.client.HTTPSConnection("indian-stock-exchange-api2.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "dfcdbfc0a1mshc940c72cfaae5c0p177f37jsncdcf596e2b9b",
    'x-rapidapi-host': "indian-stock-exchange-api2.p.rapidapi.com"
}

conn.request("GET", "/historical_data?stock_name=tcs&period=1m&filter=price", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))