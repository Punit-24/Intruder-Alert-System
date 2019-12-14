import api, time
from boltiot import Bolt
import json,requests

mybolt = Bolt(api.API_KEY, api.DEVICE_ID)

def send_telegram_message(message):
    """Sends message via Telegram"""
    url = "https://api.telegram.org/" + api.TELEGRAM_BOT_ID + "/sendMessage"
    data = {
        "chat_id": api.TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        response = requests.request(
            "POST",
            url,
            params=data
        )
        print("This is the Telegram URL")
        print(url)
        print("This is the Telegram response")
        print(response.text)
        telegram_data = json.loads(response.text)
        return telegram_data["ok"]
    except Exception as e:
        print("An error occurred in sending the alert message via Telegram")
        print(e)
        return False

while True:
    response = mybolt.digitalRead('0')
    data = json.loads(response)
    if data['success'] != 1:
        print("There was an error while retriving the data.")
        print("This is the error:"+data['value'])
        time.sleep(10)
        continue

    print ("This is the value "+data['value'])
    sensor_value=0
    try:
        sensor_value = int(data['value'])
    except e:
        print("There was an error while parsing the response: ",e)
        continue

    try:
        if sensor_value == 1 :
            print ("Security breach detected. Sending a message.")
            message = "Alert!, their is an intruder in your room"
            telegram_status = send_telegram_message(message)
            print ("Current telegram status is" + str(telegram_status))
    except Exception as e:
        print ("Error",e)
    time.sleep(2)