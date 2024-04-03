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
    wait = WebDriverWait(driver, 10)
    button = wait.until(EC.presence_of_element_located((
        By.XPATH,
        "//button[contains(@class, 'BotProtectionCard-Button') and not(contains(@class, 'hidden'))]",
    )))
    if button:
        button.click()
        try:
            wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.P24BotProtectionModal.hidden")))
        except:
            driver.save_screenshot("screenshot.png")
            status = 500
            info = "Bot protection modal not hidden"

    return {
        "page_source": driver.page_source,
        "url": driver.current_url,
        "cookies": driver.get_cookies(),
        "status": status,
        "info": info,
    }
