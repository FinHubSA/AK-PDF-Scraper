import time
import os.path
import re
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
import sys
import urllib
import pydub
import speech_recognition as sr
from selenium.webdriver.common.keys import Keys
from selenium import webdriver


class recaptcha_solver:

    def __init__(self, driver: webdriver):

        self._driver = driver

        def delay(waiting_time=30):
            driver.implicitly_wait(waiting_time)

        # reCAPTCHA Solver

        checkbox_loop=True

        while checkbox_loop:
            try:
                WebDriverWait(driver,20).until(expected_conditions.presence_of_element_located((By.XPATH, "/html/body/div[4]/div[4]/iframe")))
                frames = driver.find_elements(By.TAG_NAME,"iframe")

                recaptcha_control_frame = None
                recaptcha_challenge_frame = None

                for index, frame in enumerate(frames):
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
                
                # switch to checkbox
                delay()
                frames = driver.find_elements(By.TAG_NAME,"iframe")
                driver.switch_to.frame(recaptcha_control_frame)

                # click on checkbox to activate recaptcha
                driver.find_element(By.CLASS_NAME,"recaptcha-checkbox-border").click()

                print("checkbox clicked")
            
            except:
                print("An error has occured.")
                print("IP address might have been blocked for recaptcha.")
                print("User input required.")
                input()
  
            try:               
                WebDriverWait(driver,20).until(expected_conditions.presence_of_element_located((By.XPATH, r"//div[@data-qa='stable-url']")))
                print("ReCAPTCHA successfully solved after the checkbox was clicked")
                checkbox_loop=False
                count_puzzle_solver=False
            except:      
                try:
                    # switch to recaptcha audio control frame
                    delay()
                    driver.switch_to.default_content()
                    frames = driver.find_elements(By.TAG_NAME,"iframe")
                    driver.switch_to.frame(recaptcha_challenge_frame)

                    # click on audio challenge
                    time.sleep(10)
                    driver.find_element(By.ID,"recaptcha-audio-button").click()
                    print("Switched to audio control frame")
                    
                    checkbox_loop=False
                    count_puzzle_solver=True
                except:
                    continue
        
        while count_puzzle_solver:
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
            urllib.request.urlretrieve(src, path_to_mp3)

            # load downloaded mp3 audio file as .wav
            try:
                sound = pydub.AudioSegment.from_mp3(path_to_mp3)
                sound.export(path_to_wav, format="wav")
                sample_audio = sr.AudioFile(path_to_wav)
                print("Exported audio file to .wav")
            except Exception:
                print(
                    "[ERR] Please run program as administrator or download ffmpeg manually, "
                    "https://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/"
                    )

            # translate audio to text with google voice recognition
            delay()
            r = sr.Recognizer()
            with sample_audio as source:
                audio = r.record(source)
                try:
                    key = r.recognize_google(audio)
                    print(f"[INFO] Recaptcha Passcode: {key}")
                    print("Audio Snippet was recognised")
                except:
                    print("reCAPTCHA voice segment is too difficult to solve.")
                    print("User input required.")
                    input()

            # key in results and submit
            delay()
            try:
                driver.find_element(By.ID,"audio-response").send_keys(key.lower())
                driver.find_element(By.ID,"audio-response").send_keys(Keys.ENTER)
                time.sleep(5)
                driver.switch_to.default_content()
                time.sleep(5)
                print("Audio snippet submitted")
            except:
                print("An error has occured.")
                print("IP address might have been blocked for recaptcha.")
                print("User input required.")
                input()

            count_checkbox_solver=True

            while count_checkbox_solver:
                try:
                    # check to see if reCAPTCHA was solved
                    print("trying to find JSTOR page")
                    WebDriverWait(driver,20).until(expected_conditions.presence_of_element_located((By.XPATH, r"//div[@data-qa='stable-url']")))
                    print("ReCAPTCHA successfully solved")
                    count_checkbox_solver=False
                    count_puzzle_solver=False
                except:
                    try:
                        # check to see if checkbox pops up
                        print("trying to find and solve checkbox")
                        ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
                        WebDriverWait(driver,20,ignored_exceptions=ignored_exceptions).until(expected_conditions.presence_of_element_located((By.XPATH, "/html/body/div[4]/div[4]/iframe")))
                        frames = driver.find_elements(By.TAG_NAME,"iframe")
                        driver.switch_to.frame(recaptcha_control_frame)

                        # click on checkbox to activate recaptcha
                        driver.find_element(By.CLASS_NAME,"recaptcha-checkbox-border").click()
                    except:
                        print("Trying to solve reCAPTCHA puzzle")
                        count_checkbox_solver=False

        

           