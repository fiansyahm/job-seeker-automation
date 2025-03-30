from flask import Flask, request, render_template

import os
import subprocess
import time
from datetime import datetime
import pyperclip  # Library untuk mengakses clipboard
import re

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
import re

app = Flask(__name__)

def kill_chrome_processes():
    # Untuk Windows, gunakan taskkill untuk mematikan semua proses chrome.exe
    try:
        subprocess.run("taskkill /F /IM chrome.exe", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Semua proses Chrome telah dimatikan.")
    except subprocess.CalledProcessError:
        print("Tidak ada proses Chrome yang berjalan atau gagal mematikan.")

def loginGmail(driver):
    # register
    # identity
    xfullpath='/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[2]/div/div/div/button/span'
    click_selenium(driver,xfullpath,'xpath')        
    xfullpath='/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div/div[1]/div[1]/div/div[1]/div/div[1]/input'
    click_selenium(driver,xfullpath,'xpath','Rudi')
    xfullpath='/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div/div[1]/div[2]/div/div[1]/div/div[1]/input'
    click_selenium(driver,xfullpath,'xpath','Wijaya')
    xfullpath='/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div/div/div/button/span'
    click_selenium(driver,xfullpath,'xpath')

    # birthday
    xfullpath='/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div[1]/div[1]/div/div/div[2]/select/option[8]'
    click_selenium(driver,xfullpath,'xpath')
    xfullpath='/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div[1]/div[2]/div/div/div[1]/div/div[1]/input'
    click_selenium(driver,xfullpath,'xpath','23')
    xfullpath='/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div[1]/div[3]/div/div/div[1]/div/div[1]/input'
    click_selenium(driver,xfullpath,'xpath','2000')
    xfullpath='/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div[2]/div[1]/div/div[2]/select/option[3]'
    click_selenium(driver,xfullpath,'xpath')
    xfullpath='/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div/div/div/button/span'
    click_selenium(driver,xfullpath,'xpath')

    # choose email
    try:
        xfullpath='/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div/div[1]/div/div[1]/div/div[1]/input'
        # example 3 september 2000 jam 09:38 to be 030920000938
        stringtoday= datetime.now().strftime("%d%m%Y%H%M%S")
        click_selenium(driver,xfullpath,'xpath','Rudi'+stringtoday)
        # click xfullpath yang mengandung button
        xfullpath='/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button'
        click_selenium(driver,xfullpath,'xpath')
    except:
        xfullpath='/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div[1]/div[1]/div/span/div[3]/div/div[1]/div'
        click_selenium(driver,xfullpath,'xpath')
        xfullpath='/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div[2]/div[1]/div/div[1]/div/div[1]/input'
        click_selenium(driver,xfullpath,'xpath','Rudi'+stringtoday)
        xfullpath='/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button'
        click_selenium(driver,xfullpath,'xpath')

    xfullpath='/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div/div[1]/div/div/div[1]/div/div[1]/div/div[1]/input'
    click_selenium(driver,xfullpath,'xpath','Dr@gon32')
    xfullpath='/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'
    click_selenium(driver,xfullpath,'xpath','Dr@gon32')
    xfullpath='/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div/div/div/button'
    click_selenium(driver,xfullpath,'xpath')


def init_driver():
    # Matikan semua proses Chrome yang berjalan
    kill_chrome_processes()

    # Path ke chromedriver.exe
    chromedriver_path = r".\application\chrome\chromedriver.exe"

    # Set opsi Chrome untuk pakai profil yang sudah ada
    chrome_options = Options()

    choseOptions = 1
    if choseOptions == 1:
        # Mode Profil
        chrome_options.add_argument(f"user-data-dir=C:\\Users\\Arifiansyah\\AppData\\Local\\Google\\Chrome\\User Data")  # Folder utama User Data
        chrome_options.add_argument(f"profile-directory=Profile 22")  # Nama profil spesifik
        chrome_options.add_argument("--remote-debugging-port=9222")
    else:
        chrome_options.add_argument("--guest")  # Mode Guest
        # chrome_options.add_argument("user-data-dir=C:\\Temp\\SeleniumGuest")  # Profile kosong
    
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
    prompt+='\n\nMulai dari Yth. Bapak/Ibu HRD (tanpa alamat dan nama) dan ditutup dengan nomer telepon\n\n'
    prompt+='Jangan ada sejenis: [Alamat ....., jika diperlukan] ,**Catatan:**  Surat lamaran ini telah disesuaikan dengan informasi yang Anda berikan dan deskripsi pekerjaan di HTML.  Pastikan untuk mengganti placeholder "[Nama Anda]", "[Nomor Telepon]"'
    prompt+='Ganti NashTa Global Utama dan lowongan di apply denga nama perusahaan, jobnya dan posisinya Dengan informasi lamaran seperti pada HTML'
    return call_gemini_api(prompt)


def call_gemini_api(prompt):
    # API Key
    # api_key = 'AIzaSyCfQvu0vb5BC1Y3A0Yxd8Pd1qwtKsvY8JE'
    # Alternatif API Key (dikomentari)
    api_key = 'AIzaSyArumy4ma-XCr9yXFnsoqOKkHdXCbhV2iQ'
    
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
def clickColoumnDetail(driver,xfullpath):
    if '||' in xfullpath:
        xfullpath = xfullpath.split('||')[0]
        contain = xfullpath.split('||')[1]
        print('xfullpath:',xfullpath)
        print('\ncontain:',contain)
        click_selenium(driver,xfullpath,'xpath',contain)
    elif 'option' not in xfullpath:
        checkbox = driver.find_element(By.XPATH, xfullpath)
        if not checkbox.is_selected():
            checkbox.click()
    else:
        click_selenium(driver,xfullpath,'xpath')
    # time.sleep(10)

def clickColoumn(driver,xfullpath,totalxpath):
    if totalxpath == 1:
        clickColoumnDetail(driver,xfullpath)
    else:
        parts = xfullpath.split('//*')
        for part in parts:
            clickColoumnDetail(driver,part)

def getAutoComplete(driver,html_content):
    print('Auto Complete Start')
    prompt=''
    prompt+='\n\nDengan informasi from pra lamaran seperti pada html ini:\n\n\''
    prompt+=html_content
    prompt+='\n\nBuatkan urutan xpath yang di klik berdasar profil lamaran disini\n\n'
    prompt+= example_lamaran
    prompt+='\n\nJika tidak ada pengalaman piih Less than 1 year\n\n\''
    # Get JSON from URL
    # url = 'https://ideea.site/personal-profile/30'
    # response = requests.get(url)
    # data = response.text  # Mengambil isi respons sebagai string
    # prompt+= data

    prompt+=f'''Keluarannya tolong seperti ini: ["//*[@data-testid='continue-button']", "//*[@data-testid='continue-button']", "//*[@data-testid='continue-button']"]'''
    prompt+=f'''\n\nPilihannya dipilihkan Gemini saja'''
    prompt+='formulir pra-lamaran ini xpathnya dipilih kira2 saja,misal pertanyaan tentang bahasa,dipilih bahasa inggris saja,dll'
    list_xpath_string=call_gemini_api(prompt)
    print('list_xpath_string:',list_xpath_string)

    # change //select[  //input[
    list_xpath_string=list_xpath_string.replace('//select[', '//*[')
    list_xpath_string=list_xpath_string.replace('//input[', '//*[')
    # list_xpath_string=list_xpath_string.replace('//textarea[', '//*[')
    # list_xpath_string=list_xpath_string.replace('//option[', '//*[')
    # list_xpath_string=list_xpath_string.replace('//label[', '//*[')
    # list_xpath_string=list_xpath_string.replace('//button[', '//*[')
    # list_xpath_string=list_xpath_string.replace('//a[', '//*[')
    # list_xpath_string=list_xpath_string.replace('//li[', '//*[')
    # list_xpath_string=list_xpath_string.replace('//div[', '//*[')
    # list_xpath_string=list_xpath_string.replace('//span[', '//*[')
  

    arr_xpath=list_xpath_string.split('```')[1].split('```')[0]
    print('arr_xpath:',arr_xpath)
    elements = arr_xpath.split('",')
    print('-------GO TO XPATH---------')
    for i in range(len(elements)):
        if('"//*' in elements[i] and 'continue-button' not in elements[i]):
            start = elements[i].find('"//*[')           +1
            xfullpath=elements[i][start:len(elements[i])]
            try:
                xfullpath.strip()
                print('xpath:',xfullpath)
                totalxpath = xfullpath.count('//*')
                clickColoumn(driver,xfullpath,totalxpath)
                time.sleep(1)
            except:
                pass
    # time.sleep(10000)

def getAutoCompleteInput(driver,html_content):
    print('Auto Complete Start')
    prompt=''
    prompt+='\n\nDengan informasi from pra lamaran seperti pada html ini:\n\n\''
    prompt+=html_content
    prompt+='\n\nBuatkan urutan xpath yang di klik berdasar profil lamaran disini\n\n'
    prompt+= example_lamaran
    prompt+='\n\nJika tidak ada pengalaman piih Less than 1 year\n\n\''
    # Get JSON from URL
    # url = 'https://ideea.site/personal-profile/30'
    # response = requests.get(url)
    # data = response.text  # Mengambil isi respons sebagai string
    # prompt+= data

    prompt+=f'''Keluarannya tolong seperti ini: ["//*[@data-testid='continue-button']", "//*[@data-testid='continue-button']", "//*[@data-testid='continue-button']","//*[contains(@data-testid, 'input-q_8e48fd774b5a6cc61e1027601d678e56')]/textarea||5 tahun" ]'''
    prompt+=f'''\n\n//*[contains(@data-testid, 'input-q_8e48fd774b5a6cc61e1027601d678e56')]/textarea||5 tahun   jadi ada xpath yang dikasih || 5 tahun sebagai inputannya,jadi kalau ada inputan tempelkan dengan || (isi)'''

    prompt+=f'''\n\nPilihannya dipilihkan Gemini saja'''
    prompt+='formulir pra-lamaran ini xpathnya dipilih kira2 saja,misal pertanyaan tentang bahasa,dipilih bahasa inggris saja,dll'
    list_xpath_string=call_gemini_api(prompt)
    print('list_xpath_string:',list_xpath_string)

    # change //select[  //input[
    list_xpath_string=list_xpath_string.replace('//select[', '//*[')
    list_xpath_string=list_xpath_string.replace('//input[', '//*[')
    list_xpath_string=list_xpath_string.replace('//textarea[', '//*[')

    arr_xpath=list_xpath_string.split('```')[1].split('```')[0]
    print('arr_xpath:',arr_xpath)
    elements = arr_xpath.split('",')
    print('-------GO TO XPATH---------')
    for i in range(len(elements)):
        if('"//*' in elements[i] and 'continue-button' not in elements[i]):
            start = elements[i].find('"//*[')           +1
            xfullpath=elements[i][start:len(elements[i])]
            try:
                xfullpath.strip()
                print('xpath:',xfullpath)
                totalxpath = xfullpath.count('//*')
                clickColoumn(driver,xfullpath,totalxpath)
                time.sleep(1)
            except:
                pass
    # time.sleep(10000)

def getAutoComplete1(driver,html_content):
    print('Auto Complete Start')
    prompt=''
    prompt+='\n\nDengan informasi html ini:\n\n\''
    prompt+=html_content
    prompt+='\n\nBuatkan urutan xpath yang di klik berdasar informasi disini\n\n'

   # Get JSON from URL
    url = 'https://ideea.site/personal-profile/30'
    response = requests.get(url)
    data = response.text  # Mengambil isi respons sebagai string
    prompt+= data
    
    prompt+=f'''Keluarannya tolong seperti ini dalam bentuk list xpath bukan lain (bukan kode python ,java,dll): ["//*[@data-testid='continue-button']", "//*[@data-testid='continue-button']", "//*[@data-testid='continue-button']"]'''
    prompt+=f'''\n\nPilihannya dipilihkan Gemini saja'''
    prompt+='formulir pra-lamaran ini xpathnya dipilih kira2 saja,misal pertanyaan tentang bahasa,dipilih bahasa inggris saja,dll'
    list_xpath_string=call_gemini_api(prompt)
    print('list_xpath_string:',list_xpath_string)

    # Regex untuk menangkap XPath
    pattern1 = r"`(/html[^`\n]*)`"
    pattern2 = r'"(//[^"]+)"'

    # Ekstrak semua XPath
    xpaths = re.findall(pattern1, list_xpath_string)
    if xpaths == []:
        xpaths = re.findall(pattern2, list_xpath_string)
    print('xpaths:',xpaths)
    
    print('------------------------')
    for xpath in xpaths:
        try:
            print('xpath:',xpath)
            if 'option' not in xpath:
                checkbox = driver.find_element(By.XPATH, xpath)
                if not checkbox.is_selected():
                    checkbox.click()
            else:
                click_selenium(driver,xpath,'xpath')
        except:
            pass
    # //*[@id="question-ID_Q_2630_V_1"]

def loginJobstreet(driver):
    xfullpath='/html/body/div/div/div/div[2]/div/div/div/div[3]/div/div/form/span/div[2]/button[1]'
    click_selenium(driver,xfullpath,'xpath')

    xfullpath='/html/body/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[1]/form/span/section/div/div/div/div/ul/li[1]/div/div[1]/div/div[2]'
    click_selenium(driver,xfullpath,'xpath')

    xfullpath='/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div/div[2]/div/div/button/div[1]'
    click_selenium(driver,xfullpath,'xpath')
    print('Sukses Login')

def openJobstreet():
    # loginGmail(driver)
    
    # Inisialisasi driver
    driver = init_driver()
    
    url='https://id.jobstreet.com/id/oauth/login?returnUrl=http%3A%2F%2Fid.jobstreet.com%2F';
    # Buka URL
    driver.get(url)
    try:
        # loginJobstreet(driver)
        pass
    except:
        # print('check')
        # time.sleep(100)
        # url='https://accounts.google.com/AccountChooser/signinchooser?service=mail&continue=https://mail.google.com/mail/&flowName=GlifWebSignIn&flowEntry=AccountChooser&ec=asw-gmail-globalnav-signin'
        # driver.get(url)
        # xfullpath='/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div[1]/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input'
        # click_selenium(driver,xfullpath,'xpath','fiansyahm31125@gmail.com')
        # xfullpath='/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button'
        # click_selenium(driver,xfullpath,'xpath')
        # xfullpath='/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input'
        # click_selenium(driver,xfullpath,'xpath','Dr@gon060')
        # xfullpath='/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button'
        # click_selenium(driver,xfullpath,'xpath')

        # time.sleep(5)

        # url='https://id.jobstreet.com/id/oauth/login?returnUrl=http%3A%2F%2Fid.jobstreet.com%2F';
        # # Buka URL
        # driver.get(url)
        # try:
        #     loginJobstreet(driver)
        # except:
        #     pass
        
        # Tunggu sebentar agar halaman termuat
        print('sudah login')
    
    last_index=0
    total_apply=''
    for page in range(10):
        main_url = driver.current_url
        print("Recently URL:", main_url)
        for index in range(32):
            print('page '+str(page+1)+' index '+str(last_index+index+1)+ ' last index '+str(last_index))
            if index==31:
                last_index+=32
            # if page<=1:
            #     continue
            try:
                way=1
                if(way==1):
                    # click apply
                    main_url='https://id.jobstreet.com/id/jobs-in-information-communication-technology'
                    main_url+='?page='+str(page+1)
                    driver.get(main_url)
                    # driver.get('https://id.jobstreet.com/id/jobs-in-information-communication-technology?subclassification=6302%2C6290%2C6287')
                    xfullpath=f"""//div[contains(@data-search-sol-meta, '"sectionRank":{last_index+index+1}')]"""
                    click_selenium(driver,xfullpath,'xpath')
                    # link full lamaran
                    # xfullpath='/html/body/div[1]/div/div[6]/div/section/div[2]/div/div/div[1]/div/div/div/div/div[2]/div/div/div[3]/div/div/div[2]/div[2]'
                    xfullpath='//*[@id="newTabButton"]/ancestor::*[11]'
                elif(way==2):
                    # theory
                    # click apply
                    driver.get(main_url)
                    xfullpath='/html/body/div[1]/div/div[6]/div/div[2]/div[3]/section/div/div[3]/div[1]/div/div[2]/div[1]/div[2]/div/div/div[1]/div/a'
                    click_selenium(driver,xfullpath,'xpath')
                    # link full lamaran
                    xfullpath='//*[@id="newTabButton"]/ancestor::*[11]'
                time.sleep(5)
                html_content=getAttributeDiv(driver,xfullpath,'xpath','innerHTML')
                link='https://id.jobstreet.com'+getHrefAttribute(html_content)
                driver.get(link)

                xfullpath='/html/body/div[1]/div/div[5]/div/div/div[2]/div[2]/div/div/div[1]'
                position = getAttributeDiv(driver, xfullpath, 'xpath', 'innerHTML')
                print('Posisi:'+position)
                
                xfullpath='/html/body/div[1]/div/div[5]/div/div/div[2]/div[2]/div/div/div[2]/section[1]/div/div'
                job_desc = getAttributeDiv(driver, xfullpath, 'xpath', 'innerHTML')
                print('Jobdesc:'+job_desc)

                full_apply="Dengan keterangan posisi:"+position+'\n\nDengan Jobdesc:'+job_desc
                cover_latter=getCoverLatter(full_apply)
                # cover_latter='Izin Melamar '
                print(cover_latter)

                # klik lamaran
                link = driver.current_url.split('?')[0].rstrip('/') + '/apply'
                driver.get(link)

                # get info job
                xfullpath='/html/body/div[1]/div/div[1]/div[4]/div/div[1]/div/div/div/div[2]/h1'
                company=getAttributeDiv(driver,xfullpath,'xpath','innerHTML')
                xfullpath='/html/body/div[1]/div/div[1]/div[4]/div/div[1]/div/div/div/div[2]/span[2]'
                position=getAttributeDiv(driver,xfullpath,'xpath','innerHTML')
                apply_desc=company+' - '+position
                print('apply_desc: '+apply_desc)
                
                # fill lamaran
                xfullpath='/html/body/div[1]/div/div[1]/div[4]/div/div[3]/div[2]/div[3]/fieldset/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div/div/textarea'
                click_selenium(driver,xfullpath,'xpath','clear')
                click_selenium(driver,xfullpath,'xpath',cover_latter)

                # klik lanjut 1
                xfullpath='/html/body/div[1]/div/div[1]/div[4]/div/div[3]/div[2]/div[4]/div/button'
                click_selenium(driver,xfullpath,'xpath')

                time.sleep(5)
                xfullpath='/html/body/div/div/div[1]/div[4]/div/div[3]'
                html_content = getAttributeDiv(driver, xfullpath, 'xpath', 'innerHTML')
                getAutoComplete(driver,html_content)

                for i in range(4):
                    try:
                        # klik lanjut 3 //Perbarui Profil Jobstreet [OPTIONAL]
                        xfullpath=f"//*[@data-testid='continue-button']"
                        click_selenium(driver,xfullpath,'xpath')
                    except:
                        print('skip button selanjutnya')
                    
                for i in range(3):
                    try:
                        # final klik
                        xfullpath=f"//*[@data-testid='review-submit-application']"
                        click_selenium(driver,xfullpath,'xpath')
                    except:
                        print('skip button kirim lamaran')
                time.sleep(5)
                total_apply+=str(last_index+index+1)+'.'+apply_desc+'\n'
            except:
                print('proses '+str(index+1)+' Gagal')
        print("Page "+str(page+1)+" Selesai")
    
    print(total_apply)
    with open("output.txt", "w", encoding="utf-8") as file:
        file.write(total_apply)

    # Tutup driver
    driver.quit()


def openIndeed():
    # loginGmail(driver)
    
    # Inisialisasi driver
    driver = init_driver()
    total_apply=''
    for page in range(10):
        if page==0:
            continue
        for index in range(10):
            try:    
                url='https://id.indeed.com/jobs?q=back+end+developer&start='+str(page*10)
                driver.get(url)
                xfullpath=f"""/html/body/main/div/div[2]/div/div[5]/div/div[1]/div[4]/div/ul/li[{index+2}]"""
                click_selenium(driver,xfullpath,'xpath')
                xfullpath="//button[contains(@aria-label, 'Copy Link')]"
                click_selenium(driver,xfullpath,'xpath')
                url=pyperclip.paste()
                driver.get(url)
                # get info job
                company='Tidak Ada'
                position='Tidak Ada'
                time.sleep(10)
                try:
                    xfullpath='/html/body/div/div[2]/div[3]/div/div/div[1]/div[2]/div[1]/div[2]/div/div/div/div[1]/div/span/a'
                    company=getAttributeDiv(driver,xfullpath,'xpath','innerHTML').split('<svg')[0]
                except:
                    pass
                try:
                    xfullpath='/html/body/div/div[2]/div[3]/div/div/div[1]/div[2]/div[1]/div[1]'
                    position=getAttributeDiv(driver,xfullpath,'xpath','innerHTML').split('Header-title">')[1]
                    position = re.sub(r'<.*?>', '', position)
                except:
                    pass
                
                apply_desc=company+' - '+position
                print('apply_desc: '+apply_desc)

                time.sleep(5)

                # continue
                # url=url+'%2CiaBackPress'
                # driver.get(url)
                xfullpath="//button[contains(@aria-label, 'Apply now')]"
                click_selenium(driver,xfullpath,'xpath')

                time.sleep(5)

                try:
                    xfullpath='/html/body/div[2]/div/div[1]/div/div/div[2]/div[2]/div/div/main/div[2]/div/div/fieldset/label/input'
                    clickColoumnDetail(driver,xfullpath)
                    xfullpath='/html/body/div[2]/div/div[1]/div/div/div[2]/div[2]/div/div/main/div[3]/div/button'
                    click_selenium(driver,xfullpath,'xpath')
                except:
                    print('tidak ada this session')
                
                try:
                    # CV
                    xfullpath='/html/body/div[2]/div/div[1]/div/div/div[2]/div[2]/div/div/main/div[3]/div'
                    click_selenium(driver,xfullpath,'xpath')
                except:
                    print('tidak ada CV')

                time.sleep(5)

                try:
                    # job experience
                    xfullpath='/html/body/div[2]/div/div/div/div/div[2]/div[2]/div/div/main/div[1]/div/div/div/div/div/div/div[2]/button'
                    click_selenium(driver,xfullpath,'xpath')
                except:
                    print('tidak ada job experience')

                time.sleep(20)

                try:
                    # question
                    xfullpath='/html/body/div[2]/div/div[1]/div/div/div[2]/div[2]/div/div/main'
                    html_content = getAttributeDiv(driver, xfullpath, 'xpath', 'innerHTML')
                    getAutoCompleteInput(driver,html_content)
                except:
                    print('tidak ada question')

                try:
                    time.sleep(5)
                    # lanjut
                    xfullpath='/html/body/div[2]/div/div[1]/div/div/div[2]/div[2]/div/div/main/div[3]/div/button'
                    click_selenium(driver,xfullpath,'xpath')
                except:
                    print('tidak ada lanjut')

                try:
                    time.sleep(5)
                    # final submit
                    xfullpath='/html/body/div[2]/div/div/div/div/div[2]/div[2]/div/div/main/div[3]/div/button'
                    click_selenium(driver,xfullpath,'xpath')
                except:
                    print('tidak ada final submit')
                total_apply+=str(index+2)+'.'+apply_desc+'\n'
            except:
                print('proses '+str(index+1)+' Gagal')
            
    print(total_apply)
    with open("output.txt", "w", encoding="utf-8") as file:
        file.write(total_apply)
    time.sleep(1000)


# Route utama
@app.route('/', methods=['GET', 'POST'])
def index():
    html_content = None
    if request.method == 'POST':
        url = request.form.get('url')
        platform = int(request.form.get('platform')) 
        print(url,platform)

        if url:
            try:
                if platform == 0:
                    openJobstreet()
                elif platform == 1:
                    openIndeed()
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