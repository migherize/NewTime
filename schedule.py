import subprocess
import time
from datetime import datetime, timedelta

while True:
    today = datetime.now()
    dt_string = today.strftime("%d/%m/%Y %H:%M:%S")
    schedule = "schedule={}".format(dt_string)
    subprocess.call(["scrapy","crawl","cryptonews","-a",schedule],cwd="./noticias")
    subprocess.call(["scrapy","crawl","cryptoslate","-a",schedule],cwd="./noticias")
    time.sleep(60)