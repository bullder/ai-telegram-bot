import json
import os
import sys
import re

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "./vendored"))

import requests

TOKEN = os.environ['OPENAI_TOKEN']
BASE_URL = "https://api.telegram.org/bot{}/sendMessage".format(os.environ['TELEGRAM_TOKEN'])


def send(message, chat_id):
    requests.post(
        BASE_URL,
        {
            "text": message,
            "chat_id": chat_id
        }
    )
    print('tg msg is sent')


def openai_img(promt):
    promt = re.sub('^img ', '', promt)

    response = requests.post(
        "https://api.openai.com/v1/images/generations",
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(TOKEN),
        },
        json={
            'prompt': promt,
            'n': 1,
            "size": "1024x1024"
        }
    )
    j = response.json()
    print(j)

    return str(j["data"][0]["url"])


def openai(promt):
    response = requests.post(
        "https://api.openai.com/v1/completions",
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(TOKEN),
        },
        json={
            'model': 'text-davinci-003',
            'prompt': promt,
            'max_tokens': 1024,
            'temperature': 0.9,
        }
    )
    j = response.json()
    print(j)

    return str(j["choices"][0]["text"])


def hello(event, context):
    try:
        print("start handling")
        data = json.loads(event["body"])
        chat_id = data["message"]["chat"]["id"]
        message = str(data["message"]["text"])
        print(message)

        if message == "ping":
            answer = "pong"
        elif message.startswith('img '):
            answer = openai_img(message)
        else:
            answer = openai(message)

        print(answer)
        send(answer, chat_id)
    except Exception as e:
        print(e)

    return {"statusCode": 200}
