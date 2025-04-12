from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import time

# 1. Setup Chrome Options
chrome_options = Options()

chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('--ignore-certificate-errors')

chrome_options.add_argument("--headless")  # Run in headless mode (no window)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# 2. Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

try:
    # 3. Open the URL
    url = "https://www.stubhub.com/explore?lat=MjUuNDQ3ODkwMw%3D%3D&lon=LTgwLjQ3OTIxOTY%3D&to=253402300799999&page=1&tlcId=2"
    driver.get(url)

    # 4. Wait for page to load
    time.sleep(5)  # Let JavaScript load the events

    # 5. Find all event cards
    event_cards = driver.find_elements(By.XPATH, "//ul[@class=\"sc-13546f91-1 bDlbkX\"]//li//a")
    event_cards_count = len(driver.find_elements(By.XPATH, "//ul[@class=\"sc-13546f91-1 bDlbkX\"]//li//a"))
    events = []

   # 6. Loop through first  event cards
    for card in event_cards[:event_cards_count]:  
        try:
            title_element = card.find_element(By.XPATH, ".//p[@class='sc-9b60a1e0-6 hvVHAU']")
            image_element = card.find_element(By.XPATH, ".//img")
 
            # Defaults
            date_time = ""
            location = ""
 
            details = card.find_elements(By.XPATH, ".//p[@class='sc-9b60a1e0-8 haloEs']")
            if len(details) == 2:
                date_time = details[0].text.strip()
                location = details[1].text.strip()
            elif len(details) == 1:
                date_time = details[0].text.strip()
    
            event = {
                "title": title_element.text.strip(),
                "datetime": date_time,
                "location": location,
                "image": image_element.get_attribute("src").strip()
            }
 
            events.append(event)
        except Exception as e:
            print(f"Error parsing an event: {e}")

    # 12. Output to JSON
    json_output = json.dumps(events, indent=4)
    print(json_output)

    # 13. Save to a file
    with open("events.json", "w") as f:
        f.write(json_output)
  

finally:
    # 14. Clean up
    driver.quit()