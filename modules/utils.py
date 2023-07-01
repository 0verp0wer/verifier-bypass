import json
import base64
import requests

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.192 Safari/537.36"
buildNumber = int(requests.get("https://raw.githubusercontent.com/EffeDiscord/discord-api/main/fetch").json()['client_build_number'])

class Utils:
    def get_token_id(token):
        token_parts = token.split(".")
        user_id = base64.urlsafe_b64decode(token_parts[0] + "==").decode("utf-8")
        return user_id
    
    def GetSuperProperties(buildNumber):
        return base64.b64encode(json.dumps({"os":"Windows","browser":"Chrome","device":"","system_locale":"en-US","browser_user_agent":user_agent,"browser_version":"110.0.5481.192","os_version":"10","referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":buildNumber,"client_event_source":None}).encode()).decode()
    
    def get_headers(token):
        x_properties = Utils.GetSuperProperties(buildNumber)

        cookie = Cookie()
        __dcfduid , __sdcfduid , __cfruid  = cookie.get_cookies(x_properties)

        headers = {
            'Accept': '*\*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
            'Authorization': token,
            'Content-Type': 'application/json',
            'Origin': 'https://discord.com',
            'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'Sec-Ch-Ua-Mobile': '?1,',
            'Sec-Ch-Ua-Platform': '"Android"',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': user_agent,
            'X-Debug-Options': 'bugReporterEnabled',
            'X-Discord-Locale': 'it',
            'X-Discord-Timezone': 'Europe/Rome',
            'X-Super-Properties': x_properties,
            'Cookie': f'__dcfduid={__dcfduid}; __sdcfduid={__sdcfduid}; __cfruid={__cfruid}; locale=it;'
        }
        return headers
    
    def banner():
        banner_value = '''
             __    __)                          ______                       
            (, )  /         ,  /) ,            (, /    )                     
               | /  _  __     //     _  __       /---(       __   _   _   _  
               |/ _(/_/ (__(_/(__(__(/_/ (_   ) / ____) (_/_ /_)_(_(_/_)_/_)_
               |            /)               (_/ (     .-/.-/                
                           (/                         (_/(_/                                                                                
        '''
        return banner_value
    
    
class Cookie:
    @staticmethod
    def get_cookies(x_track):
        cookie_headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
            "Alt-Used": "discord.com",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Host": "discord.com",
            "Origin": "https://discord.com",
            "Referer": "https://discord.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "TE": "trailers",
            "User-Agent": user_agent,
            "X-Track": x_track
        }

        response = requests.get("https://discord.com", headers=cookie_headers)
        __dcfduid = response.cookies.get('__dcfduid') 
        __sdcfduid  = response.cookies.get('__sdcfduid')
        __cfruid = response.cookies.get('__cfruid')

        return (__dcfduid, __sdcfduid, __cfruid)
