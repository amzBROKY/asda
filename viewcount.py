import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup logging
logging.basicConfig(filename="kick_view_count.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Configuration
url = "https://kick.com/slicka"
geckodriver_path = "C:\\Users\\Amz\\Desktop\\geckodriver.exe"
os.environ["PATH"] += os.pathsep + os.path.dirname(geckodriver_path)
num_times = 3

# Configure Firefox options
options = Options()
options.headless = True  
options.set_preference("permissions.default.image", 2)  # Disable image loading

def get_view_count(driver):
    try:
        view_count_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "odometer-value"))
        )
        if view_count_elements:
            view_count = ''.join([element.text for element in view_count_elements])
            logging.info(f"Live View Count: {view_count}")
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Live View Count: {view_count}")
            return int(view_count)
        else:
            logging.warning("View count element not found")
            return None
    except Exception as e:
        logging.error(f"Error retrieving view count: {e}")
        return None

def open_side_pages(driver, url, num_times):
    for _ in range(num_times):
        driver.execute_script(f'window.open("{url}");')
        time.sleep(1)

try:
    with webdriver.Firefox(options=options) as driver:
        driver.get(url)
        
        view_count = get_view_count(driver)
        
        if view_count is not None:
            open_side_pages(driver, url, num_times)
        
        while True:
            # Refresh the main page
            driver.get(url)
            view_count = get_view_count(driver)
            
            if view_count is not None and view_count >= 100:  # Change the threshold to 100
                break
            
            # Refresh side pages
            for handle in driver.window_handles[1:]:
                driver.switch_to.window(handle)
                driver.get(url)
                time.sleep(15)  # Adjustable refresh interval (15 seconds)
            
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(10)  # Adjustable refresh interval (10 seconds)

except Exception as e:
    logging.error(f"Error: {e}")
