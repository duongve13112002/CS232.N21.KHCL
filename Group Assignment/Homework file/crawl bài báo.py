
from selenium import webdriver
from time  import sleep
import pandas as pd

import os

#1 Khai báo đường dẫn webdriver
browser=webdriver.Chrome(executable_path="./chromedriver.exe")

#2. Truy cập tới website
browser.get("https://scholar.google.com/citations?hl=vi&user=ddyBSkoAAAAJ")
sleep(3)

showmore_paper = browser.find_element("id",'gsc_bpf_more')
showmore_paper.click()
sleep(3)

title_paper=[]
author_paper=[]
year_paper=[]

paper_list = browser.find_elements("class name",'gsc_a_tr')

for paper in paper_list:
    title = paper.find_element("class name",'gsc_a_at')
    authors = paper.find_element("class name",'gs_gray')
    year=paper.find_element("class name",'gsc_a_h')

    title_paper.append(title.text)
    author_paper.append(authors.text)
    year_paper.append(year.text)

data={'Title': title_paper,'Authors':author_paper,'Year':year_paper}

pd.DataFrame(data).to_csv('./crawl_paper.csv')

browser.close()
