import os

DEFAULT_SITE_URLS = {
    "default": "https://www.saucedemo.com",
    "items": "https://www.saucedemo.com/inventory.html",
    "cart": "https://www.saucedemo.com/cart.html",
}

DEBUG = True
HEADLESS = False
ON_PROXY = False
DO_SCREENSHOT = True
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROXY_FILE = os.path.join(BASE_DIR, "proxy.txt")
BROWSER_TYPE = "chromium" # "firefox", "webkit" "chromium"
SESSION_DATA_DIR = "data/temp/"

# [min, max] milliseconds
TIMEOUT = 5000
DELAYS = {
    "click": [1000, 3000],
    "type": [100, 200],
    "scroll": [2000, 5000],
}

# DEFAULT LOGIN INFO
USERNAME = "standard_user"
PASSWORD = "secret_sauce"
