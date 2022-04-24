## PDF scraper to retrieve pdf files from JSTOR and requires a user login

from ast import Not
import json
from pathlib import Path
import time
import os.path
import random
import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

from connection_controllers.gen_connection_controller import GenConnectionController
from recaptcha_solver import recaptcha_solver
from temp_storage import storage

# Set the storage location
directory = storage.createTempStorage()


# Select a random User Agent
USER_AGENT_LIST = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
                ]

USER_AGENT = random.choice(USER_AGENT_LIST)

chrome_options = webdriver.ChromeOptions()

# don't recommend this because this scraper may require some human intervention if it crashes but...
# uncomment below if you dont want the google chrome browser UI to show up.
#chrome_options.add_argument('--headless')

# Add chrome options
curdir = Path.cwd().joinpath("BrowserProfile")
#chrome_options.add_argument("user-data-dir=selenium") #this is supposed to automatically manage cookies but it's not working
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

driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# step 1: retrieve required url from the database --> something like select top(15) DOI, URL from database.[tablename] where [openaccess] = false and [downloaded] = false <--

# for testing I just used the current metadata
metadata = json.load(open("/Users/danaebouwer/Documents/Work/Aarons-kit/Masterlist_Scraper/Metadata.json"))

run=True

while run:
    web_session = GenConnectionController(driver, "https://www.jstor.org")
    current_url = driver.current_url

    for i in metadata:

        # step 2: navigate to URLs of the pdfs and download --> still having issues with the reCAPTCHA <--

        URL = i["URL"]
        DOI = i["objectDOI"]

        # Construct file name
        url = os.path.join(directory,URL.split("/")[-1] + ".pdf")
        doi = os.path.join(directory,DOI.replace("/",".") + ".pdf")

        if not os.path.isfile(doi): #i["Open Access"] == False and

            # Navigate to the pdf page
            driver.get(current_url + "stable/" + URL.split("/")[-1])

            try:
                print('execute ' + DOI)
                WebDriverWait(driver,10).until(expected_conditions.presence_of_element_located((By.ID, "metadata-info-tab")))
            except:
                try: 
                    WebDriverWait(driver,10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "error-message")))
                    print("Article page not loading, possible reCAPTCHA")
                    
                    driver.find_element(By.XPATH, r".//content-viewer-pharos-link[@aria-label='Clicking this link will refresh the page.']").click()
                    print("Calling reCAPTCHA solver")
                    recaptcha_solver(driver)

                    time.sleep(5+random.random()) 

                except:
                    print("Article page not loading, possible reCAPTCHA")
                    print("Calling reCAPTCHA solver")
                    recaptcha_solver(driver)

                    time.sleep(30+random.random())

            #click download
            driver.find_element(by = By.XPATH, value = r".//mfe-download-pharos-button[@data-sc='but click:pdf download']").click()

            # bypass t&c (in some case t&c are different, I need to test to find another case again)
            try:
                WebDriverWait(driver, 10).until(
                    expected_conditions.presence_of_element_located((By.ID, 'content-viewer-container'))
                    ) 
                driver.find_element(by = By.XPATH, value = r".//mfe-download-pharos-button[@data-qa='accept-terms-and-conditions-button']").click()
            except:
                print("no t&c")

            #need to allow time for download to complete and return to initial page
            time.sleep(30+random.random())

            #rename the pdf file to DOI
            storage.renameFile(url,doi)

            # step 3: upload the pdf files to digital ocean after download has been completed

            # step 4: update masterlist to show digital ocean url/url if it is free and true if the article has been uploaded 

        else:
            continue


    # step 5: delete temp storage folder on local computer --> needs work <--
    if storage.countFiles(directory)==15:
        print("deleting downloads")
        storage.deleteTempStorage(directory)
        run = False
        input()
    else:
        # try to handle the error: most likely a reCAPTCHA came up and download could not complete
        print("restart the driver")
        input()
        
        driver.quit

        time.sleep(10+random.random())
        

