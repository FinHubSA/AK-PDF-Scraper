    
import pandas as pd

with open('Metadata.json') as inputfile:
    df=pd.read_json(inputfile)

df.to_csv('Metadata.csv')
import pandas as pd
article_url=pd.read_csv('Metadata.csv')['url']
print(article_url)

from temp_storage import storage
import os
directory = storage.getTempStoragePath()

os.chdir(directory)
sorted(os.listdir(directory), key=os.path.getmtime)
os.remove('.DS_Store')
files = sorted(os.listdir(directory), key=os.path.getmtime)
newest = files[-1]
print(newest)

import pickle
import requests
with open('cookies.pkl', 'rb') as f:
    cookie_list = pickle.load(f)  

cookie = {}
for elem in cookie_list:
    cookie[elem["name"]] = elem["value"]

s = requests.Session()
s.cookies = requests.utils.cookiejar_from_dict(cookie)

url = "https://www-google-com.ezproxy.uct.ac.za/recaptcha/api2/payload?p=06AGdBq27Jm0gHPA0B22_y2fNJ80G7NJWCPyNqdtrnCeuOZ5aul51ETQWtwl6Uz-bZdU5PplgCKd6quyIM4YxnuHhpP2RPRRTKh9txxO1ZoDenc5FFBBmAcYMnM3CENMZYpimcqB8sEqnByoeJ2ht6WniW3I61gRrr6VGxyAb8w5OWYIc_fUyjpXRGvf_6YAQflD7fxwPaA5K_&k=6Lf0YjcbAAAAAMwhwSboGTYDUkAfo-nU-TD0aAzx"
def DownloadFile(url):
    local_filename = 'sample.mp3'
    r = s.get(url)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    return None

DownloadFile(url)


import os
from temp_storage import storage

directory=storage.getTempStoragePath()
def latest_download_file():
    #os.chdir(directory)
    #os.remove('.DS_Store')
    files = sorted(os.listdir(directory), key=os.path.getmtime)
    newest = files[-1]
    os.chdir(os.path.dirname(__file__))
    print(newest)
    return newest

latest_download_file()

import time
import random
import os.path
import re
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import pydub
import speech_recognition as sr
from selenium.webdriver.common.keys import Keys
import pickle
import requests

def delay():
    waiting_time = random.randrange(5,10,1)
    time.sleep(waiting_time)

def check_solved(driver,url,url_pending,t_c_accepted):
    try:
        if t_c_accepted==True:
            WebDriverWait(driver,10).until(expected_conditions.element_to_be_clickable((By.XPATH, r".//terms-and-conditions-pharos-button[@data-qa='accept-terms-and-conditions-button']")))
            print("[SUCCESS] ReCAPTCHA successfully solved after the checkbox was clicked")
            success = True
    except:
        delay()
        if os.path.exists(url) == True or os.path.exists(url_pending) == True:
            print("[SUCCESS] ReCAPTCHA successfully solved after the checkbox was clicked")
            success = True
    return success
                       
