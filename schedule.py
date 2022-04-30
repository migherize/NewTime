import subprocess
import time
from datetime import datetime, timedelta

while True:
    subprocess.call(["scrapy","crawl","cryptonews"],cwd="./noticias")
    subprocess.call(["scrapy","crawl","cryptoslate"],cwd="./noticias")
    time.sleep(3600)