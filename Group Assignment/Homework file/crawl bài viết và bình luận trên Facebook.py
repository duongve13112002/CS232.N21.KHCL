from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys  import Keys

import os
from time import sleep
import pickle


def readData(fileName):
    f = open(fileName, 'r', encoding='utf-8')
    data = []
    for i, line in enumerate(f):
        try:
            line = repr(line)
            line = line[1:len(line) - 3]
            data.append(line)
        except:
            print("error write line")
    return data

def writeFileTxt(fileName, content):
    with open(fileName, 'a') as f1:
        if('pfb' in content):
            f1.write(content + os.linesep)


def handleComment(TEXT):
    tem = TEXT.text
    tems = tem.split('\n')
    author = tems[0]
    if('đã trả lời' in tem):
        comment = tems[1:len(tems)-2]
        commentTime = tems[len(tems)-1]
    else:
        comment = tems[1:len(tems)-1]
        commentTime = tems[-1]
    
    print('Author', author )
    print("Comment", comment)
    print("Time", commentTime)


def initDriver():
    browser = webdriver.Chrome(executable_path="./chromedriver")

    # 1. open Facebook
    browser.get("https://mbasic.facebook.com/")

    # 2.Load cookie from file

    cookies = pickle.load(open("my_cookie.pkl","rb"))
    for cookie in cookies:
        browser.add_cookie(cookie)
    
    browser.get("https://mbasic.facebook.com/")

    sleep(10)
    return browser


def getContentComment(driver, i):
    try:
        link = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div[1]/div[2]/div/div[5]/div[' +str(i)+ ']/div')
        ids = []
        if(link):
            print(link.text)
            # handleComment(link.text)
            ids.append(link)
            sleep(1)
        return ids, link.text
    except:
        print("error get link")

def getAmountOfComments(driver,postId, numberCommentTake):
    try:
        driver.get("https://mbasic.facebook.com/" + str(postId))

        sleep(3)

        title = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div[1]/div[1]/div/div/div[1]/div').text
        print("Day la title", title)

        sumLinks = []
        result = []
        pre_sum = 0
        i = 1
        while(len(sumLinks) < numberCommentTake):
            if i> pre_sum + 2:
                break
            try:
                pre_sum = len(sumLinks)
                arr, comment = getContentComment(driver, i)
                sumLinks.extend(arr)
                result.append({
                    'link': "https://mbasic.facebook.com/" + str(postId),
                    'title': title,
                    'comment': comment,
                })
            except:
                print('Error when cralw content comment')
            i +=1
        return result  
    except:
        print("Error get cmt")


def getPostIds(driver, filePath = 'posts.csv'):
    allPosts = readData(filePath)
    sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    shareBtn = driver.find_elements(By.XPATH,'//a[contains(@href, "/sharer.php")]')
    if (len(shareBtn)):
        for link in shareBtn:
            postId = link.get_attribute('href').split('sid=')[1].split('&')[0]
            if postId not in allPosts:
                print(postId)
                writeFileTxt(filePath, postId)

def getnumOfPostFanpage(driver, pageId, amount, filePath = 'posts.csv'):
    driver.get("https://touch.facebook.com/" + pageId)
    while len(readData(filePath)) < amount:
        getPostIds(driver, filePath)


driver = initDriver()
isLive =  True

result = []
# isLive = checkLiveCookie(driver, cookie)
if (isLive):
    getnumOfPostFanpage(driver, 'ShopeeVN', 10, 'posts.csv')
    print('Done get nmber post of fanpage')
    # sleep(1000)
    for postId in readData('posts.csv'):
        # print(postId)
        result.append(getAmountOfComments(driver, postId, 5))
        sleep(1)

driver.close()

print(result)

import csv
with open('comment.csv', 'w',  newline = '', encoding='utf-8') as file_output:
    headers = ['Link', "Title", 'Comment']
    writer = csv.DictWriter(file_output, delimiter=',', lineterminator='\n',fieldnames=headers)
    writer.writeheader() 
    for temp in result:
        print(temp)
        # writer.writerow({headers[0]: 'abc',headers[1]:'azc'})
        if temp != []:
            writer.writerow({headers[0]:temp[0]['link'].strip("\n"),headers[1]:  "-".join(temp[0]['title'].split("\n")),headers[2]: "-".join(temp[0]['comment'].split("\n"))})