def recaptcha_solver(driver,url,url_pending,t_c_accepted):

    recaptcha_log=0

    while True:
        recaptcha_log=recaptcha_log+1
        randint=random.randrange(4,8)

        if recaptcha_log>=randint:
            print("[ERR] Too many iterations, restart driver")
            success = False
            break

        try:
            print("trying to find reCAPTCHA")
            delay()
            frames = driver.find_elements(By.TAG_NAME,"iframe")

            recaptcha_control_frame = None
            recaptcha_challenge_frame = None

            for index,frame in enumerate(frames):
                # Find the reCAPTCHA checkbox
                if re.search('reCAPTCHA', frame.get_attribute("title")):
                    recaptcha_control_frame = frame
                    print('recaptcha box located')
                # Find the reCAPTCHA puzzle    
                if re.search('recaptcha challenge expires in two minutes', frame.get_attribute("title")):
                    recaptcha_challenge_frame = frame
                    print('recaptcha puzzle located')

            if not (recaptcha_control_frame or recaptcha_challenge_frame):
                print("[ERR] Unable to find recaptcha.")
                success = False
                break
            
            # switch to checkbox
            delay()
            frames = driver.find_elements(By.TAG_NAME,"iframe")
            driver.switch_to.frame(recaptcha_control_frame)

            # click on checkbox to activate recaptcha
            driver.find_element(By.CLASS_NAME,"recaptcha-checkbox-border").click()
            print("checkbox clicked")
        
        except:
            print("[ERR] IP address might have been blocked for recaptcha.")
            success = False
            break

        try:
            if t_c_accepted==True:
                WebDriverWait(driver,10).until(expected_conditions.element_to_be_clickable((By.XPATH, r".//terms-and-conditions-pharos-button[@data-qa='accept-terms-and-conditions-button']")))
                print("[SUCCESS] ReCAPTCHA successfully solved after the checkbox was clicked")
                success = True
                break
        except:
            delay()
            if os.path.exists(url) == True or os.path.exists(url_pending) == True:
                print("[SUCCESS] ReCAPTCHA successfully solved after the checkbox was clicked")
                success = True
                break
            else:
                try:
                    # switch to recaptcha audio control frame
                    delay()
                    driver.switch_to.default_content()
                    frames = driver.find_elements(By.TAG_NAME,"iframe")
                    driver.switch_to.frame(recaptcha_challenge_frame)

                    # click on audio challenge
                    delay()
                    driver.find_element(By.ID,"recaptcha-audio-button").click()
                    print("Switched to audio control frame")

                    # switch to recaptcha audio challenge frame
                    driver.switch_to.default_content()
                    frames = driver.find_elements(By.TAG_NAME,"iframe")
                    driver.switch_to.frame(recaptcha_challenge_frame)

                    # get the mp3 audio file
                    delay()
                    src = driver.find_element(By.ID,"audio-source").get_attribute("src")
                    print(f"[INFO] Audio src: {src}")

                    path_to_mp3 = os.path.normpath(os.path.join(os.getcwd(), "sample.mp3"))
                    path_to_wav = os.path.normpath(os.path.join(os.getcwd(), "sample.wav"))

                    # download the mp3 audio file from the source
                    with open('cookies.pkl', 'rb') as f:
                        cookie_list = pickle.load(f)

                    cookie = {}
                    for elem in cookie_list:
                        cookie[elem["name"]] = elem["value"]

                    try:
                        s = requests.Session()
                        s.cookies = requests.utils.cookiejar_from_dict(cookie)

                        def DownloadFile(src):
                            local_filename = 'sample.mp3'
                            r = s.get(src)
                            with open(local_filename, 'wb') as f:
                                for chunk in r.iter_content(chunk_size=1024): 
                                    if chunk: # filter out keep-alive new chunks
                                        f.write(chunk)
                            return None

                        DownloadFile(src)

                    except Exception as e:
                        print("[ERR] Could not download audio file")
                        success = False
                        print(e)
                        break

                    # load downloaded mp3 audio file as .wav
                    try:
                        sound = pydub.AudioSegment.from_mp3(path_to_mp3)
                        sound.export(path_to_wav, format="wav")
                        sample_audio = sr.AudioFile(path_to_wav)
                        print("Exported audio file to .wav")
                    except Exception as e:
                        print("[ERR] Failed to convert file as .wav")
                        success = False
                        print(e)
                        break

                    # translate audio to text with google voice recognition
                    delay()
                    r = sr.Recognizer()
                    with sample_audio as source:
                        audio = r.record(source)
                        try:
                            key = r.recognize_google(audio)
                            print(f"[INFO] Recaptcha Passcode: {key}")
                            print("Audio Snippet was recognised")
                        except Exception as e:
                            print("[ERR] reCAPTCHA voice segment is too difficult to solve.")
                            success = False
                            print(e)
                            break

                    # key in results and submit
                    delay()
                    try:
                        driver.find_element(By.ID,"audio-response").send_keys(key.lower())
                        driver.find_element(By.ID,"audio-response").send_keys(Keys.ENTER)
                        time.sleep(5)
                        driver.switch_to.default_content()
                        time.sleep(5)
                        print("Audio snippet submitted")
                    except Exception as e:
                        print("[ERR] IP address might have been blocked for recaptcha.")
                        success = False
                        print(e)
                        break
                except:
                    print("[INFO] Recurring checkbox")
                    continue
    
    print("program stopped")
    return success




    