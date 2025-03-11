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

import requests

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
    attribute_value = elem.get_attribute(attribute)
    return attribute_value

def getHrefAttribute(html_content):
    # print("HTML CONTENT :",html_content)
    soup = BeautifulSoup(html_content, 'html.parser')
    link = soup.find('a')
    if link and 'href' in link.attrs:
        href = link['href']
        # print("Nilai href:", href)
        return href
    else:
        print("Tidak ada href ditemukan di HTML")

def getCoverLatter(html_content):
    prompt='Buatkan cover letter dengan keterangan\n\n'
    prompt+='Nama:Muhammad Arifiansyah\n\n'
    prompt+='Lulusan Teknik Informatika ITS\n\n'
    prompt+='Contoh Lamaran:\n\n'
    prompt+= example_lamaran
    prompt+='\n\nDengan informasi lamaran seperti pada HTML dibawah:\n\n\''
    prompt+=html_content
    prompt+='\n\nMulai dari Yth. Bapak/Ibu HRD PT. NashTa Global Utama (tanpa alamat dan nama) dan ditutup dengan nomer telepon\n\n'
    prompt+='Jangan ada sejenis: [Alamat PT. NashTa Global Utama, jika diperlukan] ,**Catatan:**  Surat lamaran ini telah disesuaikan dengan informasi yang Anda berikan dan deskripsi pekerjaan di HTML.  Pastikan untuk mengganti placeholder "[Nama Anda]", "[Nomor Telepon]"'
    return call_gemini_api(prompt)


def call_gemini_api(prompt):
    # API Key
    api_key = 'AIzaSyCfQvu0vb5BC1Y3A0Yxd8Pd1qwtKsvY8JE'
    # Alternatif API Key (dikomentari)
    # api_key = 'AIzaSyArumy4ma-XCr9yXFnsoqOKkHdXCbhV2iQ'
    
    # URL API Gemini
    gemini_api_url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}'
    
    # Payload untuk request (sesuai format API Gemini)
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    
    # Header untuk request
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        # Kirim request POST ke API
        response = requests.post(gemini_api_url, json=payload, headers=headers)
        
        # Pastikan request berhasil
        response.raise_for_status()
        
        # Ambil hasil dari response
        result = response.json()
        # Ekstrak teks dari response (sesuai struktur API Gemini)
        generated_text = result['candidates'][0]['content']['parts'][0]['text']
        return generated_text
    
    except requests.exceptions.RequestException as e:
        print(f"Error saat memanggil API: {e}")
        return None

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
    
    main_url = driver.current_url
    print("Recently URL:", main_url)

    for i in range(10):
        # click apply
        xfullpath='/html/body/div[1]/div/div[6]/div/div[2]/div[3]/section/div/div[3]/div[1]/div/div[2]/div[1]/div[2]/div/div/div[1]/div/a'
        click_selenium(driver,xfullpath,'xpath')

        # get data job opening
        # xfullpath='/html/body/div[57]/div/div[2]/div[2]/div/div/div[1]/div/div[2]/div[2]'
        # html_content=getAttributeDiv(driver,xfullpath,'xpath','innerHTML')
        # cover_latter=getCoverLatter(html_content)
        cover_latter='Izin Melamar'
        print(cover_latter)
        
        # link full lamaran
        xfullpath='/html/body/div[57]/div/div[2]/div[2]/div/div/div[1]/div/div[2]/div[2]'
        html_content=getAttributeDiv(driver,xfullpath,'xpath','innerHTML')
        link='https://id.jobstreet.com'+getHrefAttribute(html_content)
        driver.get(link)

        # klik lamaran
        link = driver.current_url.split('?')[0].rstrip('/') + '/apply'
        driver.get(link)

        # fill lamaran
        xfullpath='/html/body/div[1]/div/div[1]/div[4]/div/div[3]/div[2]/div[3]/fieldset/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div/div/textarea'
        click_selenium(driver,xfullpath,'xpath','clear')
        click_selenium(driver,xfullpath,'xpath',cover_latter)

        # klik lanjut 1
        xfullpath='/html/body/div[1]/div/div[1]/div[4]/div/div[3]/div[2]/div[4]/div/button'
        click_selenium(driver,xfullpath,'xpath')

        print('wait')
        time.sleep(10)

        # klik lanjut 2 //Jawab Pertanyaan
        xfullpath=f"//*[@data-testid='continue-button']"
        click_selenium(driver,xfullpath,'xpath')

        try:
            # klik lanjut 3 //Perbarui Profil Jobstreet
            xfullpath=f"//*[@data-testid='continue-button']"
            click_selenium(driver,xfullpath,'xpath')
        except:
            print('skip button')

        # final klik
        xfullpath=f"//*[@data-testid='review-submit-application']"
        click_selenium(driver,xfullpath,'xpath')

        driver.get(main_url)

        

    # buka current link
    # driver.get(current_url)
        
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

