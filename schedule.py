import subprocess
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

while True:
    today = datetime.now(ZoneInfo("Europe/Berlin"))
    dt_string = today.strftime("%d/%m/%Y %H:%M:%S")
    schedule = "schedule={}".format(dt_string)
    subprocess.call(["scrapy","crawl","cryptonews","-a",schedule],cwd="./noticias")
    subprocess.call(["scrapy","crawl","cryptoslate","-a",schedule],cwd="./noticias")
    subprocess.call(["scrapy","crawl","bitcoinmagazine","-a",schedule],cwd="./noticias")
    subprocess.call(["scrapy","crawl","newsbtc","-a",schedule],cwd="./noticias")
    subprocess.call(["scrapy","crawl","bitcoins","-a",schedule],cwd="./noticias")
    print("ESPERANDO SIGUIENTE HORA")
    time.sleep(60)