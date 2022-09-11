import urllib

import urllib3
from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd


def scrap_urls(url: str)-> None:
    max_pages = 46
    current_page = 20 #17
    while current_page <= max_pages:
        # open the file in the write mode
        current_url = f'{url}/page/{current_page}'
        print(current_url)
        # with open('urls.csv', mode='w', newline='',encoding='utf-8') as urls_file:
        #     urls_writer = csv.writer(urls_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        #     urls_writer.writerow(current_url)
        raw_html = requests.get(current_url)
        #print(raw_html.status_code)
        soup = BeautifulSoup(raw_html.text, 'html.parser')
        for content in soup.find_all('div', {'class':'entry-wrap entry-wrap-archive'}):
            #print(content.text)
            a_tag = content.find("a")
            content_link = a_tag['href']
            content_link = content_link.replace(",", "")
            urls = urllib.parse.unquote(content_link)
            # urls = urllib.parse.unquote(content_link).encode('utf8')
            print(urls)

            localFile = open('urls.csv',  mode='a+', newline='',encoding='utf-8')
            writer = csv.writer(localFile)
            writer.writerow([urls])
            localFile.close()
            raw_page = requests.get(urls)
            raw_soup = BeautifulSoup(raw_page.text, 'html.parser')
            title = raw_soup.find('h1',{'class':'page-header-title'}).text
            content_text =raw_soup.find('div',{'class':'entry-content entry-content-single'}).text

            localFile = open('content.csv', mode='a+', newline='', encoding='utf-8')
            writer = csv.writer(localFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([title])
            writer.writerow([content_text])
            localFile.close()
            # print(urls)
        current_page += 1

def main()-> int:
    url = 'https://www.ebanglalibrary.com/category/%e0%a6%ac%e0%a6%be%e0%a6%82%e0%a6%b2%e0%a6%be-%e0%a6%ae%e0%a6%b9%e0%a6%be%e0%a6%ad%e0%a6%be%e0%a6%b0%e0%a6%a4'
    scrap_urls(url)
    return 0

if __name__ == '__main__':
    exit(main())


