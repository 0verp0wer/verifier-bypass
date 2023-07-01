import os
import time
import torch
import requests

from PIL import Image
from colorama import init,Fore

init()

def clear_screen(): #clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

def load_model(): # Load the model from the path specified
    clear_screen()
    print('['+ Fore.BLUE + '>' + Fore.RESET + ']' + 'Loading model...')
    start_time = time.time()
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='model/captcha.pt', force_reload=True)
    end_time = time.time()
    clear_screen()
    print('['+ Fore.GREEN + '+' + Fore.RESET + ']' + f'Model loaded succesfully in {end_time-start_time} seconds \n')
    return model

class CaptchaSolver:
    
    model = load_model()

    def process_image(img, hex_color, tolerance=20): #This function is used to process the image and remove the background color of the captcha
        image_data = img.load()
        width, height = img.size
        r, g, b = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        r_min, r_max = max(0, r - tolerance), min(255, r + tolerance)
        g_min, g_max = max(0, g - tolerance), min(255, g + tolerance)
        b_min, b_max = max(0, b - tolerance), min(255, b + tolerance)
        for y in range(height):
            for x in range(width):
                try:
                    pixel_r, pixel_g, pixel_b, _ = image_data[x, y]
                except ValueError:
                    pixel_r, pixel_g, pixel_b = image_data[x, y]
                if not (r_min <= pixel_r <= r_max and g_min <= pixel_g <= g_max and b_min <= pixel_b <= b_max):
                    image_data[x, y] = 0, 0, 0, 0
        return img
    
    def solve_captcha(url, color): #This function is used to solve the captcha from the url provided and return the captcha text as a string
        print('['+ Fore.BLUE + '>' + Fore.RESET + ']' + 'Solving the captcha...')
        start_time = time.time()
        img = Image.open(requests.get(url, stream=True).raw)
        img =  CaptchaSolver.process_image(img, color)
        model = CaptchaSolver.model
        result = model(img) #use the model for solve the captcha
        a = result.pandas().xyxy[0].sort_values('xmin')
        while len(a) > 6:
            lines = a.confidence
            linev = min(a.confidence)
            for line in lines.keys():
                if lines[line] == linev:
                    a = a.drop(line)
        captcha_text = ""
        for _, key in a.name.items():
            captcha_text += key
        end_time = time.time()
        print('['+ Fore.GREEN + '+' + Fore.RESET + ']' + f'Captcha solved successfully in {end_time-start_time} seconds: {captcha_text}')
        return captcha_text