from bs4 import BeautifulSoup
import requests
import time
import pandas as pd


def fetchSoup(url):
    r = session.get(url)
    htmlContent = r.content
    soup = BeautifulSoup(htmlContent, 'html.parser')
    return soup


session = requests.Session()
itr = 0
baseUrl = 'https://www.ebanglalibrary.com/category/%e0%a6%ac%e0%a6%be%e0%a6%82%e0%a6%b2%e0%a6%be-%e0%a6%ae%e0%a6%b9%e0%a6%be%e0%a6%ad%e0%a6%be%e0%a6%b0%e0%a6%a4/'
baseSoup = fetchSoup(baseUrl)
author = []
postContentList = []

anchors = baseSoup.find(class_='entries-wrap has-columns').find_all('a')


startTime = time.time()

for link in anchors[:100]:
    authorUrl = link.get('href')
    authorSoup = fetchSoup(authorUrl)

    authorName = authorSoup.find(class_='page-header-title').text
    print(authorName)

    try:
        authorDescription = authorSoup.find(class_='archives-description term-description').find('p').text
        author.append([authorName, authorDescription])
    except AttributeError:
        pass

    postList = []
    try:
        for i in authorSoup.find(class_='entries entries-archive has-boxed').find_all('a'):
            postList.append(i)
    except AttributeError:
        pass

    while True:
        try:
            nextUrl = authorSoup.find(class_='pagination-next').find('a').get('href')
            nextSoup = fetchSoup(nextUrl)
            authorSoup = nextSoup

            for i in authorSoup.find(class_='entries entries-archive has-boxed').find_all('a'):
                postList.append(i)
        except AttributeError:
            break

    for post in postList:
        try:
            postLink = post.get('href')
            postSoup = fetchSoup(postLink)
            postContent = postSoup.find(class_='entry-content entry-content-single').text
            postName = postSoup.find(class_='page-header-title').text

            try:
                postName = postName[postName.index('.')+2:]
            except ValueError:
                pass

            postContentList.append([postName, authorName, postContent])
            itr += 1
            print(itr)
        except AttributeError:
            pass

endTime = time.time()

print('Time elapsed : ', endTime - startTime)


df_author = pd.DataFrame(author, columns=['Author Name', 'Description'])
df_literature = pd.DataFrame(postContentList, columns=['Title', 'Author', 'Content'])
df_author.to_csv('Authors.csv')
df_literature.to_csv('Literature.csv')