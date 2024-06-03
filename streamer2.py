from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import threading
import random
import time
import sys
import subprocess

# Configuration
config = {
    "video_url": "https://www.youtube.com/watch?v=6SUeRyOmfps",
    "num_views": 25,
    "num_dns_changes": 5,  # Number of times to change DNS settings
    "chromedriver_path": "C:\\Users\\Amz\\.cache\\selenium\\chromedriver\\win64\\123.0.6312.122\\chromedriver.exe",
    "view_duration_min": 45,  # Minimum duration to play the video (in seconds)
    "view_duration_max": 100,  # Maximum duration to play the video (in seconds)
    "seek_wait_time": 2,  # Time to wait after seeking to a specific position in the video (in seconds)
    "thread_wait_time": 1,   # Time to wait between starting each thread (in seconds)
}

# Function to simulate viewing the YouTube video
def view_video(url):
    try:
        # Configure Chrome webdriver
        chrome_options = Options()
        chrome_options.add_argument("--mute-audio")  # Mute audio to avoid disturbing sound
        chrome_options.add_argument("--headless")  # Run in headless mode (without opening browser window)
        service = Service(config["chromedriver_path"])  # Specify the path to chromedriver executable
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Open the video URL
        driver.get(url)

        # Simulate playing the video for a random duration
        play_duration = random.randint(config["view_duration_min"], config["view_duration_max"])
        action_times = [play_duration / 4 * i for i in range(1, 5)]

        for action_time in action_times:
            print(f"Performing action at {int(action_time)} seconds")
            # Simulate seeking to a specific time in the video
            driver.execute_script(f"document.getElementsByTagName('video')[0].currentTime = {action_time};")
            time.sleep(config["seek_wait_time"])  # Wait after seeking

        # Close the browser
        driver.quit()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Function to cycle through tabs and swap DNS
def cycle_tabs_and_swap_dns():
    for _ in range(config["num_views"]):
        for _ in range(config["num_dns_changes"]):
            # Swap DNS
            swap_dns()
        # View video and perform actions
        for _ in range(4):  # Perform video actions four times
            view_video_with_dns_swap(config["video_url"])

# Function to view video and perform actions with DNS swap
def view_video_with_dns_swap(url):
    # Swap DNS before viewing the video
    swap_dns()
    # View the video and perform actions
    view_video(url)
# Function to swap DNS settings
def swap_dns():
    # Replace this command with the appropriate command to change DNS settings on your operating system
    # For Windows, you might use something like netsh command
    subprocess.run(["netsh", "interface", "ipv4", "set", "dnsservers", "name=", "source=static", "address=8.8.8.8"])
    print("DNS settings swapped.")

# Create threads for simultaneous viewing
threads = []
try:
    for _ in range(config["num_views"]):
        thread = threading.Thread(target=cycle_tabs_and_swap_dns)
        threads.append(thread)
        thread.start()
        time.sleep(config["thread_wait_time"])  # Wait between starting each thread

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("All views completed.")
except KeyboardInterrupt:
    print("\nScript terminated by user.")
    sys.exit(0)
except Exception as e:
    print(f"An error occurred: {str(e)}")
