import json
import re


import requests
import dotenv
import os


from uuid import uuid4
from dotenv import load_dotenv

load_dotenv()


SESSION_TOKEN = os.getenv("SESSION_TOKEN")
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"

baseApi = "https://chat.openai.com/backend-api"
chatApi = baseApi + "/conversation"

refreshTokenApi = "https://chat.openai.com/api/auth/session"


class ChatGPT:

    def sendMessage(self, message):
        try:
            accessToken = self.refreshToken()
            converstation_id = str(uuid4())
            body = {
                "action": "next",
                "messages": [
                    {
                        "id": str(uuid4()),
                        "role": "user",
                        "content": {
                            "content_type": "text",
                            "parts": [message],
                        }
                    }
                ],
                "model": "text-davinci-002-render",
                "parent_message_id": converstation_id,
            }

            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json",
                'Accept': 'text/event-stream',
                'Referer': 'https://chat.openai.com/chat',
                'Origin': 'https://chat.openai.com',
                "user-agent": USER_AGENT,
            }

            response = requests.post(chatApi, json=body, headers=headers)
            if response.status_code == 200:
                response_text = response.text.replace("data: [DONE]", "")
                data = re.findall(r'data: (.*)', response_text)[-1]
                as_json = json.loads(data)
                return as_json['message']['content']['parts'][0]

        except requests.exceptions.ConnectionError as err:
            print(f"A connection error occurred: {err}")
        except requests.exceptions.HTTPError as err:
            print(f"An HTTP error occurred: {err}")
        except requests.exceptions.Timeout as err:
            print(f"The request timed out: {err}")

    def refreshToken(self):
        try:

            headers = {
                "cookie": f"__Host-next-auth.csrf-token=695052cb72123bec8286a86f7cdd86f344be8aeeca87f12bbe675d8d004bb301%7C7cc53a1dfbe3168406084087b5dc10b7ae44dee712946990934f892b1ad1dfb4; _ga=GA1.2.1120066159.1670229933; intercom-device-id-dgkjq2bp=48aa19af-218c-42a6-91f2-ce52b18beadb; mp_d7d7628de9d5e6160010b84db960a7ee_mixpanel=%7B%22distinct_id%22%3A%20%22user-prt0pzzKiQK36c7LKxe8QuKC%22%2C%22%24device_id%22%3A%20%22184e17050654e-06e7e54958d589-9116d2c-100200-184e170506665%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22%24user_id%22%3A%20%22user-prt0pzzKiQK36c7LKxe8QuKC%22%7D; intercom-session-dgkjq2bp=WUNFRHJwNG05N0hoQ3ZQclJhcVdLc0hHckJOcUVOQmFaZFZwQmxMUFk5amhGMnM4NENGcDBySjBXZHIva00yaC0tSFNGUVcrL1N6bUMxUmc1d0JJT0RxUT09--5ceef2f7a1d15224a387585aaadded84daf8dc67; __Secure-next-auth.callback-url=https%3A%2F%2Fchat.openai.com%2Fchat; __Secure-next-auth.session-token={SESSION_TOKEN}",
                "user-agent": USER_AGENT
            }

            response = requests.get(refreshTokenApi, headers=headers)
            jsonRes = json.loads(response.text)

            accessToken = ""
            if bool(jsonRes):
                accessToken = jsonRes['accessToken']
                dotenv.set_key(".env", "SESSION_TOKEN", accessToken, "never")

            return accessToken or SESSION_TOKEN

        except requests.exceptions.ConnectionError as err:
            print(f"A connection error occurred: {err}")
        except requests.exceptions.HTTPError as err:
            print(f"An HTTP error occurred: {err}")
        except requests.exceptions.Timeout as err:
            print(f"The request timed out: {err}")
