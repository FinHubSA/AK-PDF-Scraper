from logging import exception
import time
import pickle
import random
import os.path
import os
import re
from datetime import datetime
import requests
import platform
from termcolor import colored

import pydub
import speech_recognition as sr
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def frame(driver):

    frames = driver.find_elements(By.TAG_NAME, "iframe")

    recaptcha_control_frame = None
    recaptcha_challenge_frame = None

    for index, frame in enumerate(frames):

        # Find the reCAPTCHA checkbox
        if re.search("reCAPTCHA", frame.get_attribute("title")):

            recaptcha_control_frame = frame
            print("recaptcha box located")

        # Find the reCAPTCHA puzzle
        if re.search(
            "recaptcha challenge expires in two minutes", frame.get_attribute("title")
        ):

            recaptcha_challenge_frame = frame
            print("recaptcha puzzle located")

    return recaptcha_control_frame, recaptcha_challenge_frame


def check_solved(driver, url, url_pending, wait):

    try:
        WebDriverWait(driver, wait).until(
            expected_conditions.element_to_be_clickable(
                (
                    By.XPATH,
                    r".//terms-and-conditions-pharos-button[@data-qa='accept-terms-and-conditions-button']",
                )
            )
        )

        print("[SUCCESS] ReCAPTCHA successfully solved")
        solved = True

    except:

        if os.path.exists(url) or os.path.exists(url_pending):

            print("[SUCCESS] ReCAPTCHA successfully solved")
            solved = True

        else:
            solved = False

    return solved


