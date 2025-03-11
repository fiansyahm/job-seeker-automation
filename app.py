from flask import Flask, request, render_template

import os
import subprocess
import time

# Fungsi untuk menginisialisasi Selenium WebDriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


app = Flask(__name__)

def kill_chrome_processes():
    # Untuk Windows, gunakan taskkill untuk mematikan semua proses chrome.exe
    try:
        subprocess.run("taskkill /F /IM chrome.exe", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Semua proses Chrome telah dimatikan.")
    except subprocess.CalledProcessError:
        print("Tidak ada proses Chrome yang berjalan atau gagal mematikan.")

def init_driver():
    # Matikan semua proses Chrome yang berjalan
    kill_chrome_processes()

    # Path ke chromedriver.exe
    chromedriver_path = r".\application\chrome\chromedriver.exe"

    # Tentukan path ke profil Chrome-mu
    chrome_profile_path = r"C:\Users\Arifiansyah\AppData\Local\Google\Chrome\User Data\Profile 22"

    # Set opsi Chrome untuk pakai profil yang sudah ada
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir=C:\\Users\\Arifiansyah\\AppData\\Local\\Google\\Chrome\\User Data")  # Folder utama User Data
    chrome_options.add_argument(f"profile-directory=Profile 22")  # Nama profil spesifik

    # Tambahan untuk menghindari masalah DevTools
    chrome_options.add_argument("--remote-debugging-port=9222")

    # Inisialisasi WebDriver dengan profil
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver

def click_selenium(driver,xfullpath,search_by,send_keys=None):
 # tunggu hingga elemen yang ingin diklik terlihat dan dapat diklik
    wait = WebDriverWait(driver, 5)
    if search_by == "xpath":
        by_for=By.XPATH
    elif search_by == "id":
        by_for=By.ID
    elif search_by == "css":
        by_for=By.CSS_SELECTOR
    click_elem = wait.until(EC.element_to_be_clickable((by_for, xfullpath)))
    
    if send_keys != None:
        click_elem.send_keys(send_keys)
    if send_keys == 'clear':
        click_elem.clear()
    else:
        # klik elemen yang sudah terlihat dan dapat diklik
        click_elem.click() 
    return click_elem

def getAttributeDiv(driver, xfullpath, search_by, attribute):
    wait = WebDriverWait(driver, 5)  # Tunggu maksimal 5 detik
    if search_by == "xpath":
        by_for = By.XPATH
    elif search_by == "id":
        by_for = By.ID
    elif search_by == "css":
        by_for = By.CSS_SELECTOR
    else:
        raise ValueError("search_by harus 'xpath', 'id', atau 'css'")

    # Ganti element_to_be_clickable dengan presence_of_element_located
    elem = wait.until(EC.presence_of_element_located((by_for, xfullpath)))
    attribute_value = elem.get_attribute("innerHTML")
    return attribute_value

def getHrefAttribute(html_content):
    print("HTML CONTENT :",html_content)
    soup = BeautifulSoup(html_content, 'html.parser')
    link = soup.find('a')
    if link and 'href' in link.attrs:
        href = link['href']
        print("Nilai href:", href)
        return href
    else:
        print("Tidak ada href ditemukan di HTML")

def openJobstreet():
    # Inisialisasi driver
    driver = init_driver()
    
    url='https://id.jobstreet.com/id/oauth/login?returnUrl=http%3A%2F%2Fid.jobstreet.com%2F';
    # Buka URL
    driver.get(url)
    try:
        xfullpath='/html/body/div/div/div/div[2]/div/div/div/div[3]/div/div/form/span/div[2]/button[1]'
        click_selenium(driver,xfullpath,'xpath')

        xfullpath='/html/body/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[1]/form/span/section/div/div/div/div/ul/li[1]/div/div[1]/div/div[2]'
        click_selenium(driver,xfullpath,'xpath')

        xfullpath='/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div/div[2]/div/div/button/div[1]'
        click_selenium(driver,xfullpath,'xpath')

        print('login dulu')
    except:
        # Tunggu sebentar agar halaman termuat
        print('sudah login')
    
    current_url = driver.current_url
    print("Recently URL:", current_url)

    time.sleep(20)

    for i in range(10):
        xfullpath='/html/body/div[1]/div/div[6]/div/div[2]/div[3]/section/div/div[3]/div[1]/div/div[2]/div[1]/div[2]/div/div/div[1]/div/a'
        click_selenium(driver,xfullpath,'xpath')
        time.sleep(5)
        
        xfullpath='/html/body/div[58]/div/div[2]/div[2]/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/div[4]/div/div/div/div/div[1]'
        href=getAttributeDiv(driver,xfullpath,'xpath','href')
        link=getHrefAttribute(href)
        driver.get(link)

        # buka current link
        driver.get(current_url)
        time.sleep(20000)
        
    time.sleep(20000)
    

    # Ambil HTML
    html_content = driver.page_source

    # Tutup driver
    driver.quit()

# Route utama
@app.route('/', methods=['GET', 'POST'])
def index():
    html_content = None
    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            try:

                openJobstreet()

                # Inisialisasi driver
                driver = init_driver()
                
                # Buka URL
                driver.get(url)
                
                # Tunggu sebentar agar halaman termuat
                time.sleep(20000)
                
                # Ambil HTML
                html_content = driver.page_source
                
                # Tutup driver
                driver.quit()
                
            except Exception as e:
                html_content = f"Error: {str(e)}"
    
    return render_template('index.html', html_content=html_content)

# Template HTML sederhana (simpan sebagai templates/index.html)
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Selenium Flask Browser</title>
</head>
<body>
    <h1>Masukkan URL</h1>
    <form method="POST" action="/">
        <input type="text" name="url" placeholder="Masukkan URL (contoh: https://example.com)">
        <input type="submit" value="Browse">
    </form>
    {% if html_content %}
        <h2>Hasil HTML:</h2>
        <textarea rows="20" cols="100">{{ html_content }}</textarea>
    {% endif %}
</body>
</html>
"""

# Buat file template jika belum ada
import os
if not os.path.exists('templates'):
    os.makedirs('templates')
with open('templates/index.html', 'w') as f:
    f.write(html_template)

if __name__ == '__main__':
    app.run(debug=True)