import json
import random
import string
import requests
import websocket

from pystyle import Center, Colors, Colorate, System
from colorama import init, Fore
from modules.solver import *
from modules.utils import *

init()

banner = Utils.banner()
print(Colorate.Diagonal(Colors.blue_to_purple, Center.XCenter(banner)))
System.Title("Verifier Bypass by over_on_top")

channel_id = input('['+ Fore.BLUE + '>' + Fore.RESET + ']' + 'Input the channel id:')
guild_id = input('['+ Fore.BLUE + '>' + Fore.RESET + ']' + 'Input the guild id:')
button_id = input('['+ Fore.BLUE + '>' + Fore.RESET + ']' + 'Input the button id:')
print("\n")

def connect(ws):
  ws.connect('wss://gateway.discord.gg/?encoding=json&v=9&compress=json')
  ws.send(
    json.dumps(
      {
        "op":2,
        "d":{
          "token":token,
          "capabilities":8189,
          "properties":
          {
            "os":"Windows",
            "browser":"Chrome",
            "device":"",
            "system_locale":"it-IT",
            "browser_user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "browser_version":"114.0.0.0",
            "os_version":"10",
            "referrer":"",
            "referring_domain":"",
            "referrer_current":"",
            "referring_domain_current":"",
            "release_channel":"stable",
            "client_build_number":201332,
            "client_event_source":None},
            "presence":
            {
              "status":"online",
              "since":0,
              "activities":[],
              "afk":False
            },
            "compress":False,
            "client_state":
            {
              "guild_versions":{},
              "highest_last_message_id":"0",
              "read_state_version":0,
              "user_guild_settings_version":-1,
              "user_settings_version":-1,
              "private_channels_version":"0",
              "api_code_version":0
            }
          }
        }
      )
    )
  
with open("tokens.txt", "r") as f:
  tokens = f.readlines()
  for i in tokens:
    token = i.rstrip()

    token_id = Utils.get_token_id(token) #get the token id
    headers = Utils.get_headers(token) #get headers

    ws = websocket.WebSocket()
    connect(ws) #connect to the websocket

    print('['+ Fore.GREEN + '+' + Fore.RESET + ']' + 'Button clicked succesfully')
    print('['+ Fore.BLUE + '>' + Fore.RESET + ']' + 'Getting captcha...')

    r = requests.post("https://discord.com/api/v9/interactions", headers=headers, json={"type": 3, "nonce":"".join([str(random.randint(1, 9)) for _ in range(19)]), "guild_id": guild_id, "channel_id": channel_id, "message_flags":"0", "message_id":button_id, "application_id":"792081366862790687","session_id":"".join(random.choice(string.ascii_letters + string.digits) for _ in range(32)), "data":{"component_type":2,"custom_id": f"captchaSystem_{guild_id}_captcha"}})

    while True:
      response = json.loads(ws.recv())
      if response['t'] == 'MESSAGE_CREATE':
        try:
          description = response['d']['embeds'][0]['description']
          if "In order to gain access to the server you must" in description:
            message_id = response['d']['id'] #get new message id
            captcha_url = response['d']['embeds'][0]['image']['url'] #get the captcha link
            ws.close() #close the websocket
            break
        except:
          continue

    print('['+ Fore.GREEN + '+' + Fore.RESET + ']' + 'Captcha obtained correctly')
    connect(ws)
    r = requests.post("https://discord.com/api/v9/interactions", headers=headers, json={"type":3,"nonce":"".join([str(random.randint(1, 9)) for _ in range(19)]),"guild_id":guild_id,"channel_id":channel_id,"message_flags":"64","message_id":message_id,"application_id":"792081366862790687","session_id":"".join(random.choice(string.ascii_letters + string.digits) for _ in range(32)),"data":{"component_type":2,"custom_id":f"captchaSystemTextModalStarter_{token_id}"}})
    while True:
      response = json.loads(ws.recv())
      if response['t'] == 'INTERACTION_SUCCESS':
        id_value = response['d']['id'] #get another message id
        ws.close()
        break
      
    captcha = CaptchaSolver.solve_captcha(captcha_url, "929ea8") #solve the captcha
    r = requests.post("https://discord.com/api/v9/interactions", headers=headers, json={"type":5,"application_id":"792081366862790687","channel_id":channel_id,"guild_id":guild_id,"data":{"id":id_value,"custom_id":f"captchaTextModalSubmit_{token_id}","components":[{"type":1,"components":[{"type":4,"custom_id":"captcha_code","value":captcha}]}]},"session_id":"".join(random.choice(string.ascii_letters + string.digits) for _ in range(32)),"nonce":"".join([str(random.randint(1, 9)) for _ in range(19)])})