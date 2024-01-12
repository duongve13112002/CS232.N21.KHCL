from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import urllib.request 
from time import sleep

#1 Khai báo đường dẫn webdriver và chỉnh option
options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(executable_path="./chromedriver.exe", chrome_options=options)

#2 Kết nối tới trang đích
browser.get('https://images.google.com/')

#3 Truy xuất đến ô tìm kiếm của trang 
search_input = browser.find_element(by=By.XPATH, value='/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')

#4 Nhập tên hình ảnh mà mình muốn crawl
info = 'kubo-san wa mob wo yurusanai cute'
search_input.send_keys(info)

#5 Nhấn enter 
search_input.send_keys(Keys.ENTER) 

src_images = []
path = './image/'

for i in range(20):
    try:
        img = browser.find_element(by=By.XPATH, value = '//*[@id="islrg"]/div[1]/div[' + str(i+1) + ']/a[1]/div[1]/img')
        src_images.append(img.get_attribute("src"))#trích xuất thuộc tính src của ảnh
        sleep(1)
    except:
        continue
number = 0
for src in src_images:
     urllib.request.urlretrieve(src, path + str(number) + ".png") # lưu dưới dạng "png"
     number += 1
sleep(3)

browser.close()