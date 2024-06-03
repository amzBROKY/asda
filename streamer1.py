import tkinter as tk
from tkinter import scrolledtext
import threading
import random
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

# Configuration
config = {
    "video_url": "https://www.youtube.com/watch?v=ZQw76wV6j8E",
    "num_views": 25,
    "edgedriver_path": "C:/Users/Amz/Desktop/msedgedriver.exe",
    "view_duration_min": 45,  # Minimum duration to play the video (in seconds)
    "view_duration_max": 100,  # Maximum duration to play the video (in seconds)
    "seek_wait_time": 2,  # Time to wait after seeking to a specific position in the video (in seconds)
    "thread_wait_time": 1,   # Time to wait between starting each thread (in seconds)
}

# Function to simulate viewing the YouTube video
def view_video(url, thread_num, output_text):
    try:
        # Configure Edge webdriver
        edge_options = Options()
        edge_options.use_chromium = True  # Use Chromium-based Edge
        edge_options.add_argument("--mute-audio")  # Mute audio to avoid disturbing sound
        edge_options.add_argument("--headless")  # Run in headless mode (without opening browser window)
        service = Service(config["edgedriver_path"])  # Specify the path to msedgedriver executable
        driver = webdriver.Edge(service=service, options=edge_options)

        # Open the video URL
        output_text.insert(tk.END, f"Thread-{thread_num}: Opening the video URL\n")
        driver.get(url)

        # Simulate playing the video for a random duration
        play_duration = random.randint(config["view_duration_min"], config["view_duration_max"])
        output_text.insert(tk.END, f"Thread-{thread_num}: Simulating viewing for {play_duration} seconds\n")
        time.sleep(play_duration)

        # Close the browser
        driver.quit()
        output_text.insert(tk.END, f"Thread-{thread_num}: Viewing completed\n")
    except Exception as e:
        output_text.insert(tk.END, f"Thread-{thread_num}: An error occurred: {str(e)}\n")

# Function to cycle through tabs
def cycle_tabs(thread_num, output_text):
    for _ in range(config["num_views"]):
        view_video(config["video_url"], thread_num, output_text)

# Function to start viewing threads
def start_threads(output_text):
    threads = []
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "Starting viewing threads...\n")
    for i in range(config["num_views"]):
        thread = threading.Thread(target=cycle_tabs, args=(i+1, output_text))
        threads.append(thread)
        thread.start()
        time.sleep(config["thread_wait_time"])  # Wait between starting each thread

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    output_text.insert(tk.END, "All views completed.\n")

# Create Tkinter GUI
root = tk.Tk()
root.title("YouTube Viewer")
root.geometry("600x400")

# Create scrolled text widget for output
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
output_text.pack(expand=True, fill=tk.BOTH)

# Button to start viewing threads
start_button = tk.Button(root, text="Start Viewing", command=lambda: start_threads(output_text))
start_button.pack()

root.mainloop()
