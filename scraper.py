import os
import datetime
import requests
import lxml.html as html

HOME_URL = 'https://www.larepublica.co/'

XPATH_LINK_TO_ARTICLE = '//text-fill/a/@href'
XPATH_TITLE = '//div[@class="mb-auto"]/text-fill/span/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_ARTICLE = '//div[@class="html-content"]/p/text()'

def parse_news(link, date):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            article_page = response.content.decode('utf-8')
            parsed = html.fromstring(article_page)

            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"', '')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                article = parsed.xpath(XPATH_ARTICLE)
            except IndexError:
                return
            
            with open(f'{date}/{title}.txt', 'w', encoding='utf-8') as file:
                file.write(title)
                file.write('\n\n')
                file.write(summary)
                file.write('\n\n')
                
                for p in article:
                    file.write(p)
                    file.write('\n')
        else:
            raise ValueError(f'Error {response.status_code}')
    except ValueError as e:
        print(e)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            #Se obtienen todos los links de las noticias
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            link_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            today = datetime.date.today().strftime('%m-%d-%Y')
            if not os.path.isdir(today):
                #Se crea la carpeta de la fecha actual
                os.mkdir(today) 

            print(len(link_to_notices))

            for link in link_to_notices:
                parse_news(link, today)
        else:
            raise ValueError(f'Error {response.status_code}')
    except ValueError as e:
        print(e)

def run():
    parse_home()
    
if __name__ == '__main__':
    run()