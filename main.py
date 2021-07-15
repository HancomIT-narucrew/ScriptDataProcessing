import requests
import change
from bs4 import BeautifulSoup

def getUrl(input, titles) :
    response = requests.get(input)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.select("a")
        for href in soup.find("div", class_="series_seasons").find_all("li"):
            titles.append(href.find("a")["href"])
    else:
        print(response.status_code)

def getScripts(titles) :
    f = open('The_Moon_Rising_River.txt', 'a+', encoding='UTF-8')    # 원본 파일 생성

    for i in titles:
        url = 'https://subslikescript.com' + i

        html = requests.get(url)
        soup = BeautifulSoup(html.text)

        if html.status_code == 200:
            script_tag = soup.find_all(['script', 'style', 'header', 'footer', 'form'])
            script_tags = ['body > div > div > main > nav.prevnext',
                           'body > div > div > main > article > h1',
                           'body > div > div > main > nav:nth-child(1) > ul',
                           'head > title']

            for script in script_tag:
                script.extract()
            for i in script_tags:
                script_tag2= soup.select_one(i)
                script_tag2.extract()

            content = soup.get_text('\n', strip=True)
            f.write(content)

        else:
            print(html.status_code)

    f.close()

if __name__ == '__main__':
    total_url = 'https://subslikescript.com/series/The_Moon_Rising_River-13634686'
    titles = list()

    # getUrl(total_url, titles)   # 전체 스크립트 URL 가져오기
    # getScripts(titles)    # 스크립트 본문 가져오기
    # change.modifyScripts()     # 스크립트 전처리

    change.attachTag() # 정제된 스크립트에 tag 부착
