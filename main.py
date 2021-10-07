import os
import cv2
import time
import wget
import platform
import argparse
import subprocess
import chromedriver_autoinstaller

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--email', type=str, dest='email', action='store',
                        required=True, help='E-mail for login on Pinterest.')
    parser.add_argument('--password', type=str, dest='password', action='store',
                        required=True, help='Password for login on Pinterest.')
    parser.add_argument('--link', type=str, dest='link', action='store',
                        help='Url to a pinterest folder.')
    parser.add_argument('--list', type=str, dest='list', action='store',
                        help='Path to a txt file with a list of urls.')
    args = parser.parse_args()
    
    if args.link == None:
        if args.list == None:
            print('Please enter an url or an url file!')
            exit()
        links = open(args.list, 'r').read().splitlines()
    else:
        links = [args.link]
        
    chromedriver_autoinstaller.install()
    
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    
    driver.get("https://br.pinterest.com/")
    
    images_folder = 'images/'
    os.makedirs(images_folder, exist_ok=True)
    
    enterPath = '//*[@id="__PWS_ROOT__"]/div[1]/div/div/div/div[1]/div[1]/div[2]/div[2]/button/div'    
    enterButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, enterPath))).click()
    
    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="email"]')))
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]')))
    
    username.clear()
    username.send_keys(args.email)   
    password.clear()
    password.send_keys(args.password)
    
    enterPath = '//*[@id="__PWS_ROOT__"]/div[1]/div/div/div/div[1]/div[2]/div[2]/div/div/div/div/div/div/div/div[4]/form/div[5]/button/div'
    enterButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, enterPath))).click()
    time.sleep(15)
    
    log_file = open('log.txt','w')

    for i, link in enumerate(links):
        images_path = images_folder + str(i).zfill(6)
        os.mkdir(images_path)
    
        try:
            driver.get(link)
        except TimeoutException as e:
            print('Could not access the link:' + link)
            
        time.sleep(5)

        urls = []
        scroll_times = 0
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            anchors = driver.find_elements_by_tag_name('img')
            anchors = [anchor for anchor in anchors]
            
            for anchor in anchors:
                try:
                    link = anchor.get_attribute('srcset')
                    link = link.split(',')[-1].split(' ')[1]
                    urls.append(link)
                except:
                    continue 
                        
            driver.execute_script("window.scrollBy(0, 50);")
            scroll_times += 1
            
            if scroll_times == 100:
                urls = list(set(urls))
                for url in urls:
                    try:
                        wget.download(url, out=images_path)
                        image_name = url.split('/')[-1]
                        image_path = os.path.join(images_path, image_name)
                        image = cv2.imread(image_path)
                        image_name = image_name.split('.')[0]
                        new_image_path = os.path.join(images_path, image_name, '.jpg')
                        cv2.imwrite(new_image_path,image)
                    except:
                        continue
                
                if platform.system() == 'Windows':
                    subprocess.run(["powershell", "-Command", "Get-ChildItem -recurse -Path images | Where-Object {$_.Name -match '\(1\)'} | Remove-Item"])
                elif platform.system() == 'Linux':
                    os.system("rm *\(1\)*")
                
                urls = []
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                else:
                    last_height = new_height
                    scroll_times = 0
                    driver.execute_script("window.scrollBy(0, 50);")