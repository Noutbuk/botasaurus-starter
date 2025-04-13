from botasaurus.browser import browser, Driver, Wait

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@browser
def list_locations(driver: Driver, data):
    # Visit the Omkar Cloud website
    driver.get_via(data["link"], referer="https://www.fansale.de")
    # driver.get_via("https://www.fansale.de/tickets/all/nina-chuba/583604", referer="https://www.fansale.de")
        
    cookie_banner = driver.wait_for_element("#cmpwrapper", wait=Wait.LONG)
    cookie_button = driver.get_element_with_exact_text("Accept", wait=Wait.LONG)
    driver.enable_human_mode()
    cookie_button.click()
    driver.disable_human_mode()

    location_entry = driver.select_all("a.EventEntry")

    locations = [extract_locations(entry) for entry in location_entry]
    locations = [entry for entry in locations if "eventim" not in entry["link"]]

    # Retrieve the heading element's text
    #driver.prompt()


    # Save the data as a JSON file in output/scrape_heading_task.json
    return {
        "locations": locations
    }

def extract_locations(entry):
    # <a data-city="BERLIN" data-event-series-name="" data-event-series-id="3559509" data-tracking-eventdate="2025-11-09" data-qa="eventRow" href="/tickets/all/nina-chuba/583604/18559825" target="_self" class="EvEntry EventEntry ListEntry js-EventEntry js-VisibleByFilter" aria-label="Sonntag 9. Nov 2025 Nina Chuba - Arena Tour 2025 BERLIN 19:30 Uhr Uber Arena EVENTIM Ticketcheck Angebot Fair Deal Angebot Angebote ab €58,54 Ansehen" data-track="" data-category="productlist" data-action="fansale_main" data-label="nina chuba">
    return {
        "link": "https://www.fansale.de" + entry.get_attribute("href"),
        "eventdate": entry.get_attribute("data-tracking-eventdate"),
        "city": entry.get_attribute("data-city"),
    }

@browser
def get_tickets(driver: Driver, data):
    # https://www.fansale.de/tickets/all/lady-gaga/228027
    # https://www.fansale.de/tickets/all/lady-gaga/228027/20060384
    # Visit the Omkar Cloud website
    # driver.get_via(data["link"], referer="https://www.fansale.de/tickets/all/lady-gaga/228027")
    #driver.get_via("https://www.fansale.de/tickets/all/lady-gaga/228027/20060384", referer="https://www.fansale.de/tickets/all/lady-gaga/228027")
    driver.get_via(data["link"], referer=data["referer"])
    #driver.get_via("https://www.fansale.de/tickets/all/nina-chuba/583604/19533536", referer="https://www.fansale.de/tickets/all/nina-chuba/583604")
    
    cookie_banner = driver.wait_for_element("#cmpwrapper", wait=Wait.VERY_LONG)
    cookie_button = driver.get_element_with_exact_text("Accept", wait=Wait.VERY_LONG)
    if cookie_button:
        driver.enable_human_mode()
        cookie_button.click()
        driver.disable_human_mode()
    
    bot_button = driver.get_element_with_exact_text("Angebote laden", wait=Wait.VERY_LONG)
    if bot_button:
        driver.enable_human_mode()
        bot_button.click()
        driver.disable_human_mode()

    event_list = driver.wait_for_element(".EventEntryList", wait=Wait.LONG)
    event_entries = driver.select_all("div.EventEntry-isClickable")

    # <div data-offer-id="9511319" data-qa="ticketToBuy" data-splitting-possibilities="1,2" data-splitting-possibility-prices="77.97,155.94" data-fairdeal="true" data-certified="true" data-offertype="Sofortkauf" data-seatdescriptionforarialabel="Freie Platzwahl" class="EventEntry js-EventEntry EventEntry-isClickable EventEntry-isLast" style="order: 1;">

    for entry in event_entries:
        print(entry.get_attribute("data-offer-id"))
        print(entry.get_attribute("data-splitting-possibilities"))
        print(entry.get_attribute("data-splitting-possibility-prices"))
        print(entry.get_attribute("data-seatdescriptionforarialabel"))

    available_tickets = [extract_events(entry) for entry in event_entries]
    #driver.prompt()

    # button = driver.findElement(By.id("cmpwrapper")).getShadowRoot().findElement(By.id("cmpbox").cssSelector("a.cmpboxbtnyes"))
    # cookie_button = WebDriverWait(driver, 5).until(EC.visibility_of((driver.execute_script(
    #     "return document.getElementById('cmpwrapper').shadowRoot.getElementById('cmpbox').querySelector('a.cmpboxbtnyes')"))))

    # Save the data as a JSON file in output/scrape_heading_task.json
    return {
        "available_tickets": available_tickets
    }
# scrape_heading_task(data={"link": "https://www.fansale.de/tickets/all/lady-gaga/228027"})

def extract_events(entry):
    return {
        "id": entry.get_attribute("data-offer-id"),
        "possibilities": entry.get_attribute("data-splitting-possibilities"),
        "possibility-prices": entry.get_attribute("data-splitting-possibility-prices"),
        "seatdescription": entry.get_attribute("data-seatdescriptionforarialabel"),
    }
