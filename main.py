import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

get_api = os.getenv("EXCHANGE_API")
url = f"https://v6.exchangerate-api.com/v6/{get_api}/latest/USD"
res = requests.get(url)
try:
    if res.status_code == 200:
        print(res.json())
        file_path = os.path.join("data", "exchange_rate.json")
        with open(file_path, "w") as file:
            json.dump(res.json(), file, indent=4)
    else:
        print(res.status_code)
except Exception as err:
    print(err)