def recaptcha_solver(driver, url, url_pending, wait, misc_directory, jstor_url):

    recaptcha_log = 0

    start_time = None

    is_recaptcha_control_active = True

    print("trying to find reCAPTCHA")
    time.sleep(wait)

    recaptcha_control_frame, recaptcha_challenge_frame = frame(driver)

    if not (recaptcha_control_frame and recaptcha_challenge_frame):

        print("[ERR] Unable to find reCAPTCHA")
        is_recaptcha_control_active = False
        success = False

    while is_recaptcha_control_active:

        recaptcha_log += 1
        randint = random.randrange(3, 5)

        # Make sure that reCAPTCHA does not get stuck in a loop
        if recaptcha_log >= randint:

            print("[ERR] IP address has been blocked by reCAPTCHA, restart browser")

            success = False

            break

        try:
            # switch to checkbox
            # time.sleep(wait)

            # test to make reCAPTCHA solve fail: driver.switch_to.frame(recaptcha_challenge_frame)
            driver.switch_to.default_content()
            driver.switch_to.frame(recaptcha_control_frame)

            # click on checkbox to activate recaptcha TESTING HERE
            driver.find_element(By.CLASS_NAME, "recaptcha-checkbox-border").click()
            print("checkbox clicked")

            start_time = datetime.now().timestamp()

        except:

            print("[ERR] Cannot solve reCAPTCHA checkbox")

            success = False

            break

        if check_solved(driver, url, url_pending, wait):

            success = True

            break

        else:

            is_recaptcha_challenge_active = True

            ##Test here
            switched_to_audio = False
            while is_recaptcha_challenge_active:

                if not switched_to_audio:

                    # Try to click on the button that allows you to do a voice challenge
                    try:

                        driver.switch_to.default_content()
                        driver.switch_to.frame(recaptcha_challenge_frame)

                        time.sleep(random.randrange(10, 15, 1))
                        driver.find_element(By.ID, "recaptcha-audio-button").click()
                        print("Switched to audio control frame")
                        switched_to_audio = True

                    except:

                        print("[INFO] Recurring checkbox")
                        break

                # Get the audio source (the mp3 file)
                try:
                    # switch to recaptcha audio challenge frame
                    driver.switch_to.default_content()
                    driver.switch_to.frame(recaptcha_challenge_frame)

                    # get the mp3 audio file
                    time.sleep(wait)
                    src = driver.find_element(By.ID, "audio-source").get_attribute(
                        "src"
                    )
                    print(f"[INFO] Audio src: {src}")

                except Exception as e:

                    print("[ERR] Error when using Audio challenge frame")
                    print(e)
                    success = False
                    is_recaptcha_control_active = False
                    break

                path_to_mp3 = os.path.normpath(
                    os.path.join(misc_directory, "sample.mp3")
                )
                path_to_wav = os.path.normpath(
                    os.path.join(misc_directory, "sample.wav")
                )

                # download the mp3 audio file from the source
                with open(os.path.join(misc_directory, "cookies.pkl"), "rb") as f:
                    cookie_list = pickle.load(f)

                cookie = {}
                for elem in cookie_list:
                    cookie[elem["name"]] = elem["value"]

                try:
                    s = requests.Session()
                    s.cookies = requests.utils.cookiejar_from_dict(cookie)

                    local_filename = "sample.mp3"
                    r = s.get(src)
                    with open(os.path.join(misc_directory, local_filename), "wb") as f:
                        for chunk in r.iter_content(chunk_size=1024):
                            if chunk:  # filter out keep-alive new chunks
                                f.write(chunk)

                except Exception as e:
                    print("[ERR] Could not download audio file")
                    print(e)
                    success = False
                    is_recaptcha_control_active = False
                    break

                # load downloaded mp3 audio file as .wav
                try:
                    sound = pydub.AudioSegment.from_mp3(path_to_mp3)
                    sound.export(path_to_wav, format="wav")
                    sample_audio = sr.AudioFile(path_to_wav)
                    print("Exported audio file to .wav")
                except Exception as e:

                    print(colored("!" + "   Failed to convert file to .wav", "red"))

                    if platform.system() == "Windows":
                        print(
                            "\nFor installation instructions visit: https://windowsloop.com/install-ffmpeg-windows-10/"
                        )
                    elif platform.system() == "Darwin":
                        print(
                            "\nFor installation instructions visit: https://bbc.github.io/bbcat-orchestration-docs/installation-mac-manual/"
                        )
                    else:
                        print(
                            "\nFor installation instructions visit: https://linuxize.com/post/how-to-install-ffmpeg-on-debian-9/"
                        )

                    driver.get(jstor_url)

                    input(
                        colored("\n-- Once installed, press ")
                        + colored("ENTER/RETURN")
                        + colored(" to continue: ")
                    )

                    success = False
                    is_recaptcha_control_active = False
                    break

                # translate audio to text with google voice recognition
                time.sleep(random.randrange(10, 15, 1))
                r = sr.Recognizer()
                with sample_audio as source:
                    audio = r.record(source)
                    try:
                        key = r.recognize_google(audio)
                        print(f"[INFO] Recaptcha Passcode: {key}")
                        print("Audio Snippet was recognised")
                    except Exception as e:
                        print(
                            "[ERR] reCAPTCHA voice segment is too difficult to solve."
                        )
                        print(e)
                        success = False
                        is_recaptcha_control_active = False
                        break

                    # key in results and submit

                    time.sleep(random.randrange(10, 15, 1))

                    try:
                        driver.find_element(By.ID, "audio-response").send_keys(
                            key.lower()
                        )
                        driver.find_element(By.ID, "audio-response").send_keys(
                            Keys.ENTER
                        )

                        start_time = datetime.now().timestamp()

                        time.sleep(5)
                        driver.switch_to.default_content()
                        time.sleep(5)
                        print("Audio snippet submitted")

                    except Exception as e:

                        print("[ERR] IP address might have been blocked for recaptcha.")
                        print(e)
                        success = False
                        is_recaptcha_control_active = False
                        break

                    # Check if reCAPTCHA has been solved
                    if check_solved(driver, url, url_pending, wait):
                        success = True
                        is_recaptcha_control_active = False
                        break

                    # If it has not been solved, the while loop will run again. NEED TO TEST!!!

    print("program stopped")

    return success, start_time
