import time
import datetime
import requests

last_recieved = 0
while True:
    response = requests.get(
        "http://localhost:5000/messages",
        params={"after": last_recieved}
    )
    if response.status_code == 200:
        messages = response.json()["messages"]
        for mes in messages:
            print(mes["username"], datetime.datetime.fromtimestamp(mes["time"]))
            print(mes["text"])
            print()
            last_recieved = mes["time"]
    time.sleep(1)