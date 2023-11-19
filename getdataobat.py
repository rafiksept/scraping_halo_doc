from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.chrome.options import Options
import pandas as pd
# from bs4 import BeautifulSoup

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
chrome_options = Options()
options = [
    "--headless",
    f"--user-agent={user_agent}"
]
for option in options:
    chrome_options.add_argument(option)

df = pd.read_csv("name_obat_fix.csv")
name_array = []
price_array = []
deksripsi_array = []
isi_deksripsi_array = []


for i in range(11000, 13000 ):
    name = df["name"][i]
    print(f"Index ke - {i} Ambil data - {name}")
    url = f"https://www.halodoc.com/obat-dan-vitamin/{name}"

    try:
    # run in GitHub action
        driver = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=chrome_options)
        driver.get(url)
        print("driver based on ChromeType.CHROMIUM is working")
    except:
        # run in local
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)
        print(f"driver is working")
        continue

    try :
        tunggu =  WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.drug-detail')))
    except :
        print("tidak ada elemen nya!")
        continue

    try :
        nama_obat = driver.find_elements(By.CSS_SELECTOR, ".product-label")
        name_array.append(nama_obat[0].text)
    except :
        print(name + "tidak ada nama!")
        continue

    try :
        harga = driver.find_elements(By.CSS_SELECTOR, ".product-price")
        price_array.append(harga[0].text)
    except :
        print(name + "tidak ada harga")
        price_array.append("noValue")

    try :
        deskripsi = driver.find_elements(By.CSS_SELECTOR, ".ttl-list")
        deksripsi_array.append
        teks_deksripsi = []

        for i in range(0, len(deskripsi)):
            teks_deksripsi.append(deskripsi[i].text)

        deksripsi_string = "**".join(teks_deksripsi)
        deksripsi_array.append(deksripsi_string)

        isi_deksripsi = driver.find_elements(By.CSS_SELECTOR, ".drug-detail")
        teks_isi_deksripsi = []

        for i in range(0, len(isi_deksripsi)):
            teks_isi_deksripsi.append(isi_deksripsi[i].text)

        isi_deksripsi_string = "**".join(teks_isi_deksripsi)
        isi_deksripsi_array.append(isi_deksripsi_string)


    except :
        print(name + "tidak ada deskripsi")
        deksripsi_array.append("noValue")
        isi_deksripsi_array.append("noValue")

    driver.close()
df_obat = pd.DataFrame({
    "name" : name_array,
    "price" : price_array,
    "deskripsi" : deksripsi_array,
    "isi_deksripsi" : isi_deksripsi_array 
})

df_obat.to_csv("data_obat9.csv")