example_lamaran="""
Yth Bapak/Ibu
HRD Perusahaan
Dengan hormat,
Perkenalkan nama saya Muhammad Arifiansyah Melalui email ini saya menyampaikan lamaran pekerjaan ke Perusahaan PT Cipta Teknologi Bersama di posisi Software Developer sesuai dengan lowongan pekerjaan yang ditayangkan pada platfrom jobstreet.

Saya merupakan lulusan Institut Teknologi Sepuluh Nopember (ITS), Saya juga pernah tergabung dalam beberapa organisasi dikampus salah satunya pada event schematics sebagai Kepala Biro Pendanaan dan memiliki kemampuan untuk mengembangkan website informasi ataupun e-commerce serta aplikasi android yang fungsional dan menarik secara visual, saya memiliki minat besar berkarier di Perusahaan PT Cipta Teknologi Bersama karena deskripsi pekerjaan sesuai dengan pengalaman dan minat saya. Dari segi pengalaman, sering menggunakan Laravel untuk mengerjakan project sebagai backendnya. Saya juga terbiasa dalam menggunakan API contohnya API Midtrans, API Shopee, API Alamat, dll. Beberapa proyek saya kerjakan sendiri, sehingga dapat disebut saya menjadi Software Developerdalam hal ini.

Dari pengalaman dan beberapa kemampuan tersebut, saya berharap mendapat gaji Rp. 6.500.000. Saya memiliki kemampuan beberapa bahasa pemprograman seperti PHP, Python, Javascript, dan Java. Framework Backend yang saya kuasai adalah Laravel, Django, React, dan Spring. Sedangkan untuk Framework Frontend yang saya kuasai adalah Boostrap, Tailwind, dll. Untuk RDBMS yang saya gunakan adalah MySQL, MongoDB, dan Firebase. Pengalaman saya menjadi Front Dev dan Back Dev adalah 3 tahun. Saya terbiasa menggunakan GIT untuk menyimpan kodingan dan beberapa dokumentasinya. Menggunakan GIT kurang lebih 3 tahun. Saya berpengalaman dalam scrum agile team salah satunya saat mengerjakan tugas skripsi saya, saya menggunakan platfrom clickup waktu itu. Saya siap bekerja secepatnya untuk saat ini, saya hanya berharap nanti dapat bekerjasama dan berkontribusi dengan baik di perusahaan ini. 

Bersama email ini saya lampirkan CV sebagai dokumen pendukung. Demikian disampaikan, atas perhatian Bapak/Ibu disampaikan terimakasih.

Hormat saya,
Muhammad Arifiansyah
085730794876

"""

# Buat file template jika belum ada
import os
if not os.path.exists('templates'):
    os.makedirs('templates')
with open('templates/index.html', 'w') as f:
    f.write(html_template)

if __name__ == '__main__':
    app.run(debug=True)