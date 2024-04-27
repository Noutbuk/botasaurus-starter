import time
from botasaurus import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@browser
def scrape_heading_task(driver: AntiDetectDriver, data):
    status = 200
    info = "success"
    driver.get(data["link"])

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "cmpwrapper")))
    cookie_button = WebDriverWait(driver, 5).until(EC.visibility_of((driver.execute_script(
        "return document.getElementById('cmpwrapper').shadowRoot.getElementById('cmpbox').querySelector('a.cmpboxbtnyes')"))))
    cookie_button.click()

    time.sleep(2)
    driver.save_screenshot("cookie_screenshot.png")
    return after_cookies(driver, data, status, info, 1)

def after_cookies(driver, data, status, info, max_tries):
    if max_tries < 0:   
        return {
            "page_source": driver.page_source,
            "url": driver.current_url,
            "cookies": driver.get_cookies(),
            "status": status,
            "info": info,
            "max_tries": max_tries,
        }

    wait = WebDriverWait(driver, 5)

    hidden_modal = None
    try:
        hidden_modal = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR,
            "div.P24BotProtectionModal.hidden"
        )))
    except:
        driver.save_screenshot(f"{max_tries}_first_check_screenshot.png")
        status = 500
        info = "Bot protection modal not hidden on first check"

    if hidden_modal:
        info = "success, modal was hidden from the beginning"
    else:
        # span.js-BotProtectionCardText1 -> click button
        potection_text_one = None
        try:
            potection_text_one = driver.find_element(By.XPATH, "//span[contains(@class, 'js-BotProtectionCardText1') and not(contains(@class, 'hidden'))]")

            protection_button = None
            try:
                protection_button = driver.find_element(By.XPATH, "//button[contains(@class, 'BotProtectionCard-Button') and not(contains(@class, 'hidden'))]")
            except:
                protection_button = None

            if protection_button:
                print("click button")
                protection_button.click()
        except:
            potection_text_one = None

        # span.js-BotProtectionCardText2 -> visit other page
        protection_text_two = None
        try:
            protection_text_two = driver.find_element(By.XPATH, "//span[contains(@class, 'js-BotProtectionCardText2') and not(contains(@class, 'hidden'))]")
        except:
            protection_text_two = None

        if protection_text_two:
            # switch to artist page
            driver.get(data["link"].rsplit('/', 1)[0])
            
            #id="artistName"
            try:
                headline = wait.until(EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    "h1#artistName"
                )))
            except:
                driver.save_screenshot(f"{max_tries}_headline_screenshot.png")
                status = 503
                info = "Failed to get headline on artist page"
            
            # switch back to location page
            driver.get(data["link"])
            return after_cookies(driver, data, status, info, max_tries-1)

        # check again for modal
        hidden_modal = None
        try:
            hidden_modal = wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "div.P24BotProtectionModal.hidden"
            )))
            status = 200
            info = "Bot protection modal hidden on second check"
        except:
            driver.save_screenshot(f"{max_tries}_second_check_screenshot.png")
            status = 502
            info = "Bot protection modal not hidden on second check"

    if status < 500:
        try:
            wait.until(EC.presence_of_element_located((
                By.XPATH,
                "//div[contains(@class, 'EventEntry') and not(contains(@class, 'hidden'))]"
            )))
        except:
            driver.save_screenshot(f"{max_tries}_entries_screenshot.png")
            status = 501
            info = "No event entries visible"

    driver.save_screenshot("screenshot.png")
    return {
        "page_source": driver.page_source,
        "url": driver.current_url,
        "cookies": driver.get_cookies(),
        "status": status,
        "info": info,
        "max_tries": max_tries,
    }
