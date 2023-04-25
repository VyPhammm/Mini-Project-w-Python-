from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from user import USERNAME, PASSWORD, PHONE
from time import sleep


URL= "https://www.linkedin.com/jobs/search/?f_LF=f_AL&geoId=102257491&keywords=python%20developer&location=London%2C%20England%2C%20United%20Kingdom&redirect=false&position=1&pageNum=0"
chrome_driver_path= r"D:/Development/chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
service = Service(executable_path=chrome_driver_path) 
driver = webdriver.Chrome(options= options, service=service) 

web= "https://www.linkedin.com/login"
driver.get(web)
sleep(5)

email_field = driver.find_element('id','username')
email_field.send_keys(USERNAME)
print('- Finish keying in email')
sleep(3)
password_field = driver.find_element('id','password')
password_field.send_keys(PASSWORD)
print('- Finish keying in password')
sleep(5)

password_field.send_keys(Keys.ENTER)
print('- Finish Task 1: Login to Linkedin')
sleep(10)

driver.get(URL)
#ember184 > div > div.job-card-container.relative.job-card-list.job-card-container--clickable.job-card-list--underline-title-on-hover.jobs-search-results-list__list-item--active.jobs-search-two-pane__job-card-container--viewport-tracking-0
all_listings = driver.find_elements(By.CSS_SELECTOR,".job-card-container--clickable")

for listing in all_listings:
    print("called")
    listing.click()
    sleep(5)

    #Try to locate the apply button, if can't locate then skip the job.
    try:
        apply_button = driver.find_element(By.CSS_SELECTOR,".jobs-s-apply button")
        apply_button.click()
        sleep(5)
        
        #If phone field is empty, then fill your phone number.
        phone = driver.find_element(By.CLASS_NAME,"fb-single-line-text__input")
        if phone.text == "":
            phone.send_keys(PHONE)

        submit_button = driver.find_element(By.CSS_SELECTOR,"footer button")

        #If the submit_button is a "Next" button, then this is a multi-step application, so skip.
        if submit_button.get_attribute("data-control-name") == "continue_unify":
            close_button = driver.find_element(By.CLASS_NAME,"artdeco-modal__dismiss")
            close_button.click()
            time.sleep(2)
            discard_button = driver.find_elements(By.CLASS_NAME,"artdeco-modal__confirm-dialog-btn")[1]
            discard_button.click()
            print("Complex application, skipped.")
            continue
        else:
            submit_button.click()
    
        #Once application completed, close the pop-up window.
        sleep(2)
        close_button = driver.find_element(By.NAME,"artdeco-modal__dismiss")
        close_button.click()

    #If already applied to job or job is no longer accepting applications, then skip.
    except NoSuchElementException:
        print("No application button, skipped.")
        continue

sleep(10)
driver.quit()

