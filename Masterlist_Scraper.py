import json
from pathlib import Path
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from datetime import datetime
import os.path
import pandas as pd
import pickle

from recaptcha_solver import recaptcha_solver, delay
from connection_controllers.gen_connection_controller import GenConnectionController
from temp_storage import storage

# Set the storage location
directory = storage.getTempStoragePath()
os.chdir(os.path.dirname(__file__))

# define function to check if download has completed
def latest_download_file():
    os.chdir(directory)
    files = sorted(os.listdir(directory), key=os.path.getmtime)
    newest = files[-1]
    os.chdir(os.path.dirname(__file__))
    return newest
          
while True:

    print("new driver started")

    # need to add code that will choose the right user agent for the person using the code
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'

    chrome_options = webdriver.ChromeOptions()

    # Add chrome options
    curdir = Path.cwd().joinpath("BrowserProfile")
    chrome_options.add_argument(f"user-agent={USER_AGENT}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("prefs", {
    "download.default_directory": directory, #Change default directory for downloads
    "download.prompt_for_download": False, #To auto download the file
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True, #It will not show PDF directly in chrome
    "credentials_enable_service": False, # gets rid of password saver popup
    "profile.password_manager_enabled": False #gets rid of password saver popup
    })

    driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)  

    # navigate to JSTOR page and prompt user to log in
    #if not os.path.exists('cookies.pkl'):

    web_session = GenConnectionController(driver, "https://www.jstor.org")

    # we save the cookies to ensure reCAPTCHA can be solved since login is required to access the mp3 file
    pickle.dump(driver.get_cookies(), open("cookies.pkl","wb"))

    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

    # else:
    #     web_session = driver.get("https://www.jstor.org")

    #     cookies = pickle.load(open("cookies.pkl", "rb"))
    #     for cookie in cookies:
    #         driver.add_cookie(cookie)

    win1 = driver.window_handles[0]
    current_url = driver.current_url
    t_c_accepted = False

    # load input tracker file to specify where the loop should start
    with open("start.json","r") as input_file:
        data = json.load(input_file)
    
    start = data['start']

    # this is temporary. We will need to get data from a database in the future.
    article_url = pd.read_csv('Metadata.csv')['url']

    for article in article_url[start:len(article_url)]:

        # log start time
        start_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        # driver navigates to win2
        driver.execute_script("window.open('" + current_url + "stable/pdf/" + article.split("/")[-1] + ".pdf','_blank')")
        
        # the driver switches between two windows: win1 is the jstor home page and win2 is either the t&c's, recaptcha or download page (which is hidden)
        win2 = driver.window_handles[1]
        driver.switch_to.window(win2)

        # Construct file names
        url = os.path.join(directory,article.split("/")[-1] + ".pdf")
        url_pending = os.path.join(directory,article.split("/")[-1] + ".pdf.crdownload")
        doi = os.path.join(directory,"10.2307." + article.split("/")[-1] + ".pdf")
        
        # The t&c's only pop up the first time you start the driver

        while t_c_accepted!=True:

            restart = False

            # Accept cookies
            try:
                WebDriverWait(driver,5).until(
                    expected_conditions.element_to_be_clickable((By.XPATH, r"//button[@id='onetrust-accept-btn-handler']"))
                    ).click()
                print('cookies accepted')
            except:
                print("no cookies")

            # Accept t&c's
            try:
                WebDriverWait(driver,5).until(
                    expected_conditions.presence_of_element_located((By.XPATH, r".//terms-and-conditions-pharos-button[@data-qa='accept-terms-and-conditions-button']"))
                    ).click()
                print("t&c's accepted")
                t_c_accepted=True
            except:
                # Solve reCAPTCHA                  
                if recaptcha_solver(driver,url,url_pending)==True:
                    print("solved")
                    continue
                else:
                    print("[ERR] reCAPTCHA could not be solved, restart driver")
                    restart = True
                    break
        
        if restart == True:
            break

        # checking for reCAPTCHA
        delay()
        if os.path.exists(url) == True or os.path.exists(url_pending) == True:
            print("No reCAPTCHA")
        else:
            if recaptcha_solver(driver,url,url_pending)==True:
                print("solved")
            else:
                print("[ERR] reCAPTCHA could not be solved, restarting driver")
                break

        # check if file has downloaded - add a max time limit?
        file = url_pending
        #count = 0
        while file == url_pending: #and count <= 60:
            time.sleep(1)
            #count+=1
            newest_file = latest_download_file()
            if newest_file == article.split("/")[-1] + ".pdf":
                file = url
            else:
                file = url_pending

        storage.renameFile(url,doi)

        # log end time
        end_time=datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        # append log file
        with open('scraperlog.txt','a+') as log:
            log.write('\n')
            log.write('\nfor URL: ' + article)
            log.write('\nscraper started at: ' + start_time)
            log.write('\nscraper ended at: ' + end_time)

        # append the tracker file
        start = start+1
        data["start"] = start
        with open("start.json","w") as input_file:
            json.dump(data, input_file)

        try:
            driver.close()
            driver.switch_to.window(win1)
        except:
            driver.switch_to.window(win1)

    driver.quit()
    delay()




