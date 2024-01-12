from selenium import webdriver
from selenium.webdriver.common.keys  import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import csv
import argparse
from time import sleep

# Open Chrome and access to url
driver = webdriver.Chrome(executable_path="./chromedriver.exe")
url = 'https://vnexpress.net/'
driver.get(url)

# Get element article
page_source = BeautifulSoup(driver.page_source)
element_title_articles = page_source.find_all('h3', class_ = "title-news")

# Get title name and link every article article
all_title_link = []
all_title_name = []
all_comments = []

for element in element_title_articles:
    all_title_name.append(element.find('a').get('title'))
    all_title_link.append(element.find('a').get('href'))

print(all_title_name)
print(all_title_link)

# Set up some parameter
num_article = 2
num_commnet = 2
save_file = 'data/comments.csv'


# Get all element comments
all_comments = []

full_object = []

for index,link in enumerate(all_title_link[:5]):
    print(link)
    driver.get(link)
    page_source = BeautifulSoup(driver.page_source)
    
    sleep(5)

    element_comments = set()
    num_of_comment = len(element_comments)
    print(num_of_comment)
    while num_of_comment < num_commnet:
        try:
            comments = page_source.find_all('div', class_='content-comment')
            element_comments.update(comments)
        except:
            break

        try:
            btn = driver.find_element(By.ID, 'show_more_coment')
            driver.execute_scripts("arguments[0].click();",btn)
        except:
            break

    # Get comment text every element comments
    for cmt in list(element_comments):
        try:
            cmt_text = cmt.find('p', 'full_content')
            print('Full content')
            all_comments.append([cmt_text.text])
            full_object.append({
                'link': link,
                'title': all_title_name[index],
                'comment': cmt_text.text,
            })
        except:
            cmt_text = cmt.find('p', 'content_more')
            print('More content')
            
            all_comments.append([cmt_text.text])
            full_object.append({
                'link': link,
                'title': all_title_name[index],
                'comment': cmt_text.text,
            })

    sleep(2)

    #  Save your data to csv
with open(save_file, 'w',  newline = '', encoding='utf-8') as file_output:
    headers = ['Link', 'Title', 'Comment']
    writer = csv.DictWriter(file_output, delimiter=',', lineterminator='\n',fieldnames=headers)
    writer.writeheader() 
    for temp in full_object:
        writer.writerow({headers[0]:temp['link'],headers[1]:temp['title'],headers[2]:temp['comment']})