from gtts import gTTS
import speech_recognition as sr
from pygame import mixer
import random
from tabulate import tabulate
import re
from pyowm import OWM
import webbrowser
import os
import smtplib
import time
from time import ctime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as soup
import numpy as np
import subprocess
import requests
import urllib.request #used to make requests
import urllib.parse #used to parse values into the url
from urllib.request import urlretrieve
from urllib.request import urlopen
from prettytable import PrettyTable
import pandas as pd
import matplotlib.pyplot as plt
from googlesearch import search
import ctypes
import psutil
import json

def talk(audio):
    print(audio)
    for line in audio.splitlines():
        text_to_speech = gTTS(text=audio, lang='en-uk')
        text_to_speech.save('audio.mp3')
       # text_to_speech.save('copy.mp3')
        mixer.init()
        mixer.music.load("audio.mp3")
        mixer.music.play()
        while mixer.music.get_busy(): 
            pass
        mixer.music.load("copy.mp3")
        os.remove("audio.mp3")
        
def myCommand():
    #Initialize the recognizer 
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Jarvis is Ready...')
        r.pause_threshold = 1
    
        r.adjust_for_ambient_noise(source, duration=1)
        
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')

    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('Your last command couldn\'t be heard')
        command = myCommand();

    return command

def jarvis(command):
    errors=[
        "I don\'t know what you mean!",
        "Excuse me?",
        "Can you repeat it please?",
    ]

    if 'hi' in command:
        talk('Hello! I am Jarvis. How can I help you?')
    if 'open google' in command:
    
        reg_ex = re.search('open google (.*)', command)
        url = 'https://www.google.com/'
        if reg_ex:
            subgoogle = reg_ex.group(1)
            url = url + 'r/' + subgoogle
        webbrowser.open(url)
        print('Done!')

   
    if 'wikipedia' in command:
        reg_ex = re.search('search in wikipedia (.+)', command)
        if reg_ex: 
            query = command.split()
            response = requests.get("https://en.wikipedia.org/wiki/" + query[3])

            if response is not None:
                html = BeautifulSoup(response.text, 'html.parser')
                title = html.select("#firstHeading")[0].text
                paragraphs = html.select("p")
                for para in paragraphs:
                    print (para.text)


                intro = '\n'.join([ para.text for para in paragraphs[0:5]])
                print (intro)
              

    elif 'youtube' in command:
        talk('Ok!')
        reg_ex = re.search('youtube (.+)', command)
        if reg_ex:
            domain = command.split("youtube",1)[1] 
            query_string = urllib.parse.urlencode({"search_query" : domain})
            html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string) 
            search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode()) # finds all links in search result
            webbrowser.open("http://www.youtube.com/watch?v={}".format(search_results[0]))
            pass


    elif 'what time is it' in command:
        talk(ctime())


   

    elif 'current weather in'  in command:
     reg_ex = re.search('current weather in (.*)', command)
     if reg_ex:
         city = reg_ex.group(1)
         owm = OWM(API_key='ab0d5e80e8dafb2cb81fa9e82431c1fa')
         obs = owm.weather_at_place(city)
         w = obs.get_weather()
         k = w.get_status()
         x = w.get_temperature(unit='celsius')
         talk('Current weather in %s is %s. The maximum temperature is %0.2f and the minimum temperature is %0.2f degree celcius' % (city, k, x['temp_max'], x['temp_min']))
         


                
    elif 'covid-19 news' in command:
        extract_contents = lambda row: [x.text.replace('\n', '') for x in row] 
        URL = 'https://www.mohfw.gov.in/'
	
        SHORT_HEADERS = ['SNo', 'State','Indian-Confirmed(Including Foreign Confirmed)','Cured','Death'] 
	
        response = requests.get(URL).content 
        soup = BeautifulSoup(response, 'html.parser') 
        header = extract_contents(soup.tr.find_all('th')) 

        stats = [] 
        all_rows = soup.find_all('tr') 

        for row in all_rows: 
            stat = extract_contents(row.find_all('td')) 
	
            if stat: 
                if len(stat) == 4: 
			# last row 
                   # stat = ['', *stat] 
                    stats.append(stat) 
                elif len(stat) == 5: 
                    stats.append(stat) 

        stats[-1][0] = len(stats) 
        stats[-1][1] = "Total Cases"



        objects = [] 
        for row in stats : 
            objects.append(row[1]) 
	
        y_pos = np.arange(len(objects)) 

        performance = [] 
        for row in stats[:len(stats)-1] : 
            performance.append(int(row[2])) 

        performance.append(int(stats[-1][2][:len(stats[-1][2])-1])) 

        table = tabulate(stats, headers=SHORT_HEADERS) 
        print(table) 


    if 'download image' in command:
          
        folder = 'C:/Users/MMD/Desktop/vap/wallpapers'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        api_key = 'fd66364c0ad9e0f8aabe54ec3cfbed0a947f3f4014ce3b841bf2ff6e20948795'
        url = 'https://api.unsplash.com/photos/random?client_id=' + api_key #pic from unspalsh.com
        f = urllib.request.urlopen(url)
        json_string = f.read()
        f.close()
        parsed_json = json.loads(json_string)
        photo = parsed_json['urls']['full']
        urllib.request.urlretrieve(photo, "C:/Users/MMD/Desktop/vap/wallpapers/a") # Location where we download the image to.
        subprocess.call(["killall Dock"], shell=True)
        talk('downloaded')

    elif 'battery' in command:
        battery = psutil.sensors_battery()
        plugged = battery.power_plugged
        percent = str(battery.percent)
        if plugged==False:
            plugged="Not Plugged In"
        else:
            plugged="Plugged In"
            talk(percent+'% | '+plugged)

    elif 'play music' in command:
       
        if True:
            music_folder = "C:/Users/MMD/Desktop/musictest"
            music = os.listdir(music_folder)
            random_music = music_folder+'/'+random.choice(music)
            
            if 'stop' not in command:
                mixer.init() 
                mixer.music.load(random_music)
                mixer.music.play()
            
    elif 'stop' in command:

        mixer.music.stop()
            
            
     

    

    elif "goodbye" in command:
        exit()


        

    else:
        error = random.choice(errors)
        talk(error)


talk('JARVIS is ready!')

    


while True:
    jarvis(myCommand())
